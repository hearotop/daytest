import os
import cv2
import numpy as np
from numpy.linalg import norm


# 来自opencv的sample
# 在找到HOG之前，使用其二阶矩对图像进行偏斜校正
def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11'] / m['mu02']
    M = np.float32([[1, skew, -0.5 * 20 * skew], [0, 1, 0]])
    img = cv2.warpAffine(img, M, (20, 20), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
    return img


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


# 省份，不包含所有省份，数据集缺失
provinces = [
    "zh_cuan", "川", "zh_e", "鄂", "zh_gan", "赣", "zh_gan1", "甘", "zh_gui", "贵", "zh_gui1", "桂", "zh_hei", "黑",
    "zh_hu", "沪", "zh_ji", "冀", "zh_jin", "津", "zh_jing", "京", "zh_jl", "吉", "zh_liao", "辽", "zh_lu", "鲁",
    "zh_meng", "蒙", "zh_min", "闽", "zh_ning", "宁", "zh_qing", "靑", "zh_qiong", "琼", "zh_shan", "陕", "zh_su", "苏",
    "zh_sx", "晋", "zh_wan", "皖", "zh_xiang", "湘", "zh_xin", "新", "zh_yu", "豫", "zh_yu1", "渝", "zh_yue", "粤",
    "zh_yun", "云", "zh_zang", "藏", "zh_zhe", "浙"
]

if __name__ == "__main__":
    # 加载SVM模型，训练英文
    model = cv2.ml.SVM_create()
    model.setGamma(0.5)
    model.setC(1)
    model.setKernel(cv2.ml.SVM_RBF)
    model.setType(cv2.ml.SVM_C_SVC)

    chars_train = []
    chars_label = []

    # 注意：数据集的路径需要按照自己的实际路径做修改 
    for root, dirs, files in os.walk("./Train/chars"):
        if len(os.path.basename(root)) > 1:
            continue
        root_int = ord(os.path.basename(root))
        # 读取字母和数字的图片数据，并转换为灰度图，读取文件名，作为标签
        for filename in files:
            print(f"File_input:{filename}")
            filepath = os.path.join(root, filename)
            digit_img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_COLOR)
            digit_img = cv2.cvtColor(digit_img, cv2.COLOR_BGR2GRAY)
            chars_train.append(digit_img)
            chars_label.append(root_int)

    # 将图片进行矫正
    chars_train = list(map(deskew, chars_train))
    # 提取hog特征
    chars_train = preprocess_hog(chars_train)
    chars_label = np.array(chars_label)
    # 训练模型
    model.train(chars_train, cv2.ml.ROW_SAMPLE, chars_label)

    # 如果路径下没有模型，那么保存，如果有，那就打印"model already exists"
    if not os.path.exists(os.path.join("model/", "svm.dat")):
        model.save(os.path.join("model/", "svm.dat"))
    else:
        print("model already exists")

    # 加载SVM模型，训练中文
    modelchinese = cv2.ml.SVM_create()
    modelchinese.setGamma(0.5)
    modelchinese.setC(1)
    modelchinese.setKernel(cv2.ml.SVM_RBF)
    modelchinese.setType(cv2.ml.SVM_C_SVC)

    chars_train = []
    chars_label = []
    # 注意：数据集的路径需要按照自己的实际路径做修改 
    for root, dirs, files in os.walk("./Train/charsChinese"):
        if not os.path.basename(root).startswith("zh_"):
            continue
        pinyin = os.path.basename(root)
        index = provinces.index(pinyin) + 1000 + 1  # 1是拼音对应的汉字
        # 读取字母和数字的图片数据，并转换为灰度图，读取文件名作为标签
        for filename in files:
            filepath = os.path.join(root, filename)
            digit_img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_COLOR)
            digit_img = cv2.cvtColor(digit_img, cv2.COLOR_BGR2GRAY)
            chars_train.append(digit_img)
            chars_label.append(index)

    # 将图片进行矫正
    chars_train = list(map(deskew, chars_train))
    # 提取hog特征
    chars_train = preprocess_hog(chars_train)
    chars_label = np.array(chars_label)
    # 训练模型
    modelchinese.train(chars_train, cv2.ml.ROW_SAMPLE, chars_label)

    # 如果路径下没有模型，那么保存，如果有，那就打印"model already exists"
    if not os.path.exists(os.path.join("model/", "svmchinese.dat")):
        modelchinese.save(os.path.join("model/", "svmchinese.dat"))
    else:
        print("model already exists")
