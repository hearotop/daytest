import cv2
import numpy as np

if __name__ == "__main__":
    # 读取图片路径
    path = "./demo.png"
    # 读取图片
    image_np = cv2.imread(path)
    # 亮度变换是对图像的每个通道的每个像素进行统一的加某个值
    # np.clip是一个截取函数，用于截取数组中小于或者大于某值的部分，并使得被截取部分等于固定值。
    # np.uint8是将值转换为0-255的整数
    brightness_conversion_img = np.uint8(np.clip((1.0 * image_np + (0)), 0, 255))
    # 显示图片
    cv2.imshow("brightness_conversion_image", brightness_conversion_img)
    cv2.waitKey(0)
