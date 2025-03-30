import cv2

if __name__ == "__main__":
    path = "./demo.png"
    try:
        image_np = cv2.imread(path)
        (h, w, _) = image_np.shape
        x_min, x_max = 150, 270
        y_min, y_max = 150, 290
        if not (((x_min >= 0) and (x_max <= w)) and ((y_min >= 0) and (y_max <= h))):
            raise OverflowError("x_min, x_max, y_min, y_max is overflow!")
        img_rec = cv2.rectangle(image_np, (x_min - 2, y_min - 2), (x_max + 2, y_max + 2), (0, 0, 255), 2)
        # 提取目标中的感兴趣区域
        ROI_img = image_np[y_min: y_max, x_min: x_max]
        cv2.imshow("ROI_img", ROI_img)
        cv2.waitKey(0)
    except Exception as e:
        # 返回出错内容
        print({"return": "error", "error_result": str(e)})
