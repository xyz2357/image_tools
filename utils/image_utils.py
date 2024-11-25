from PIL import Image, ImageDraw
from PyQt5.QtGui import QImage
import numpy as np
import cv2

def pixmap_to_pil_image_with_alpha(pixmap):
    qimage = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
    # get QImage data and convert to a NumPy array
    ptr = qimage.bits()
    ptr.setsize(qimage.byteCount())
    arr = np.array(ptr).reshape(qimage.height(), qimage.width(), 4)  # 4 for ARGB
    # create PIL Image
    pil_image = Image.fromarray(arr, "RGBA")
    return pil_image


def pil_image_to_qimage_with_alpha(pil_image):
    # convert PIL Image to QImage
    arr = np.array(pil_image)
    qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_ARGB32)
    return qimage


def apply_mosaic(pil_image, polygon, block_size):
    """
    Apply mosaic effect to the specified polygon area of the image.
    :param image: PIL Image object
    :param polygon: Polygon area to apply mosaic, format: [(x1, y1), (x2, y2), ..., (xn, yn)]
    :param block_size: Size of the mosaic block
    """
    def get_average_color(pil_image, mask):
        """
        Calculate the average color of the image, only calculate the area where the mask is 1.
        :param image: PIL Image object
        :param mask: numpy array of the mask area
        :return: average color value
        """
        image_data = np.array(pil_image)
        mask_data = mask == 1
        if mask_data.any():
            avg_color = np.mean(image_data[mask_data], axis=0).astype(int)
            return tuple(avg_color)
        return (0, 0, 0, 0)

    # create a blank mask, used to represent the polygon area
    mask = Image.new('L', pil_image.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=1)
    mask_array = np.array(mask)

    # iterate over all pixel blocks of the image and apply mosaic
    for i in range(0, pil_image.width, block_size):
        for j in range(0, pil_image.height, block_size):
            # calculate the boundary of the current block
            box = (i, j, min(i + block_size, pil_image.width), min(j + block_size, pil_image.height))
            block = pil_image.crop(box)
            block_mask = mask_array[j: j + block.size[1], i: i + block.size[0]]

            # check if the current block is in the polygon area
            if np.any(block_mask):
                # calculate the average color, only consider the part in the polygon
                avg_color = get_average_color(block, block_mask)
                # fill the pixels in the polygon area with the average color
                block_data = np.array(block)
                block_data[block_mask == 1] = avg_color
                new_block = Image.fromarray(block_data)
                pil_image.paste(new_block, box)


def apply_optimized_motion_blur_to_polygon(pil_image, polygon, intense, angle):
    """
    Apply motion blur effect to the specified polygon area of the image.
    
    Args:
        pil_image: input PIL Image object
        polygon: list of points [(x1, y1), (x2, y2), ..., (xn, yn)]
        intense: blur intensity
        angle: blur angle (degrees)
    
    Returns:
        PIL Image object after applying motion blur
    """
    open_cv_image = np.array(pil_image)
    rgb_img, alpha_channel = open_cv_image[..., :3], open_cv_image[..., 3]

    # Create a mask for the polygon
    mask = Image.new('L', pil_image.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=1)
    mask_array = np.array(mask)

    # Get the bounding box of the polygon
    x_coords, y_coords = zip(*polygon)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    rect = (min_x, min_y, max_x - min_x, max_y - min_y)

    angle = (angle - 45) % 360
    # generate motion blur kernel
    M = cv2.getRotationMatrix2D((intense / 2, intense / 2), -angle, 1)
    motion_blur_kernel = np.diag(np.ones(intense))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (intense, intense))
    motion_blur_kernel = motion_blur_kernel / np.sum(motion_blur_kernel)

    # Create a weight mask with a linear gradient from the center to the edges
    center_x = rect[0] + rect[2] // 2
    center_y = rect[1] + rect[3] // 2
    y, x = np.ogrid[:rgb_img.shape[0], :rgb_img.shape[1]]
    weight_mask = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    weight_mask = np.clip((1 - weight_mask / np.max(weight_mask)), 0, 1)

    # Apply the kernel to the sub image
    rgb_sub_img = rgb_img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    blurred_sub_img = cv2.filter2D(rgb_sub_img, -1, motion_blur_kernel)

    # Get the polygon mask for the sub image
    mask_sub = mask_array[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    weight_mask_sub = weight_mask[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    
    # Combine polygon mask with weight mask
    final_mask = mask_sub * weight_mask_sub
    final_mask = cv2.merge([final_mask] * 3)  # Make the mask 3 channels

    # Blend the blurred sub image with the original sub image based on the mask
    blended_sub_img = cv2.convertScaleAbs(rgb_sub_img * (1 - final_mask) + blurred_sub_img * final_mask)

    # Reinsert the Alpha channel
    blended_sub_img_with_alpha = cv2.merge([
        blended_sub_img, 
        alpha_channel[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    ])

    # Place the blended part back into the image
    image_with_blur = open_cv_image.copy()
    image_with_blur[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]] = blended_sub_img_with_alpha

    return Image.fromarray(image_with_blur, "RGBA")


if __name__ == "__main__":
    image = Image.open("example.png").convert("RGBA")
    polygon = [(500, 500), (1000, 800), (1500, 1500), (1200, 1000), (1200, 500)]
    block_size = 10
    apply_mosaic(image, polygon, block_size)
    polygon = [(1000, 1000), (1500, 800), (2000, 1200), (1200, 1200), (1200, 1000)]
    intense = 20
    angle = 45
    result = apply_optimized_motion_blur_to_polygon(image, polygon, intense, angle)
    result.show()