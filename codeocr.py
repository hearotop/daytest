import cv2
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import os


###############################################################
##
##车牌识别代码                                                             
##@_main_port 程序入口代码
##@predict_code 车牌识别代码
##@point_limit 像素限制代码
##@color_limit 颜色识别代码
##@accurate_place #识别范围代码
##@find_waves 找波峰，分割字符代码
##@preprocess_hog  获取图像的水平和竖直方向梯度，拿到hog特征代码
###############################################################

# 省份，不包含所有省份，数据集缺失
provinces = [
    "zh_cuan", "川", "zh_e", "鄂", "zh_gan", "赣", "zh_gan1", "甘", "zh_gui", "贵", "zh_gui1", "桂", "zh_hei", "黑",
             "zh_hu", "沪", "zh_ji", "冀", "zh_jin", "津", "zh_jing", "京", "zh_jl", "吉", "zh_liao", "辽", "zh_lu", "鲁",
             "zh_meng", "蒙", "zh_min", "闽", "zh_ning", "宁", "zh_qing", "靑", "zh_qiong", "琼", "zh_shan", "陕", "zh_su",
             "苏", "zh_sx", "晋", "zh_wan", "皖", "zh_xiang", "湘", "zh_xin", "新", "zh_yu", "豫", "zh_yu1", "渝", "zh_yue",
             "粤", "zh_yun", "云", "zh_zang", "藏", "zh_zhe", "浙"
]


#像素限制代码
def point_limit(point):
    """
    确保像素点是大于0的
    """
    if point[0] < 0:
        point[0] = 0
    if point[1] < 0:
        point[1] = 0

#识别范围代码
def accurate_place(card_img_hsv, limit1, limit2, color):
    """
    根据颜色缩小图片的范围，去掉不包含该颜色的像素行或列
    """
    row_num, col_num = card_img_hsv.shape[:2]
    xl = col_num
    xr = 0
    yh = 0
    yl = row_num
    row_num_limit = 21
    col_num_limit = col_num * 0.8 if color != "green" else col_num * 0.5  # 绿色有渐变
    for i in range(row_num):
        count = 0
        for j in range(col_num):
            H = card_img_hsv.item(i, j, 0)
            S = card_img_hsv.item(i, j, 1)
            V = card_img_hsv.item(i, j, 2)
            if limit1 < H <= limit2 and 34 < S and 46 < V:
                count += 1
        if count > col_num_limit:
            if yl > i:
                yl = i
            if yh < i:
                yh = i
    for j in range(col_num):
        count = 0
        for i in range(row_num):
            H = card_img_hsv.item(i, j, 0)
            S = card_img_hsv.item(i, j, 1)
            V = card_img_hsv.item(i, j, 2)
            if limit1 < H <= limit2 and 34 < S and 46 < V:
                count += 1
        if count > row_num - row_num_limit:
            if xl > j:
                xl = j
            if xr < j:
                xr = j
    return xl, xr, yh, yl


# 根据设定的阈值和图片直方图，找出波峰，用于分隔字符
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


# 来自opencv的sample
# 获取图像的水平和竖直方向梯度，拿到hog特征
def preprocess_hog(digits):
    samples = []
    for img in digits:
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
        mag, ang = cv2.cartToPolar(gx, gy)
        bin_n = 16
        bin = np.int32(bin_n * ang / (2 * np.pi))
        bin_cells = bin[:10, :10], bin[10:, :10], bin[:10, 10:], bin[10:, 10:]
        mag_cells = mag[:10, :10], mag[10:, :10], mag[:10, 10:], mag[10:, 10:]
        hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
        hist = np.hstack(hists)

        # transform to Hellinger kernel
        eps = 1e-7
        hist /= hist.sum() + eps
        hist = np.sqrt(hist)
        hist /= norm(hist) + eps

        samples.append(hist)
    return np.float32(samples)
