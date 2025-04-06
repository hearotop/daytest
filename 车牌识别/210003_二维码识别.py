import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path = "./images/03.png"
    image_np = cv2.imread(path)

    # 读取微信识别的模型文件， caffe训练的模型。
    # 注意这里的模型路径，生成代码不会附带模型，需要自己将模型放在合适的路径
    # detect：二维码检测
    # sr:二维码增强
    detector = cv2.wechat_qrcode_WeChatQRCode("./models/wechat_qrcode_model/detect.prototxt",
                                              "./models/wechat_qrcode_model/detect.caffemodel",
                                              "./models/wechat_qrcode_model/sr.prototxt",
                                              "./models/wechat_qrcode_model/sr.caffemodel")

    res, points = detector.detectAndDecode(image_np)
    result = []
    for i in range(len(points)):
        # 将float转换成int，像素值没有float之说
        one_pt = np.array(points[i], dtype=np.int32)

        # 绘制轮廓
        color = {"red": (0, 0, 255), "yellow": (0, 255, 255), "blue": (255, 0, 0)}
        cv2.drawContours(image_np, [one_pt], -1, color["red"], 2)
    print("识别内容：", res)
    mat_im = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    plt.imshow(mat_im)
    plt.show()
