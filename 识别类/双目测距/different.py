import cv2
import numpy as np
from ultralytics import YOLO

# iMX686 传感器的相关参数
sensor_diag_mm = 9.251  # 传感器对角线尺寸（毫米）
sensor_width_mm = 7.401  # 传感器宽度（毫米）
sensor_height_mm = 5.551  # 传感器高度（毫米）
pixel_size_um = 0.80  # 像素尺寸（微米）

# 传感器的分辨率
sensor_resolution_width = 9248  # 水平方向像素数
sensor_resolution_height = 6944  # 垂直方向像素数

# 焦距计算
image_width_pixels = 640  # 假设输入图像的宽度为 640 像素
f_mm = (sensor_diag_mm * image_width_pixels) / sensor_resolution_width  # 计算焦距（毫米）
f_pixel = f_mm * (image_width_pixels / sensor_width_mm)  # 转换为像素单位

print(f"计算的焦距（像素）：{f_pixel:.2f}")

# 加载YOLO模型
model = YOLO("yolo11n.pt")  

# 加载左右图像
left_img = cv2.imread("left.jpg")
right_img = cv2.imread("right.jpg")

print(f"左图像尺寸: {left_img.shape}, 右图像尺寸: {right_img.shape}")

# 使用YOLO模型获取笔记本电脑的检测框
results = model(left_img, save=True, imgsz=640, conf=0.5, classes=[63])# 只识别笔记本
boxes = results[0].boxes
if len(boxes) == 0:
    raise ValueError("未在左图像中检测到物体")
left_bbox = boxes[0].xyxy[0].cpu().numpy().astype(int)
print(f"检测到的边界框: {left_bbox}")

# 设置双目相机参数
baseline = 77.2  # mm
f_pixel = f_pixel  # 焦距像素单位
image_width_pixels = left_img.shape[1]
left_camera_matrix = np.array([[f_pixel, 0, image_width_pixels / 2],
                               [0, f_pixel, left_img.shape[0] / 2],
                               [0, 0, 1]])
right_camera_matrix = left_camera_matrix.copy()
left_distortion = np.zeros(5)
right_distortion = np.zeros(5)
R = np.eye(3)
T = np.array([[baseline], [0], [0]])

# 图像矫正并提取 ROI
def resize_rois(left_roi, right_roi):
    h = min(left_roi.shape[0], right_roi.shape[0])
    w = min(left_roi.shape[1], right_roi.shape[1])
    return cv2.resize(left_roi, (w, h)), cv2.resize(right_roi, (w, h))

def rectify_and_crop_roi(left_img, right_img, bbox, camera_params):
    left_K, left_D, right_K, right_D, R, T = camera_params

    R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(
        left_K, left_D, right_K, right_D,
        left_img.shape[:2][::-1], R, T
    )

    left_mapX, left_mapY = cv2.initUndistortRectifyMap(
        left_K, left_D, R1, P1, left_img.shape[:2][::-1], cv2.CV_32FC1
    )
    right_mapX, right_mapY = cv2.initUndistortRectifyMap(
        right_K, right_D, R2, P2, right_img.shape[:2][::-1], cv2.CV_32FC1
    )

    left_rectified = cv2.remap(left_img, left_mapX, left_mapY, cv2.INTER_LINEAR)
    right_rectified = cv2.remap(right_img, right_mapX, right_mapY, cv2.INTER_LINEAR)

    x1, y1, x2, y2 = bbox
    left_roi = left_rectified[y1:y2, x1:x2]
    right_roi = right_rectified[y1:y2, x1:x2]

    return resize_rois(left_roi, right_roi)

camera_params = (left_camera_matrix, left_distortion, right_camera_matrix, right_distortion, R, T)
left_roi, right_roi = rectify_and_crop_roi(left_img, right_img, left_bbox, camera_params)

# 计算视差图
def compute_disparity(left_roi, right_roi):
    left_gray = cv2.cvtColor(left_roi, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_roi, cv2.COLOR_BGR2GRAY)

    window_size = 5
    stereo = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=64,
        blockSize=5,
        P1=8 * 3 * window_size ** 2,
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32
    )
    disparity = stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0
    print(f"视差范围: 最小={np.min(disparity):.2f}, 最大={np.max(disparity):.2f}")
    return disparity

disparity = compute_disparity(left_roi, right_roi)

# 计算深度图
def compute_depth_map(disparity_map):
    with np.errstate(divide='ignore'):
        depth_map = (baseline * f_pixel) / disparity_map
        depth_map[disparity_map <= 0] = 0
        depth_map[depth_map == np.inf] = 0
    return depth_map

depth_map = compute_depth_map(disparity)

# 可视化深度图（改为灰度图）
def visualize_depth_map(depth_map):
    # 归一化深度图到 [0, 255] 范围
    norm_depth = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
    # 转换为 8 位灰度图像
    return norm_depth.astype(np.uint8)

depth_gray = visualize_depth_map(depth_map)

# 输出平均距离和最小距离
def output_distance_results(depth_map):
    depth_vals = depth_map[depth_map > 0]
    if len(depth_vals) == 0:
        print("未找到有效的深度值。")
        return 0, 0
    avg_distance = np.mean(depth_vals)
    min_distance = np.min(depth_vals)
    print(f"📏 最小距离: {min_distance:.2f} mm ({min_distance/1000:.2f} m)")
    print(f"📏 平均距离: {avg_distance:.2f} mm ({avg_distance/1000:.2f} m)")
    return min_distance, avg_distance

min_dist, avg_dist = output_distance_results(depth_map)

# 保存结果图像和距离结果
cv2.imwrite("深度图_灰度.png", depth_gray)  # 保存灰度深度图
cv2.imwrite("视差图.png", (disparity * (255.0 / np.max(disparity))).astype(np.uint8))  # 保存视差图

with open("结果.txt", "w") as f:
    f.write(f"最小距离: {min_dist:.2f} mm ({min_dist/1000:.2f} m)\n")
    f.write(f"平均距离: {avg_dist:.2f} mm ({avg_dist/1000:.2f} m)\n")

print("✅ 所有结果已保存。")