#颜色识别功能代码
def color_limit(path):
    # 如果是字符则去读图片
    if type(path) == type(""):
        img =cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

    # 否则直接用
    else:
        img = path
    # 图片的高度、宽度
    #if img is None:
     # print("图片加载失败")
    
    pic_hight, pic_width = img.shape[:2]
    #if pic_width > 1000:  # 宽度限制是1000
     #       resize_rate = 1000 / pic_width  # 得到小于1的数，用于高度也等此比例缩小
      #      img = cv2.resize(img, (1000, int(pic_hight * resize_rate)),
       #                      interpolation=cv2.INTER_AREA)  # 图片分辨率调整  区域插值
        # cv2.imshow('Image', img)
    #kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 定义一个核
    #img = cv2.filter2D(img, -1, kernel=kernel)  # 空间锐化滤波 进行卷积操作 类似拉普拉斯算子

    

    # 高斯去噪
    img = cv2.GaussianBlur(img, (5, 5), 0)
    #mat_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 图片灰度化
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #mat_im = cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
    # 开运算
    kernel = np.ones((20, 20), np.uint8)#50,80
    img_opening = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)
    #mat_im = cv2.cvtColor(img_opening, cv2.COLOR_BGR2RGB)
    # 图像合并
    img_opening = cv2.addWeighted(img_gray, 1, img_opening, -1, 0)
    #mat_im = cv2.cvtColor(img_opening, cv2.COLOR_BGR2RGB)


    # 二值化
    ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #mat_im = cv2.cvtColor(img_thresh, cv2.COLOR_BGR2RGB)
   
    # 找到图像边缘
    img_edge = cv2.Canny(img_thresh, 100, 200)
    #mat_im = cv2.cvtColor(img_edge, cv2.COLOR_BGR2RGB)
  

    # 使用开运算和闭运算让图像边缘成为一个整体
    kernel = np.ones((4,19), np.uint8)
    img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)  # 闭运算
    
    img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)  # 开运算
   

