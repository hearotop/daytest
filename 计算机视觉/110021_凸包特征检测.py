import cv2
import numpy as np

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    convex_image = image_np.copy()
    image_np_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    ret, image_np_thresh = cv2.threshold(image_np_gray, 127, 255, cv2.THRESH_BINARY)  # 进行二值化
    contours, hierarchy = cv2.findContours(image_np_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 查找轮廓
    cnt = contours[0]
    # 寻找凸包
    hull = cv2.convexHull(cnt)
    # 绘制凸包
    cv2.polylines(convex_image, [hull], True, (0, 0, 255), 2)
    # 返回处理正确后的内容
    cv2.imshow("convex_image", convex_image)
    cv2.waitKey(0)
