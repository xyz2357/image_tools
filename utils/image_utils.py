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


def apply_mosaic(image, rect, block_size):
    """
    对图片的指定区域应用马赛克效果。
    :param image: PIL Image 对象
    :param rect: 应用马赛克的区域，格式为 (x, y, width, height)
    :param block_size: 马赛克块的大小
    """
    def get_average_color(image):
        """
        计算图片的平均颜色。
        :param image: PIL Image 对象
        :return: 平均颜色值
        """
        npixels = image.size[0] * image.size[1]
        cols = image.getcolors(npixels)
        sum_cols = [0, 0, 0, 0]
        for col in cols:
            sum_cols[0] += col[1][0] * col[0]
            sum_cols[1] += col[1][1] * col[0]
            sum_cols[2] += col[1][2] * col[0]
            sum_cols[3] += col[1][3] * col[0]  # warning: this will also add mosaic to Alpha. Shall change
        avg_cols = [int(sum_cols[0] / npixels), int(sum_cols[1] / npixels), int(sum_cols[2] / npixels), int(sum_cols[3] / npixels)]
        return tuple(avg_cols)

    x1, y1, width, height = rect
    x2, y2 = x1 + width, y1 + height

    for i in range(x1, x2, block_size):
        for j in range(y1, y2, block_size):
            # 计算当前块的边界
            box = (i, j, min(i + block_size, x2), min(j + block_size, y2))
            # 提取块
            block = image.crop(box)
            # 计算块的平均颜色
            avg_color = get_average_color(block)
            # 用平均颜色填充块
            ImageDraw.Draw(image).rectangle(box, fill=avg_color)