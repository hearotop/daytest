import cv2
import numpy as np

# 加载左右图像
left_img = cv2.imread("1.jpg")
right_img = cv2.imread("2.jpg")

# 1. 合并左右图像
def merge_images(left_img, right_img):
    # 假设左右图像大小相同，直接按水平拼接
    merged_image = np.hstack((left_img, right_img))
    return merged_image

# 2. 查看左右图像的差异
def compute_image_difference(left_img, right_img):
    # 将图像转换为灰度图像进行差异计算
    left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
    # 计算两张图像的绝对差异
    difference = cv2.absdiff(left_gray, right_gray)
    # 返回灰度差异图像
    return difference

# 合并左右图像
merged_img = merge_images(left_img, right_img)

# 显示灰度图像
left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

# 计算差异图像并显示
diff_image = compute_image_difference(left_img, right_img)

# 保存合并图像和差异图像
cv2.imwrite("合并图像.png", merged_img)
cv2.imwrite("差异图像.png", diff_image)
 