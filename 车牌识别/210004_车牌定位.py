import cv2
import numpy as np
import matplotlib.pyplot as plt


def point_limit(point):
    """
    确保像素点是大于0的
    """
    if point[0] < 0:
        point[0] = 0
    if point[1] < 0:
        point[1] = 0


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


if __name__ == "__main__":
    path = "datasets/liscense/images/train/CBLPRD-330k/000000000.jpg"
    image_np = cv2.imread(path)

    img = image_np
    pic_hight, pic_width = img.shape[:2]

    # 高斯去噪
    img = cv2.GaussianBlur(img, (5, 5), 0)
    mat_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 图片灰度化
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mat_im = cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 开运算
    kernel = np.ones((20, 20), np.uint8)
    img_opening = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)
    mat_im = cv2.cvtColor(img_opening, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 图像合并
    img_opening_add = cv2.addWeighted(img_gray, 1, img_opening, -1, 0)
    mat_im = cv2.cvtColor(img_opening_add, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 二值化
    ret, img_thresh = cv2.threshold(img_opening_add, 60, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mat_im = cv2.cvtColor(img_thresh, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 找到图像边缘
    img_edge = cv2.Canny(img_thresh, 100, 200)
    mat_im = cv2.cvtColor(img_edge, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 使用开运算和闭运算让图像边缘成为一个整体
    kernel1 = np.ones((30, 50), np.uint8)
    img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel1)
    mat_im = cv2.cvtColor(img_edge1, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    kernel2 = np.ones((30, 50), np.uint8)
    img_close_open = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel2)

    # 查找图像边缘整体形成的矩形区域，可能有很多，车牌就在其中一个矩形区域中
    contours, hierarchy = cv2.findContours(img_close_open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 一一排除不是车牌的矩形区域
    car_contours = []
    img_drawContoursAll = img.copy()
    img_drawContoursScopeofCompliance = img.copy()
    for cnt in contours:
        img_drawContoursAll = cv2.drawContours(img_drawContoursAll, [cnt], 0, (0, 0, 255), 2)
        mat_im = cv2.cvtColor(img_drawContoursAll, cv2.COLOR_BGR2RGB)
        plt.imshow(mat_im)
        plt.show()
        # 车牌区域允许的面积
        if 200 > cv2.contourArea(cnt) or cv2.contourArea(cnt) > 200000:
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
        mat_im = cv2.cvtColor(img_drawContoursScopeofCompliance, cv2.COLOR_BGR2RGB)
        plt.imshow(mat_im)
        plt.show()

    card_imgs = []
    # 矩形区域可能是倾斜的矩形，需要矫正，以便使用颜色定位
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
    for card_img in card_imgs:
        mat_im = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
        plt.imshow(mat_im)
        plt.show()
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
        for card_img in card_imgs:
            mat_im = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
            plt.imshow(mat_im)
            plt.show()
