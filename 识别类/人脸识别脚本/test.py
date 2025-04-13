import cv2
import time
import ctypes
import face_recognition
import os
import configparser
import pyautogui
import numpy as np
from pywinauto.keyboard import send_keys
from pywinauto import mouse
import logging
import random

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')
face_threshold = config.getfloat('recognition', 'threshold', fallback=0.6)
lock_timeout = config.getfloat('lock', 'timeout', fallback=30)
pin_code = config.get('unlock', 'pin', fallback='123456')

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wake_up_screen():
    try:
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        try:
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            ctypes.windll.user32.SetCursorPos(x, y)  # 移动鼠标到指定坐标
        except Exception as e:
            logging.error(f"[错误] 移动鼠标到指定坐标失败: {e}")
        try:
            ctypes.windll.user32.SetCursorPos(0, 0)  # 将鼠标返回到屏幕左上角
        except Exception as e:
            logging.error(f"[错误] 将鼠标返回到屏幕左上角失败: {e}")
        # 方法1：轻微移动鼠标
        x, y = pyautogui.position()  # ✅ 获取当前鼠标位置
        mouse.move(coords=(x + 1, y))
     
        mouse.move(coords=(x, y))

        # 方法2：发送 Shift 键作为备用触发
        send_keys('{VK_SHIFT}')
        logging.info("[提示] 已尝试唤醒屏幕")
    except Exception as e:
        logging.error(f"[错误] 唤醒屏幕失败: {e}")

# 加载本地人脸数据
known_face_encodings = []
known_face_names = []
known_faces_dir = os.path.join(os.path.dirname(__file__), 'faces')

for filename in os.listdir(known_faces_dir):
    try:
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
        encodings = face_recognition.face_encodings(image)
        if len(encodings) == 1:
            known_face_encodings.append(encodings[0])
            known_face_names.append(filename.split('.')[0])
        else:
            logging.warning(f"[跳过] {filename} 包含 {len(encodings)} 张人脸")
    except Exception as e:
        logging.error(f"[错误] 加载 {filename} 失败：{e}")

# 摄像头初始化
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def is_locked():
    return ctypes.windll.User32.GetForegroundWindow() == 0

def recognize_face(frame, known_face_encodings, known_face_names):
    locations = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, locations)
    for face_encoding in encodings:
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(distances)
        if distances[best_match_index] <= face_threshold:
            return known_face_names[best_match_index]
    return None

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [('wVk', ctypes.c_ushort),
                ('wScan', ctypes.c_ushort),
                ('dwFlags', ctypes.c_ulong),
                ('time', ctypes.c_ulong),
                ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    _fields_ = [('type', ctypes.c_ulong),
                ('ki', KEYBDINPUT)]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def send_key(vk_code):
    input_down = INPUT(type=1, ki=KEYBDINPUT(wVk=vk_code, wScan=0, dwFlags=0, time=0, dwExtraInfo=None))
    input_up = INPUT(type=1, ki=KEYBDINPUT(wVk=vk_code, wScan=0, dwFlags=0x0002, time=0, dwExtraInfo=None))
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(input_up))

def send_pin(pin):
    for digit in pin:
        send_key(0x30 + int(digit))  # 0x30 是 '0' 键的 VK 码
       
    send_key(0x0D)  # 回车键

if __name__ == '__main__':
    last_detected_time = time.time()
    logging.info("人脸识别系统已启动，等待识别...")

    # 如果不是管理员，则重新以管理员权限运行
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    while True:
        try:
            if is_locked():
                logging.info("系统处于锁屏状态，尝试识别人脸...")
                ret, frame = cap.read()
                if ret:
                    name = recognize_face(frame, known_face_encodings, known_face_names)
                    if name:
                        logging.info(f"识别到本人：{name}，自动解锁中...")
                        pyautogui.FAILSAFE = False
                        pyautogui.press("tab")
                        wake_up_screen()  # ✨ 调用唤醒
                     
                        send_pin(pin_code)
                        last_detected_time = time.time()
                      
                    else:
                        logging.info("未识别到本人，继续锁定")
            else:
                ret, frame = cap.read()
                if ret:
                    locations = face_recognition.face_locations(frame)
                    if locations:
                        name = recognize_face(frame, known_face_encodings, known_face_names)
                        if name:  # 本人时保持唤醒
                            last_detected_time = time.time()
                            logging.info(f"识别到本人：{name}，保持唤醒状态")
                        else:  # 不是本人时保持锁定
                            logging.info("未识别到本人，保持锁定")
                    elif time.time() - last_detected_time > lock_timeout:
                        logging.info("长时间无人，自动锁屏")
                        ctypes.windll.user32.LockWorkStation()
                        last_detected_time = time.time()

          

        except Exception as e:
            logging.error(f"[错误] {e}")
       