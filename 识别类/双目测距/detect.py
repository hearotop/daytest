from ultralytics import YOLO
import cv2
import numpy as np

# Step 1: 加载 YOLO 模型并进行目标检测
def detect_objects(image_path):
    model = YOLO("yolo11n.pt")  # 加载预训练模型
    results = model.predict(image_path, save=False, imgsz=320, conf=0.5, classes=[63])  # 检测笔记本
    return results[0].boxes.xyxy.cpu().numpy()  # 返回检测框 (x1, y1, x2, y2)

# Step 2: 提取 ROI 区域
def extract_roi(image, bbox):
    x1, y1, x2, y2 = map(int, bbox)
    roi = image[y1:y2, x1:x2]  # 裁剪 ROI 区域
    return roi

# Step 3: 调整 ROI 区域尺寸
def resize_rois(left_roi, right_roi):
    # 获取左右 ROI 的最小宽度和高度
    min_height = min(left_roi.shape[0], right_roi.shape[0])
    min_width = min(left_roi.shape[1], right_roi.shape[1])

    # 调整左右 ROI 到相同的尺寸
    left_resized = cv2.resize(left_roi, (min_width, min_height))
    right_resized = cv2.resize(right_roi, (min_width, min_height))

    return left_resized, right_resized

# Step 4: 特征提取和匹配（使用 ORB）
def match_features(left_roi, right_roi):
    # 初始化特征检测器（ORB）
    detector = cv2.ORB_create()

    # 检测关键点和描述符
    keypoints_left, descriptors_left = detector.detectAndCompute(left_roi, None)
    keypoints_right, descriptors_right = detector.detectAndCompute(right_roi, None)

    # 使用 BFMatcher（暴力匹配器）进行特征匹配
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # 对于 ORB 使用 NORM_HAMMING
    matches = bf.match(descriptors_left, descriptors_right)

    # 按距离排序匹配结果
    matches = sorted(matches, key=lambda x: x.distance)

    # 绘制匹配结果
    matched_image = cv2.drawMatches(
        left_roi, keypoints_left,
        right_roi, keypoints_right,
        matches[:50],  # 只绘制前 50 个最佳匹配
        None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    return matched_image

# Step 5: 计算视差图（使用 StereoBM）
def compute_disparity(left_roi, right_roi):
    # 将灰度图像转换为 8 位单通道格式
    left_gray = cv2.cvtColor(left_roi, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_roi, cv2.COLOR_BGR2GRAY)

    # 使用 StereoBM 算法进行视差计算
    stereo = cv2.StereoBM_create(numDisparities=16 * 5, blockSize=15)
    disparity = stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0

    # 归一化视差图到 0-255 范围
    min_disp = np.min(disparity)
    max_disp = np.max(disparity)
    disparity_normalized = ((disparity - min_disp) / (max_disp - min_disp) * 255).astype(np.uint8)

    return disparity_normalized

# Step 6: 增强视差图的可视化效果
def enhance_disparity_map(disparity):
    # 应用伪彩色映射
    disparity_colored = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)

    # 平滑处理（可选）
    disparity_smoothed = cv2.GaussianBlur(disparity_colored, (5, 5), 0)

    return disparity_smoothed

# 主函数
if __name__ == "__main__":
    # Step 1: 目标检测
    left_bbox = detect_objects("left.jpg")
    right_bbox = detect_objects("right.jpg")

    if len(left_bbox) == 0 or len(right_bbox) == 0:
        print("未检测到目标，请检查图片或模型配置！")
        exit()

    # 假设只检测到一个目标（取第一个检测框）
    left_bbox = left_bbox[0]
    right_bbox = right_bbox[0]

    # Step 2: 加载图片并提取 ROI
    left_img = cv2.imread("left.jpg")
    right_img = cv2.imread("right.jpg")

    left_roi = extract_roi(left_img, left_bbox)
    right_roi = extract_roi(right_img, right_bbox)

    # Step 3: 调整左右 ROI 尺寸
    left_roi, right_roi = resize_rois(left_roi, right_roi)

    # Step 4: 特征匹配
    matched_image = match_features(left_roi, right_roi)

    # Step 5: 计算视差图
    disparity = compute_disparity(left_roi, right_roi)

    # Step 6: 增强视差图的可视化效果
    disparity_enhanced = enhance_disparity_map(disparity)

    # Step 7: 保存特征差异图和视差图
    cv2.imwrite('feature_difference1.png', matched_image)
    cv2.imwrite('disparity_map1.png', disparity_enhanced)

    print("特征差异图片已保存为 'feature_difference1.png'")
    print("视差图已保存为 'disparity_map1.png'")