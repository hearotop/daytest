import cv2
import numpy as np

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    hsv_image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)  # 转为HSV空间
    color_low = np.array([[0, 43, 46], [10, 255, 255]][0])
    color_high = np.array([[0, 43, 46], [10, 255, 255]][1])
    mask_image_np = cv2.inRange(hsv_image_np, color_low, color_high)  # 创建掩膜
    color_image_np = cv2.bitwise_and(image_np, image_np, mask=mask_image_np)  # 获得颜色识别后的图像
    cv2.imshow("mask_image_np", mask_image_np)
    cv2.imshow("color_image_np", color_image_np)
    cv2.waitKey(0)
