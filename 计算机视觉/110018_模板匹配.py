import cv2
import numpy as np

if __name__ == "__main__":
    path_search = "./demo.png"
    image_np = cv2.imread(path_search)
    image_np_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)  # 转为灰度图(原图)
    path_target = "./template.png"
    template = cv2.imread(path_target)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # 转为灰度图(匹配模板)
    h, w = template_gray.shape[:2]
    res = cv2.matchTemplate(image_np_gray, template_gray, cv2.TM_CCOEFF_NORMED)  # 模板匹配
    threshold = 0.8
    loc = np.where(res >= threshold)  # 匹配程度大于threshold的坐标y,x
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        right_bottom = (pt[0] + w, pt[1] + h)
        cv2.rectangle(image_np, pt, right_bottom, (0, 0, 255), 2)
    # 返回处理正确后的内容
    cv2.imshow("image_np", image_np)
    cv2.waitKey(0)
