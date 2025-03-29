import cv2
import numpy as np

"""
相关过程详见:https://zhuanlan.zhihu.com/p/36656952
"""
if __name__ == "__main__":
    path_origin = "./demo.png"
    image_np = cv2.imread(path_origin)
    path_logo = "./logo.png"
    logo = cv2.imread(path_logo)
    rows, cols = logo.shape[:2]
    roi = image_np[:rows, :cols]
    gray_logo = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    ret, mask_logo = cv2.threshold(gray_logo, 127, 255, cv2.THRESH_BINARY_INV)  # 得到logo的掩膜
    image_np_bg = cv2.bitwise_and(roi, roi, mask=mask_logo)  # 通过位于操作得到图片除掩膜以外的背景
    # 图像融合
    dst = cv2.add(image_np_bg, logo)
    image_np[:rows, :cols] = dst
    cv2.imshow("mask_logo", mask_logo)
    cv2.imshow("image_np_bg", image_np_bg)
    cv2.imshow("image_np", image_np)
    cv2.waitKey(0)
