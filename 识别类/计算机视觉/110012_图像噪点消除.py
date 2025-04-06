import cv2

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    no_noise_image = cv2.blur(image_np, (3, 3))  # 均值滤波
    # 返回处理正确后的内容
    cv2.imshow("image_np", image_np)
    cv2.imshow("no_noise_image", no_noise_image)
    cv2.waitKey(0)
