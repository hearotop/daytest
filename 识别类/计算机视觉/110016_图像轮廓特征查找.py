import cv2

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    contour_image = image_np.copy()
    image_np_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    ret, image_np_thresh = cv2.threshold(image_np_gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # 进行二值化
    contours, hierarchy = cv2.findContours(image_np_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 查找轮廓
    cv2.drawContours(contour_image, contours, -1, (0, 0, 255), 2)  # 绘制轮廓
    # 绘制外接矩形
    circumscribed_contour_image = contour_image.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(circumscribed_contour_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # 返回处理正确后的内容
    cv2.imshow("contour_image", contour_image)
    cv2.imshow("circumscribed_contour_image", circumscribed_contour_image)
    cv2.waitKey(0)
