import cv2
import numpy as np

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    img_shape = image_np.shape
    image_np_gray = np.zeros((img_shape[0], img_shape[1]), dtype=np.uint8)  # image_np.copy()
    # 加权灰度化
    wr = 0.299
    wg = 0.587
    wb = 0.114
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            image_np_gray[i, j] = (int(wr * image_np[i, j][2]) + int(wg * image_np[i, j][1]) + int(
                wb * image_np[i, j][0]))
    # 二值化
    ret, image_np_thresh = cv2.threshold(image_np_gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("image_np_gray", image_np_gray)
    cv2.imshow("image_np_thresh", image_np_thresh)
    cv2.waitKey(0)
