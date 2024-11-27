from PIL import Image, ImageDraw, ImageFont
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
    """Apply mosaic effect to the specified polygon area of the image."""
    def get_average_color(pil_image, mask):
        image_data = np.array(pil_image)
        mask_data = mask == 1
        if mask_data.any():
            avg_color = np.mean(image_data[mask_data], axis=0).astype(int)
            return tuple(avg_color)
        return (0, 0, 0, 0)

    mask = Image.new('L', pil_image.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=1)
    mask_array = np.array(mask)

    for i in range(0, pil_image.width, block_size):
        for j in range(0, pil_image.height, block_size):
            box = (i, j, min(i + block_size, pil_image.width), min(j + block_size, pil_image.height))
            block = pil_image.crop(box)
            block_mask = mask_array[j: j + block.size[1], i: i + block.size[0]]

            if np.any(block_mask):
                avg_color = get_average_color(block, block_mask)
                block_data = np.array(block)
                block_data[block_mask == 1] = avg_color
                new_block = Image.fromarray(block_data)
                pil_image.paste(new_block, box)

def apply_optimized_motion_blur_to_polygon(pil_image, polygon, intense, angle):
    """Apply motion blur effect to the specified polygon area of the image."""
    open_cv_image = np.array(pil_image)
    rgb_img, alpha_channel = open_cv_image[..., :3], open_cv_image[..., 3]

    mask = Image.new('L', pil_image.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=1)
    mask_array = np.array(mask)

    x_coords, y_coords = zip(*polygon)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    rect = (min_x, min_y, max_x - min_x, max_y - min_y)

    angle = (angle - 45) % 360
    M = cv2.getRotationMatrix2D((intense / 2, intense / 2), -angle, 1)
    motion_blur_kernel = np.diag(np.ones(intense))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (intense, intense))
    motion_blur_kernel = motion_blur_kernel / np.sum(motion_blur_kernel)

    center_x = rect[0] + rect[2] // 2
    center_y = rect[1] + rect[3] // 2
    y, x = np.ogrid[:rgb_img.shape[0], :rgb_img.shape[1]]
    weight_mask = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    weight_mask = np.clip((1 - weight_mask / np.max(weight_mask)), 0, 1)

    rgb_sub_img = rgb_img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    blurred_sub_img = cv2.filter2D(rgb_sub_img, -1, motion_blur_kernel)

    mask_sub = mask_array[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    weight_mask_sub = weight_mask[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    
    final_mask = mask_sub * weight_mask_sub
    final_mask = cv2.merge([final_mask] * 3)

    blended_sub_img = cv2.convertScaleAbs(rgb_sub_img * (1 - final_mask) + blurred_sub_img * final_mask)
    blended_sub_img_with_alpha = cv2.merge([
        blended_sub_img, 
        alpha_channel[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    ])

    image_with_blur = open_cv_image.copy()
    image_with_blur[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]] = blended_sub_img_with_alpha

    return Image.fromarray(image_with_blur, "RGBA")

class CameraEffectConfig:
    """Configuration for camera effect overlay"""
    # Size ratios
    REC_TEXT_SIZE_RATIO = 0.04
    REC_CIRCLE_RADIUS_RATIO = REC_TEXT_SIZE_RATIO / 4
    MARGIN_RATIO = 0.05
    RECT_LINE_WIDTH_RATIO = 0.01
    BATTERY_LINE_WIDTH_RATIO = 0.005
    CORNER_LENGTH_RATIO = 0.1
    ICON_OFFSET_RATIO = 4
    ARC_RADIUS_RATIO = 0.025

    # Battery dimensions
    BATTERY_BODY_WIDTH_RATIO = 16
    BATTERY_BODY_HEIGHT_RATIO = 8
    BATTERY_HEAD_WIDTH_RATIO = 3
    BATTERY_HEAD_HEIGHT_RATIO = 3

    # Colors
    OUTLINE_COLOR = "white"
    REC_COLOR = (0, 0, 255)  # red in BGR
    TIMER_COLOR = "white"
    TIMER_OUTLINE_WIDTH = 2
    TIMER_OUTLINE_COLOR = "gray"

    @staticmethod
    def get_battery_color(battery_level):
        """Return appropriate battery color based on level
        
        Returns:
            tuple: BGR color values
            - Red (0, 0, 255) for level <= 0.3
            - Yellow (0, 191, 255) for level <= 0.6
            - Green (127, 255, 0) for level > 0.6
        """
        if battery_level <= 0.3:
            return (0, 0, 255)
        elif battery_level <= 0.6:
            return (0, 191, 255)
        return (127, 255, 0)

def _draw_corner_frames(draw, image, margin, line_width, cfg):
    """Draw corner frame decorations"""
    arc_radius = int(cfg.ARC_RADIUS_RATIO * min(image.width, image.height))
    arc_line_shift = line_width / 2
    corner_length = int(cfg.CORNER_LENGTH_RATIO * min(image.width, image.height))

    # Top-left corner
    draw.line([(margin + arc_radius / 2, margin), (margin + corner_length, margin)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.line([(margin, margin + arc_radius / 2), (margin, margin + corner_length)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.arc([(margin - arc_line_shift, margin - arc_line_shift), 
              (margin + 2 * arc_radius - arc_line_shift, margin + 2 * arc_radius - arc_line_shift)], 
             start=180, end=270, fill=cfg.OUTLINE_COLOR, width=line_width)

    # Top-right corner
    draw.line([(image.width - margin - corner_length, margin), 
               (image.width - margin - arc_radius / 2, margin)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.line([(image.width - margin, margin + arc_radius / 2), 
               (image.width - margin, margin + corner_length)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.arc([(image.width - margin - 2 * arc_radius + arc_line_shift, margin - arc_line_shift), 
              (image.width - margin + arc_line_shift, margin + 2 * arc_radius - arc_line_shift)], 
             start=270, end=360, fill=cfg.OUTLINE_COLOR, width=line_width)

    # Bottom-left corner
    draw.line([(margin + arc_radius / 2, image.height - margin), 
               (margin + corner_length, image.height - margin)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.line([(margin, image.height - margin - corner_length), 
               (margin, image.height - margin - arc_radius / 2)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.arc([(margin - arc_line_shift, image.height - margin - 2 * arc_radius + arc_line_shift), 
              (margin + 2 * arc_radius - arc_line_shift, image.height - margin + arc_line_shift)], 
             start=90, end=180, fill=cfg.OUTLINE_COLOR, width=line_width)

    # Bottom-right corner
    draw.line([(image.width - margin - corner_length, image.height - margin), 
               (image.width - margin - arc_radius / 2, image.height - margin)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.line([(image.width - margin, image.height - margin - corner_length), 
               (image.width - margin, image.height - margin - arc_radius / 2)], 
             fill=cfg.OUTLINE_COLOR, width=line_width)
    draw.arc([(image.width - margin - 2 * arc_radius + arc_line_shift, 
               image.height - margin - 2 * arc_radius + arc_line_shift), 
              (image.width - margin + arc_line_shift, image.height - margin + arc_line_shift)], 
             start=0, end=90, fill=cfg.OUTLINE_COLOR, width=line_width)

def _draw_battery_indicator(draw, margin, line_width, level_ratio, fill_color, cfg):
    """Draw battery level indicator"""
    icon_offset = line_width * cfg.ICON_OFFSET_RATIO
    body_width = int(cfg.BATTERY_BODY_WIDTH_RATIO * line_width)
    body_height = int(cfg.BATTERY_BODY_HEIGHT_RATIO * line_width)
    head_width = int(cfg.BATTERY_HEAD_WIDTH_RATIO * line_width)
    head_height = int(cfg.BATTERY_HEAD_HEIGHT_RATIO * line_width)

    # Draw battery body
    battery_body = [(margin + icon_offset, margin + icon_offset), 
                   (margin + icon_offset + body_width, margin + icon_offset + body_height)]
    battery_head = [(margin + icon_offset + body_width, 
                    margin + icon_offset + (body_height - head_height) // 2),
                   (margin + icon_offset + body_width + head_width, 
                    margin + icon_offset + (body_height + head_height) // 2)]
    battery_fill = [(margin + icon_offset + line_width, margin + icon_offset + line_width),
                   (margin + icon_offset + level_ratio * body_width - line_width, 
                    margin + icon_offset + body_height - line_width)]
    
    draw.rectangle(battery_body, outline=cfg.OUTLINE_COLOR, width=line_width)
    draw.rectangle(battery_head, outline=cfg.OUTLINE_COLOR, width=line_width, fill=cfg.OUTLINE_COLOR)
    draw.rectangle(battery_fill, fill=fill_color)

def _draw_rec_indicator(draw, image, margin, min_dim, cfg):
    """Draw REC indicator with circle and text"""
    rec_text_size = int(cfg.REC_TEXT_SIZE_RATIO * min_dim)
    rec_circle_radius = int(cfg.REC_CIRCLE_RADIUS_RATIO * min_dim)
    corner_length = int(cfg.CORNER_LENGTH_RATIO * min_dim)
    icon_offset = int(cfg.ICON_OFFSET_RATIO * cfg.BATTERY_LINE_WIDTH_RATIO * min_dim)

    try:
        font = ImageFont.truetype("arial.ttf", rec_text_size)
    except IOError:
        font = ImageFont.load_default()

    rec_circle_position = (image.width - margin - corner_length + icon_offset - rec_text_size - rec_circle_radius // 2,
                         margin + icon_offset + rec_circle_radius)
    
    draw.ellipse([(rec_circle_position[0] - rec_circle_radius, rec_circle_position[1] - rec_circle_radius),
                  (rec_circle_position[0] + rec_circle_radius, rec_circle_position[1] + rec_circle_radius)],
                 fill=cfg.REC_COLOR, outline=cfg.REC_COLOR)
    
    draw.text((rec_circle_position[0] + rec_circle_radius + icon_offset, 
               rec_circle_position[1] - rec_text_size // 2),
              "REC", fill=cfg.REC_COLOR, font=font)

def _draw_timer(draw, margin, line_width, timer_text, height, cfg):
    """Draw timer text"""
    rec_text_size = int(cfg.REC_TEXT_SIZE_RATIO * height)
    icon_offset = line_width * cfg.ICON_OFFSET_RATIO

    try:
        font = ImageFont.truetype("arial.ttf", rec_text_size)
    except IOError:
        font = ImageFont.load_default()

    draw.text((margin + icon_offset, height - margin - icon_offset - rec_text_size),
              timer_text, fill=cfg.TIMER_COLOR, font=font,
              stroke_width=cfg.TIMER_OUTLINE_WIDTH, stroke_fill=cfg.TIMER_OUTLINE_COLOR)

def add_camera_effect(image, battery_level_ratio=1, timer_text=""):
    """
    Add camera-style overlay effects to an image
    """
    battery_level_ratio = max(battery_level_ratio, 0.2)
    cfg = CameraEffectConfig
    
    min_dim = min(image.width, image.height)
    margin = int(cfg.MARGIN_RATIO * min_dim)
    rect_line_width = max(1, int(cfg.RECT_LINE_WIDTH_RATIO * min_dim))
    battery_line_width = max(1, int(cfg.BATTERY_LINE_WIDTH_RATIO * min_dim))
    
    draw = ImageDraw.Draw(image)
    
    _draw_corner_frames(draw, image, margin, rect_line_width, cfg)
    _draw_battery_indicator(draw, margin, battery_line_width, battery_level_ratio,
                          cfg.get_battery_color(battery_level_ratio), cfg)
    _draw_rec_indicator(draw, image, margin, min_dim, cfg)
    
    if timer_text:
        _draw_timer(draw, margin, battery_line_width, timer_text, image.height, cfg)
    
    return image

if __name__ == "__main__":
    image = Image.open("example.png").convert("RGBA")
    polygon = [(500, 500), (1000, 800), (1500, 1500), (1200, 1000), (1200, 500)]
    block_size = 10
    apply_mosaic(image, polygon, block_size)
    polygon = [(1000, 1000), (1500, 800), (2000, 1200), (1200, 1200), (1200, 1000)]
    intense = 20
    angle = 45
    result = apply_optimized_motion_blur_to_polygon(image, polygon, intense, angle)
    result = add_camera_effect(result, battery_level_ratio=0.5, timer_text="10:00")
    result.show()