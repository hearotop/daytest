import cv2
import numpy as np

"""
绘制直方图
"""


def calcAndDrawHist(image, color):
    hist = cv2.calcHist([image], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256, 256, 3], np.uint8)
    hpt = int(0.9 * 256)

    for h in range(256):
        intensity = int(hist[h] * hpt / maxVal)
        cv2.line(histImg, (h, 256), (h, 256 - intensity), color)

    return histImg


if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    color = {"red": (0, 0, 255), "blue": (255, 0, 0), "green": (0, 255, 0)}
    # 灰度
    image_np_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # 绘制
    hist_image = calcAndDrawHist(image_np_gray, color["blue"])
    # 普通的直方图均衡化
    equ_hist_image_np = cv2.equalizeHist(image_np_gray)
    equ_hist_image = calcAndDrawHist(equ_hist_image_np, color["blue"])
    # 返回处理正确后的内容
    cv2.imshow("image_np_gray", image_np_gray)
    cv2.imshow("hist_image", hist_image)
    cv2.imshow("equ_hist_image_np", equ_hist_image_np)
    cv2.imshow("equ_hist_image", equ_hist_image)
    cv2.waitKey(0)
