import cv2

if __name__ == "__main__":
    path = "./demo.png"
    image_np = cv2.imread(path)
    img_shape = image_np.shape
    # 对图片进行旋转
    M = cv2.getRotationMatrix2D((img_shape[1] // 2, img_shape[0] // 2), 45, 0.5)
    rotation_image = cv2.warpAffine(image_np, M, (img_shape[1], img_shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    cv2.imshow("rotation_image", rotation_image)
    cv2.waitKey(0)
