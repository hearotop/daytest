import cv2
import numpy as np

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32)
    dst_image = cv2.filter2D(image_np, -1, kernel)  # 垂直边缘提取
    # 返回处理正确后的内容
    cv2.imshow("dst_image", dst_image)
    cv2.waitKey(0)
