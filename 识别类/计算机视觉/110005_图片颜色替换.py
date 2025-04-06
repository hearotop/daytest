import cv2
import numpy as np

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    hsv_image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)  # 转为HSV空间
    color_low = np.array([[0, 43, 46], [10, 255, 255]][0])
    color_high = np.array([[0, 43, 46], [10, 255, 255]][1])
    mask_image_np = cv2.inRange(hsv_image_np, color_low, color_high)  # 创建掩膜
    # 开操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    open_image_np = cv2.morphologyEx(mask_image_np, cv2.MORPH_OPEN, kernel)
    # 替换颜色
    image_np[open_image_np == 255] = (255, 0, 0)
    cv2.imshow("mask_image_np", mask_image_np)
    cv2.imshow("image_np", image_np)
    cv2.waitKey(0)
