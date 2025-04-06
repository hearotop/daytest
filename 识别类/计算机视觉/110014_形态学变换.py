import cv2

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    image_np_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    ret, image_np_thresh = cv2.threshold(image_np_gray, 127, 255, cv2.THRESH_BINARY)  # 进行二值化
    # 形态学操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morph_images = cv2.erode(image_np_thresh, kernel)
    # 返回处理正确后的内容
    cv2.imshow("morph_images", morph_images)
    cv2.waitKey(0)
