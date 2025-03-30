import cv2

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    image_np_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    ret, image_np_thresh = cv2.threshold(image_np_gray, 127, 255, cv2.THRESH_BINARY)  # 进行二值化
    edges_images = cv2.Canny(image_np_thresh, 30, 70)  # canny边缘检测
    # 返回处理正确后的内容
    cv2.imshow("edges_images", edges_images)
    cv2.waitKey(0)
