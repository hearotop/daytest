import cv2
import numpy as np
import matplotlib.pyplot as plt

class colorOCR:
    def __init__(self,path):
        self.path=path
    def _main_(self):
        path = self.path
        image_np = cv2.imread(path)
        # BGR转换为HSV颜色空间
        image_hsv_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)

        # 将区间内的颜色设置为白色，区间外的颜色为黑色
        hsv_low = [26, 43, 46]
        hsv_up = [34, 255, 255]
        image_bnr_np = cv2.inRange(image_hsv_np, np.array(hsv_low), np.array(hsv_up))
        mat_im = cv2.cvtColor(image_bnr_np, cv2.COLOR_BGR2RGB)
        #plt.imshow(mat_im)
        #plt.show()

        # 对二值化图进行中值滤/波
        image_aft_ft_np = cv2.medianBlur(image_bnr_np, 7)
        mat_im = cv2.cvtColor(image_aft_ft_np, cv2.COLOR_BGR2RGB)
        #plt.imshow(mat_im)
        #plt.show()

        # 开运算，先腐蚀，后膨胀
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        image_op_np = cv2.morphologyEx(image_aft_ft_np, cv2.MORPH_OPEN, kernel, iterations=1)
        mat_im = cv2.cvtColor(image_op_np, cv2.COLOR_BGR2RGB)
        #plt.imshow(mat_im)
        #plt.show()

        # 寻找轮廓
        cts, hrch = cv2.findContours(image_op_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 逐一排查轮廓
        for i in range(len(cts)):
            contour = cts[i]
            area = cv2.contourArea(contour)
            # 面积小于200和大于200000的丢弃
            if area < 200 or area > 200000:
                continue
            color = {"red": (0, 0, 255), "yellow": (0, 255, 255), "blue": (255, 0, 0)}
            image_np = cv2.drawContours(image_np, [cts[i]], -1, color["red"], 2)
        mat_im = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        #plt.imshow(mat_im)
        #plt.show()
