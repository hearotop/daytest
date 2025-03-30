import cv2
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path = "./images/02.png"
    image_np = cv2.imread(path)

    # 进行高斯模糊操作
    blurred = cv2.GaussianBlur(image_np, (5, 5), 0)
    mat_im = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 进行图片灰度化
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    mat_im = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 进行二值化
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mat_im = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()

    # 在二值图片中寻找轮廓
    cts, hrch = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历每一个轮廓
    for c in cts:
        # 计算每一个轮廓的中心点
        M = cv2.moments(c)
        if int(M["m00"]) == 0:
            continue
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))

        # 进行形状检测
        # 求出轮廓周长
        peri = cv2.arcLength(c, True)
        # 找近似的轮廓，例如：把0.04*周长的线段认为是一个边
        approx = cv2.approxPolyDP(c, float(0.04) * peri, True)
        # print(approx)

        # 如果当前的轮廓含有3个顶点，则其为三角形
        if len(approx) == 3:
            shape = "triangle"
        # 如果当前的轮廓含有4个顶点，则其可能是矩形或者正方形
        elif len(approx) == 4:
            # 获取轮廓的边界框并计算长和宽的比例
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if 0.95 <= ar <= 1.05:
                shape = "square"
            else:
                shape = "rectangle"
        # 如果这个轮廓含有5个顶点，则它是一个多边形
        elif len(approx) == 5:
            shape = "pentagon"
        # 其它顶点，是一个圆
        else:
            shape = "circle"

        # 绘制轮廓
        color = {"red": (0, 0, 255), "yellow": (0, 255, 255), "blue": (255, 0, 0)}
        cv2.drawContours(image_np, [c], -1, color["red"], 2)

        # 绘制形状文字
        cv2.putText(image_np, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color["red"], 2)
    mat_im = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()