# 查找图像边缘整体形成的矩形区域，可能有很多，车牌就在其中一个矩形区域中 CHAIN_APPROX_SIMPLE指保留拐点
    try:
        image, contours, hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except ValueError:
        # ValueError: not enough values to unpack (expected 3, got 2)
        # cv2.findContours方法在高版本OpenCV中只返回两个参数
        contours, hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 2000]  # 把大于2000的矩形选出来

    # 一一排除不是车牌的矩形区域
    car_contours = []
    #img_drawContoursAll = img.copy()
    #img_drawContoursScopeofCompliance = img.copy()
    """for cnt in contours:
        img_drawContoursAll = cv2.drawContours(img_drawContoursAll, [cnt], 0, (0, 0, 255), 2)
        mat_im = cv2.cvtColor(img_drawContoursAll, cv2.COLOR_BGR2RGB)
       
        # 车牌区域允许的面积
        if 200 > cv2.contourArea(cnt) or cv2.contourArea(cnt) > 2000:
            continue
        # 获取最小外接矩阵，中心点坐标，宽高，旋转角度
        rect = cv2.minAreaRect(cnt)

        # 要求矩形区域长宽比在2到5.5之间
        area_width, area_height = rect[1]
        wh_ratio = area_height / area_width if area_width < area_height else area_width / area_height
        # 矩形长宽比
        if 2 < wh_ratio < 5.5:
            car_contours.append(rect)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            img_drawContoursScopeofCompliance = cv2.drawContours(img_drawContoursScopeofCompliance, [box], 0,
                                                                 (0, 0, 255), 2)
        mat_im = cv2.cvtColor(img_drawContoursScopeofCompliance, cv2.COLOR_BGR2RGB)"""
    for cnt in contours:
            # 框选 生成最小外接矩形 返回值（中心(x,y), (宽,高), 旋转角度）
            rect = cv2.minAreaRect(cnt)

            # print('宽高:',rect[1])
            area_width, area_height = rect[1]

            # 1 选择宽大于高的区域
            wh_ratio = area_height / area_width if area_width < area_height else area_width / area_height


            # print('宽高比：',wh_ratio)
            # 要求矩形区域长宽比在2到5.5之间，2到5.5是车牌的长宽比，其余的矩形排除
            if wh_ratio > 2 and wh_ratio < 5.5:
                car_contours.append(rect)
                # box = cv2.boxPoints(rect)
                # box = np.int0(box)
            # 框出所有可能的矩形
            # oldimg = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
            # cv2.imshow("Test",oldimg )

        # 矩形区域可能是倾斜的矩形，需要矫正，以便使用颜色定位
    

    card_imgs = []
    # 矩形区域可能是倾斜的矩形，需要矫正，以便使用颜色定位
    print(f"找到的轮廓数量: {len(contours)}")
    print(f"符合要求的矩形区域数量: {len(car_contours)}")
    if len(car_contours) == 0:
      print("未找到符合要求的矩形区域")
    for rect in car_contours:
        # 使得左、高、右、低拿到正确的值
        if -1 < rect[2] < 1:  # 车牌的角度在-1到1之间
            angle = 1
        elif rect[2] == 90:  # 车牌是正的
            box = cv2.boxPoints(rect)
            point_list = []
            for point in box:
                point_list.append(point)
            card_img = img[int(point_list[0][1]):int(point_list[2][1]), int(point_list[0][0]):int(point_list[2][0])]
            card_imgs.append(card_img)
            continue
        else:  # 车牌不是正的
            angle = rect[2]
        rect = (rect[0], (rect[1][0] + 5, rect[1][1] + 5), angle)  # 扩大范围，避免车牌边缘被排除
        
        # 获取矩形四个顶点，浮点型
        box = cv2.boxPoints(rect)
        heigth_point = right_point = [0, 0]
        left_point = low_point = [pic_width, pic_hight]
        # 四次循环，拿到绘制出的矩阵四个点的横纵坐标最值的点。
        for point in box:
            if left_point[0] > point[0]:
                left_point = point
            if low_point[1] > point[1]:
                low_point = point
            if heigth_point[1] < point[1]:
                heigth_point = point
            if right_point[0] < point[0]:
                right_point = point
        # 正角度,左低右高
        if left_point[1] <= right_point[1]:
            new_right_point = [right_point[0], heigth_point[1]]
            pts2 = np.float32([left_point, heigth_point, new_right_point])
            pts1 = np.float32([left_point, heigth_point, right_point])
            # 仿射变换
            M = cv2.getAffineTransform(pts1, pts2)
            dst = cv2.warpAffine(img, M, (pic_width, pic_hight))
            point_limit(new_right_point)
            point_limit(heigth_point)
            point_limit(left_point)
            # 切割出经过矫正后的车牌
            card_img = dst[int(left_point[1]):int(heigth_point[1]), int(left_point[0]):int(new_right_point[0])]
            # 可能有多个车牌多次进入循环，所以用列表放起来
            card_imgs.append(card_img)
        # 负角度,左高右低
        elif left_point[1] > right_point[1]:
            new_left_point = [left_point[0], heigth_point[1]]
            pts2 = np.float32([new_left_point, heigth_point, right_point])
            pts1 = np.float32([left_point, heigth_point, right_point])
            # 仿射变换
            M = cv2.getAffineTransform(pts1, pts2)
            dst = cv2.warpAffine(img, M, (pic_width, pic_hight))
            point_limit(right_point)
            point_limit(heigth_point)
            point_limit(new_left_point)
            # 切割出经过矫正后的车牌
            card_img = dst[int(right_point[1]):int(heigth_point[1]), int(new_left_point[0]):int(right_point[0])]
            # 可能有多个车牌多次进入循环，所以用列表放起来
            card_imgs.append(card_img)
    #for card_img in card_imgs:
     #   mat_im = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
      #  plt.imshow(mat_im)
      #  plt.show()
    # 开始使用颜色定位，排除不是车牌的矩形，目前只识别蓝、绿、黄车牌
    colors = []
    global_card_index = []
    for card_index, card_img in enumerate(card_imgs):
        green = yello = blue = black = white = 0
        if card_img.shape[0] <= 0 or card_img.shape[1] <= 0:
            continue
        card_img_hsv = cv2.cvtColor(card_img, cv2.COLOR_BGR2HSV)
        # 有转换失败的可能，原因来自于上面矫正矩形出错
        if card_img_hsv is None:
            continue
        row_num, col_num = card_img_hsv.shape[:2]
        card_img_count = row_num * col_num
        # 逐一像素点遍历，观察是哪个颜色，并让该颜色+1
        for i in range(row_num):
            for j in range(col_num):
                H = card_img_hsv.item(i, j, 0)
                S = card_img_hsv.item(i, j, 1)
                V = card_img_hsv.item(i, j, 2)
                if 11 < H <= 34 < S:  # 像素是黄色，yellow+1
                    yello += 1
                elif 35 < H <= 99 and S > 34:  # 像素是绿色，green+1
                    green += 1
                elif 99 < H <= 124 and S > 34:  # 像素是蓝色，blue+1
                    blue += 1
                if 0 < H < 180 and 0 < S < 255 and 0 < V < 46:  # 像素是黑色，blue+1
                    black += 1
                elif 0 < H < 180 and 0 < S < 43 and 221 < V < 225:  # 像素是白色，blue+1
                    white += 1
        color = "no"
        # 某个颜色的像素个数大于整个车牌像素个数的一半，就认为车牌是该颜色
        limit1 = limit2 = 0
        if yello * 2 >= card_img_count:
            color = "yello"
            limit1 = 11
            limit2 = 34  # 有的图片有色偏偏绿
        elif green * 2 >= card_img_count:
            color = "green"
            limit1 = 35
            limit2 = 99
        elif blue * 2 >= card_img_count:
            color = "blue"
            limit1 = 100
            limit2 = 124  # 有的图片有色偏偏紫
        elif black + white >= card_img_count * 0.7:
            color = "bw"
        colors.append(color)
        if limit1 == 0:
            continue
        # 以下为根据车牌颜色再定位，缩小边缘非车牌边界
        xl, xr, yh, yl = accurate_place(card_img_hsv, limit1, limit2, color)
        if yl == yh and xl == xr:
            continue
        need_accurate = False
        if yl >= yh:
            yl = 0
            yh = row_num
            need_accurate = True
        if xl >= xr:
            xl = 0
            xr = col_num
            need_accurate = True
        if color != "green" or yl < (yh - yl) // 4:
            card_imgs[card_index] = card_img[yl:yh, xl:xr]
        else:
            card_imgs[card_index] = card_img[yl - (yh - yl) // 4:yh, xl:xr]
        if need_accurate:  # 可能x或y方向未缩小，需要再试一次
            card_img = card_imgs[card_index]
            card_img_hsv = cv2.cvtColor(card_img, cv2.COLOR_BGR2HSV)
            xl, xr, yh, yl = accurate_place(card_img_hsv, limit1, limit2, color)
            if yl == yh and xl == xr:
                continue
            if yl >= yh:
                yl = 0
                yh = row_num
            if xl >= xr:
                xl = 0
                xr = col_num
        card_imgs[card_index] = card_img[yl:yh, xl:xr] \
            if color != "green" or yl < (yh - yl) // 4 else card_img[yl - (yh - yl) // 4:yh, xl:xr]
        global_card_index.append(card_index)
        #for card_img in card_imgs:
         #   mat_im = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
    return card_imgs, colors
###车牌预测功能代码
def predict_code(card_imgs, colors):
    card_color = None
    roi=None
    predict_results=[]
    binary_diaplay_imgs = []
    x_histogram_imgs = []
    y_histogram_imgs = []
    for i, color in enumerate(colors):
        if color in ("blue", "yello", "green"):
            card_img = card_imgs[i]
            gray_img = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)

            # 黄、绿车牌字符比背景暗、与蓝车牌刚好相反，所以黄、绿车牌需要反向
            if color == "green" or color == "yello":
                gray_img = cv2.bitwise_not(gray_img)

            # 二值化
            ret, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            binary_diaplay_imgs.append(binary_img)

            # 查找水平直方图波峰
            x_histogram = np.sum(binary_img, axis=1)

            # 显示X轴直方图
            x_max = np.max(x_histogram)
            x_proportion = x_max / binary_img.shape[1]
            if x_proportion == 0:
                print("二值化的取值有问题！")
                continue
            x_histogram_normalized = x_histogram / x_proportion
            x_histogram_img = np.ones((binary_img.shape[0], binary_img.shape[1]), dtype=np.uint8) * 255
            for y in range(binary_img.shape[0]):
                x_histogram_img[y][0:int(x_histogram_normalized[y] - 1)] = 0

            cv2.cvtColor(x_histogram_img, cv2.COLOR_BGR2RGB)
           
            x_histogram_imgs.append(x_histogram_img)

            x_min = np.min(x_histogram)
            x_average = np.sum(x_histogram) / x_histogram.shape[0]
            x_threshold = (x_min + x_average) / 2

            wave_peaks = find_waves(x_threshold, x_histogram)
            # print(wave_peaks)
            if len(wave_peaks) == 0:
                print("peak less 0:")
                continue
            # 认为水平方向，最大的波峰为车牌区域
            wave = max(wave_peaks, key=lambda x: x[1] - x[0])
            binary_img = binary_img[wave[0]:wave[1]]

            # 查找垂直直方图波峰
            row_num, col_num = binary_img.shape[:2]
            # 去掉车牌上下边缘1个像素，避免白边影响阈值判断
            binary_img = binary_img[1:row_num - 1]
            y_histogram = np.sum(binary_img, axis=0)

            # 显示Y轴直方图
            y_max = np.max(y_histogram)
            y_proportion = y_max / binary_img.shape[0]
            y_histogram_normalized = y_histogram / y_proportion
            y_histogram_img = np.ones((binary_img.shape[0], binary_img.shape[1]), dtype=np.uint8) * 255
            for x in range(binary_img.shape[1]):
                cv2.line(y_histogram_img, [x, binary_img.shape[0]],
                            [x, binary_img.shape[0] - int(y_histogram_normalized[x])], (0, 0, 0), 1, 8)

            #cv2.cvtColor(y_histogram_img, cv2.COLOR_BGR2RGB)
        

            y_histogram_imgs.append(y_histogram_img)
            y_min = np.min(y_histogram)
            y_average = np.sum(y_histogram) / y_histogram.shape[0]
            y_threshold = (y_min + y_average) / 5  # U和0要求阈值偏小，否则U和0会被分成两半

            wave_peaks = find_waves(y_threshold, y_histogram)
            # 车牌字符数应大于6
            if len(wave_peaks) <= 6:
                print(f"peak less {len(wave_peaks)}:")
                continue
            wave = max(wave_peaks, key=lambda x: x[1] - x[0])
            max_wave_dis = wave[1] - wave[0]
            # 判断是否是左侧车牌边缘
            if wave_peaks[0][1] - wave_peaks[0][0] < max_wave_dis / 3 and wave_peaks[0][0] == 0:
                wave_peaks.pop(0)

            # 通过竖直波峰分离汉字
            cur_dis = 0
            for i, wave in enumerate(wave_peaks):
                if wave[1] - wave[0] + cur_dis > max_wave_dis * 0.6:
                    break
                else:
                    cur_dis += wave[1] - wave[0]
            if i > 0:
                wave = (wave_peaks[0][0], wave_peaks[i][1])
                wave_peaks = wave_peaks[i + 1:]
                wave_peaks.insert(0, wave)
            # 去除车牌上的分隔点
            if len(wave_peaks) <= 2:
                continue
            point = wave_peaks[2]
            if point[1] - point[0] < max_wave_dis / 3:
                point_img = binary_img[:, point[0]:point[1]]
                if np.mean(point_img) < 255 / 5:
                    wave_peaks.pop(2)
            # print(wave_peaks)
            if len(wave_peaks) <= 6:
                print(f"peak less 2 {len(wave_peaks)}:")
                continue
            # 根据找出的波峰，分隔图片，从而得到逐个字符图片
            part_cards = []
            predict_results = []
            card_colors = []
            for wave in wave_peaks:
                part_cards.append(binary_img[:, wave[0]:wave[1]])
            for i, part_card in enumerate(part_cards):
                # 可能是固定车牌的铆钉
                if np.mean(part_card) < 255 / 5:
                    print("a point")
                    continue
                part_card_old = part_card
                w = abs(part_card.shape[1] - 20) // 2

                part_card = cv2.copyMakeBorder(part_card, 0, 0, w, w, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                part_card = cv2.resize(part_card, (20, 20), interpolation=cv2.INTER_AREA)

                cv2.cvtColor(part_card, cv2.COLOR_BGR2RGB)
    
                # 提取hog特征，识别车牌
                part_card = preprocess_hog([part_card])
                if i == 0:
                    modelchinese = cv2.ml.SVM_create()
                    modelchinese.setGamma(0.5)
                    modelchinese.setC(1)
                    modelchinese.setKernel(cv2.ml.SVM_RBF)
                    modelchinese.setType(cv2.ml.SVM_C_SVC)
                    modelchinese = modelchinese.load("model/svmchinese.dat")
                    r = modelchinese.predict(part_card)
                    resp = r[1].ravel()
                    charactor = provinces[int(resp[0]) - 1000]
                else:
                    model = cv2.ml.SVM_create()
                    model.setGamma(0.5)
                    model.setC(1)
                    model.setKernel(cv2.ml.SVM_RBF)
                    model.setType(cv2.ml.SVM_C_SVC)
                    model = model.load("model/svm.dat")
                    r = model.predict(part_card)
                    resp = r[1].ravel()
                    charactor = chr(int(resp[0]))
                # 判断最后一个数是否是车牌边缘，假设车牌边缘被认为是1
                if charactor == "1" and i == len(part_cards) - 1:
                        if color == 'blue' and len(part_cards) > 7:
                            if part_card_old.shape[0] / part_card_old.shape[1] >= 7:  # 1太细，认为是边缘
                                continue
                        elif color == 'blue' and len(part_cards) > 7:
                            if part_card_old.shape[0] / part_card_old.shape[1] >= 7:  # 1太细，认为是边缘
                                continue
                        elif color == 'green' and len(part_cards) > 8:
                            if part_card_old.shape[0] / part_card_old.shape[1] >= 7:  # 1太细，认为是边缘
                                continue
                """if charactor == "1" and i == len(part_cards) - 1:
                        if part_card_old.shape[0] / part_card_old.shape[1] >= 7:  # 1太细，认为是边缘
                            continue"""
                predict_results.append(charactor)
            card_colors.append(color)
            
            card_color = color
            break
    #roi=old_img
    return predict_results,  card_color#roi
#程序入口
def _main_port(path):
    result = {}
    
    card_imgs, colors = color_limit(path)
    if card_imgs is []:
        return
    else:
        # 分割字符并识别车牌文字
        predict_result, card_color = predict_code(card_imgs, colors)

     #  结果显示
        if predict_result != []:
       
            if card_color == 'blue':
                result['Type'] = '蓝牌'
            elif card_color == 'green':
                result['Type'] = '绿牌'
            elif card_color == 'yellow':
                result['Type'] = '黄牌'    
            result['List'] = predict_result
            a=""
            for i in range(len(predict_result)):
                a=a+predict_result[i]
            result['Code']=a
           # result['Picture'] = roi
            return result
        else:
            return None
    
if __name__ == "__main__":
    #model_path_chinese = "./model/svmchinese.dat"
    #model_path = "./model/svm.dat"
    #if not os.path.exists(model_path_chinese) or not os.path.exists(model_path):
    #  print("SVM模型文件不存在")
    path = "Test/蒙AB0008.jpg"
    #if not os.path.exists(path):
    #  print("图片路径不存在")

    result=_main_port(path)
    print(result)
    
    # 切割车牌中的字符，根据直方图的波峰来定位
    # 开始逐一排查颜色块
    