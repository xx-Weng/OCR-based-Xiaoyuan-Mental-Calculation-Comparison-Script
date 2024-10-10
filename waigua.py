

import cv2
import pytesseract
import numpy as np
import re
import pyautogui
import time
import threading
from threading import Thread, Lock
import pynput
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener
 
# 如果 Tesseract 没有在环境变量中，设置 Tesseract 可执行文件的路径
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"
 
# 初始化鼠标控制器
mouse = Controller()
 
# 定义绘图函数，并限制在0.1秒左右完成
def draw_symbol(symbol):
    start_time = time.time()  # 记录开始时间
 
    screen_width, screen_height = pyautogui.size()
    x = int(screen_width * 0.5)   # 水平居中
    y = int(screen_height * 0.8)  # 将 y 坐标设置为屏幕高度的 80%，向下移动绘图位置
    duration = 0.01  # 每条线的持续时间，设定为0.05秒以保持绘制时间大约为0.1秒
 
    if symbol == '>':
        # 绘制 "<" 符号
        mouse.position = (x, y)
        mouse.press(Button.left)
        mouse.move(-screen_width * 0.03, screen_height * 0.03)  # 左下斜线
        time.sleep(duration)
        mouse.release(Button.left)
        mouse.position = (x, y)
        mouse.press(Button.left)
        mouse.move(-screen_width * 0.03, -screen_height * 0.03)  # 左上斜线
        time.sleep(duration)
        mouse.release(Button.left)
    elif symbol == '<':
        # 绘制 ">" 符号
        mouse.position = (x, y)
        mouse.press(Button.left)
        mouse.move(screen_width * 0.03, screen_height * 0.03)  # 右下斜线
        time.sleep(duration)
        mouse.release(Button.left)
        mouse.position = (x, y)
        mouse.press(Button.left)
        mouse.move(screen_width * 0.03, -screen_height * 0.03)  # 右上斜线
        time.sleep(duration)
        mouse.release(Button.left)
    elif symbol == '=':
        # 绘制 "=" 符号
        mouse.position = (x - screen_width * 0.015, y - screen_height * 0.01)
        mouse.press(Button.left)
        mouse.move(screen_width * 0.03, 0)  # 第一条横线
        time.sleep(duration)
        mouse.release(Button.left)
        mouse.position = (x - screen_width * 0.015, y + screen_height * 0.01)
        mouse.press(Button.left)
        mouse.move(screen_width * 0.03, 0)  # 第二条横线
        time.sleep(duration)
        mouse.release(Button.left)
    else:
        print("无法绘制该符号")
 
    end_time = time.time()  # 记录结束时间
    print(f"绘图 '{symbol}' 完成，耗时: {end_time - start_time:.4f} 秒")
 
# 全局变量
running = False  # 标志变量，控制任务的运行
lock = Lock()  # 定义锁
 
def process_questions():
    global running
    i = 0
    previous_result = None
    previous_numbers = (None, None)  # 新增，用于存储前一题的数字
    stable_count = 0
    stable_threshold = 1  # 可以将阈值设为1，因为我们已经检测题目变化
 
    while running:
        start_time = time.time()  # 开始时间
        
        # 获取屏幕截图
        screenshot_start_time = time.time()
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        screenshot_end_time = time.time()
 
        print(f"截图耗时: {screenshot_end_time - screenshot_start_time:.4f} 秒")
 
        # 提取需要识别的区域（根据实际情况调整坐标）
        roi = image[420:640, 1050:1500]  # 请根据实际的数字位置调整
 
        # 图像预处理
        processing_start_time = time.time()
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi_contrast = cv2.convertScaleAbs(roi_gray, alpha=2.0, beta=0)  # 增强对比度
        roi_blur = cv2.GaussianBlur(roi_contrast, (5, 5), 0)
        _, roi_thresh = cv2.threshold(roi_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processing_end_time = time.time()
 
        print(f"图像处理耗时: {processing_end_time - processing_start_time:.4f} 秒")
 
        # OCR 识别
        ocr_start_time = time.time()
        custom_config = r'--oem 3 --psm 6'
        roi_text = pytesseract.image_to_string(roi_thresh, config=custom_config)
        ocr_end_time = time.time()
 
        print(f"OCR 识别耗时: {ocr_end_time - ocr_start_time:.4f} 秒")
 
        # 提取数字并判断大小
        matches = re.findall(r'\d+', roi_text)
 
        if len(matches) >= 2:
            num1, num2 = int(matches[0]), int(matches[1])
            print(f"第{i+1}题识别到的数字：{num1}, {num2}")
 
            # 检查是否为新题目
            if (num1, num2) == previous_numbers:
                print("检测到重复的题目，跳过处理")
            else:
                # 更新前一题的数字
                previous_numbers = (num1, num2)
 
                # 判断大小
                if num1 < num2:
                    result = '<'
                elif num1 > num2:
                    result = '>'
                else:
                    result = '='
                print(f"判断结果：{num1} {result} {num2}")
 
                # 绘制符号
                draw_start_time = time.time()
                # 启动绘图线程
                draw_thread = Thread(target=draw_symbol, args=(result,))
                draw_thread.start()
                draw_thread.join()  # 等待绘图完成
                draw_end_time = time.time()
                time.sleep(0.3)
                print(f"绘图耗时: {draw_end_time - draw_start_time:.4f} 秒")
 
        else:
            print(f"第{i+1}题未能识别出足够的数字")
 
        # 等待一小段时间以确保下一题加载
        i += 1
        end_time = time.time()
        print(f"第{i}题处理总耗时: {end_time - start_time:.4f} 秒\n")
 
def toggle_running(key):
    global running
    if key == pynput.keyboard.Key.enter:
        if not running:
            running = True
            print("任务已启动")
            # 启动处理线程
            t = threading.Thread(target=process_questions)
            t.start()
        else:
            running = False
            print("任务已停止")
 
# 监听键盘输入
with Listener(on_press=toggle_running) as listener:
    listener.join()
