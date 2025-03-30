import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import *


def find_waves(threshold, histogram):
    up_point = -1  # 上升点
    is_peak = False
    if histogram[0] > threshold:
        up_point = 0
        is_peak = True
    wave_peaks = []
    for i, x in enumerate(histogram):
        if is_peak and x < threshold:
            if i - up_point > 2:
                is_peak = False
                wave_peaks.append((up_point, i))
        elif not is_peak and x >= threshold:
            is_peak = True
            up_point = i
    if is_peak and up_point != -1 and i - up_point > 4:
        wave_peaks.append((up_point, i))
    return wave_peaks


if __name__ == "__main__":
    path = "./images/05_1.png"
    image_np = cv2.imread(path)
    image_np_show = image_np.copy()

    pic_hight, pic_width = image_np.shape[:2]

    # BGR转换为HSV颜色空间
    image_hsv_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
    mat_im = cv2.cvtColor(image_hsv_np, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 将黄色设置为白色，非黄色为黑色
    hsv_low = [26, 43, 46]
    hsv_up = [34, 255, 255]
    image_bnr_np = cv2.inRange(image_hsv_np, np.array(hsv_low), np.array(hsv_up))

    # 对二值化图进行中值滤波
    image_aft_ft_np = cv2.medianBlur(image_bnr_np, 7)
    mat_im = cv2.cvtColor(image_aft_ft_np, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 开运算，先腐蚀，后膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    image_op_np = cv2.morphologyEx(image_aft_ft_np, cv2.MORPH_OPEN, kernel, iterations=1)
    mat_im = cv2.cvtColor(image_op_np, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 寻找轮廓
    cts, hrch = cv2.findContours(image_op_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_contours = []

    # 逐一排查轮廓 
    for contour in cts:
        area = cv2.contourArea(contour)
        # 面积小于1000的丢弃
        if area < 1000:
            continue

        # 获取最小外接矩阵，中心点坐标，宽高，旋转角度
        rect = cv2.minAreaRect(contour)

        # 要求矩形区域长宽比在2到5.5之间，其余的矩形排除
        area_width, area_height = rect[1]
        wh_ratio = area_height / area_width if area_width < area_height else area_width / area_height
        # 长宽比
        if 2 < wh_ratio < 5.5:
            num_contours.append(rect)

    # 矫正数字块
    correction_imgs = []
    correction_imgs_location = []
    for rect in num_contours:
        angle = rect[2]
        box = np.int0(cv2.boxPoints(rect))
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)
        crop_img = image_bnr_np[y1:y2, x1:x2]
        correction_imgs_location.append([x1, y1 + 20])
        # 角度等于90度
        if angle == 90:
            img_fin = crop_img
        else:
            box = cv2.boxPoints(rect)
            heigth_point = right_point = [0, 0]
            left_point = low_point = [pic_width, pic_hight]
            # 四次循环，拿到绘制出的矩阵四个点的横纵坐标最大值的点。
            for point in box:
                if left_point[0] > point[0]:
                    left_point = point
                if low_point[1] > point[1]:
                    low_point = point
                if heigth_point[1] < point[1]:
                    heigth_point = point
                if right_point[0] < point[0]:
                    right_point = point
            if left_point[1] <= right_point[1]:  # 正角度,左低右高
                mat = cv2.getRotationMatrix2D((crop_img.shape[1] / 2, crop_img.shape[0] / 2), angle - 90, 1)
            else:  # 负角度,左高右低
                mat = cv2.getRotationMatrix2D((crop_img.shape[1] / 2, crop_img.shape[0] / 2), angle, 1)

            img_fin = cv2.warpAffine(crop_img, mat, (crop_img.shape[1], crop_img.shape[0]))

        img_fin_copy = img_fin.copy()
        mat_im = cv2.cvtColor(img_fin, cv2.COLOR_BGR2RGB)
        plt.imshow(mat_im)
        plt.show()

        w = img_fin.shape[0]
        h = img_fin.shape[1]
        # 查找水平直方图波峰
        x_histogram = np.sum(img_fin, axis=1)
        x_min = np.min(x_histogram)
        x_average = np.sum(x_histogram) / x_histogram.shape[0]
        # x方向的黑色像素的阈值是（最小值+平均值）/5
        x_threshold = (x_min + x_average) / 5
        # 根据阈值寻找没有黑边的位置
        wave_peaks = find_waves(x_threshold, x_histogram)
        # 黑边附近还有一些零碎的黑色干扰物，也去掉
        img_fin[0:wave_peaks[0][0] + (w // 30)] = 255
        img_fin[wave_peaks[0][1] - (w // 30):] = 255

        # 查找竖直直方图波峰
        y_histogram = np.sum(img_fin_copy, axis=0)
        y_min = np.min(y_histogram)
        y_average = np.sum(y_histogram) / y_histogram.shape[0]
        # x方向的黑色像素的阈值是（最小值+平均值）/5
        y_threshold = (y_min + y_average) / 5
        # 根据阈值寻找没有黑边的位置
        wave_peaks = find_waves(y_threshold, y_histogram)
        # 黑边附近还有一些零碎的黑色干扰物，也去掉
        img_fin[:, 0:wave_peaks[0][0] + (h // 30)] = 255
        img_fin[:, wave_peaks[0][1] - (h // 30):] = 255
        mat_im = cv2.cvtColor(img_fin, cv2.COLOR_BGR2RGB)
        plt.imshow(mat_im)
        plt.show()
        correction_imgs.append(img_fin)

    inputs = Input(shape=[28, 28, 1])
    conv_1 = Conv2D(6, 5, activation="relu", padding="same")(inputs)
    pool_1 = MaxPooling2D((2, 2))(conv_1)
    conv_2 = Conv2D(16, 5, activation="relu", padding="same")(pool_1)
    pool_2 = MaxPooling2D((2, 2))(conv_2)
    fc_0 = Flatten()(pool_2)
    fc_1 = Dense(120, activation="relu")(fc_0)
    fc_2 = Dense(84, activation="relu")(fc_1)
    fc_3 = Dense(10, activation="softmax")(fc_2)
    model_lenet5 = Model(inputs, fc_3)
    model_lenet5.load_weights("./models/num_rec_cnn_model/LeNet5.ckpt")

    predict_result = []
    for correction_img, correction_img_location in zip(correction_imgs, correction_imgs_location):
        correction_img_28 = cv2.resize(correction_img, (28, 28))
        ret, img_thresh = cv2.threshold(correction_img_28, 127, 255, cv2.THRESH_BINARY_INV)
        index = np.argmax(model_lenet5.predict(np.array([img_thresh])))
        predict_result.append(index)
        image_np_show = cv2.putText(image_np_show, f'{index}', correction_img_location, cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                    (0, 0, 255), 2, cv2.LINE_AA)
    mat_im = cv2.cvtColor(image_np_show, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()
