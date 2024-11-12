from PIL import Image, ImageDraw
from PyQt5.QtGui import QImage
import numpy as np

def pixmap_to_pil_image_with_alpha(pixmap):
    qimage = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
    # 获取 QImage 的数据，并转换为一个 NumPy 数组
    ptr = qimage.bits()
    ptr.setsize(qimage.byteCount())
    arr = np.array(ptr).reshape(qimage.height(), qimage.width(), 4)  # 4 for ARGB
    # 创建 PIL Image
    pil_image = Image.fromarray(arr, "RGBA")
    print(pil_image.mode)
    return pil_image


def pil_image_to_qimage_with_alpha(pil_image):
    # 将 PIL Image 转换为 Qmiage
    arr = np.array(pil_image)
    qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_ARGB32)
    return qimage


def apply_mosaic(image, polygon, block_size):
    """
    对图片的指定多边形区域应用马赛克效果。
    :param image: PIL Image 对象
    :param polygon: 应用马赛克的多边形区域，格式为 [(x1, y1), (x2, y2), ..., (xn, yn)]
    :param block_size: 马赛克块的大小
    """
    def get_average_color(image, mask):
        """
        计算图片的平均颜色，仅计算遮罩为1的区域。
        :param image: PIL Image 对象
        :param mask: 遮罩区域的numpy数组
        :return: 平均颜色值
        """
        image_data = np.array(image)
        mask_data = mask == 1
        if mask_data.any():
            avg_color = np.mean(image_data[mask_data], axis=0).astype(int)
            return tuple(avg_color)
        return (0, 0, 0, 0)

    # 创建一个空白遮罩，用于表示多边形区域
    mask = Image.new('L', image.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=1)
    mask_array = np.array(mask)

    # 遍历图像的所有像素块，并应用马赛克
    for i in range(0, image.width, block_size):
        for j in range(0, image.height, block_size):
            # 计算当前块的边界
            box = (i, j, min(i + block_size, image.width), min(j + block_size, image.height))
            block = image.crop(box)
            block_mask = mask_array[j: j + block.size[1], i: i + block.size[0]]

            # 检查该块是否在多边形区域内
            if np.any(block_mask):
                # 计算块的平均颜色，仅考虑多边形内的部分
                avg_color = get_average_color(block, block_mask)
                # 使用平均颜色填充多边形区域内的像素
                block_data = np.array(block)
                block_data[block_mask == 1] = avg_color
                new_block = Image.fromarray(block_data)
                image.paste(new_block, box)

if __name__ == "__main__":
    # 示例用法
    image = Image.open("example.png").convert("RGBA")
    polygon = [(100, 100), (150, 80), (200, 120), (180, 200), (120, 220)]
    block_size = 10
    apply_mosaic(image, polygon, block_size)
    image.show()