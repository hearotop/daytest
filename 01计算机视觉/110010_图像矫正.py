import cv2
import numpy as np

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    img_shape = image_np.shape
    # 原图中卡片的四个角点
    pts1 = np.float32([[148, 80], [437, 114], [94, 247], [423, 288]])
    img_line = image_np.copy()
    cv2.line(img_line, pts1[0].astype(np.int64).tolist(), pts1[1].astype(np.int64).tolist(), (0, 0, 255), 2,
             cv2.LINE_AA)
    cv2.line(img_line, pts1[0].astype(np.int64).tolist(), pts1[2].astype(np.int64).tolist(), (0, 0, 255), 2,
             cv2.LINE_AA)
    cv2.line(img_line, pts1[3].astype(np.int64).tolist(), pts1[1].astype(np.int64).tolist(), (0, 0, 255), 2,
             cv2.LINE_AA)
    cv2.line(img_line, pts1[3].astype(np.int64).tolist(), pts1[2].astype(np.int64).tolist(), (0, 0, 255), 2,
             cv2.LINE_AA)
    # 变换后分别在左上、右上、左下、右下四个点
    pts2 = np.float32([[0, 0], [img_shape[1], 0], [0, img_shape[0]], [img_shape[1], img_shape[0]]])
    pts = cv2.getPerspectiveTransform(pts1, pts2)  # 生成透视变换矩阵
    correct_image = cv2.warpPerspective(image_np, pts, (img_shape[1], img_shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)  # 进行透视变换
    # 返回处理正确后的内容
    cv2.imshow("image_np", image_np)
    cv2.imshow('img_line', img_line)
    cv2.imshow("correct_image", correct_image)
    cv2.waitKey(0)
