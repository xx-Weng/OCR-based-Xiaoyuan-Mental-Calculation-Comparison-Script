

# 基于OCR的小猿口算比大小脚本

@花未央心流 2024.10.10

Reference: https://blog.csdn.net/qq_18813685/article/details/142819750





## 环境准备

1. 安装 pytesseract
  https://github.com/UB-Mannheim/tesseract/wiki

2. 环境配置：你的环境应该有以下包

```python
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
```

cv2 是 OpenCV 库的一部分，直接pip可能查不到，可以使用以下命令：
```
pip install opencv-python
```





## 运行方式

1. 下载 mumu12（安卓模拟器，google即可）
2. 打开mumu12，下载chrome，在chrome中下载正版小猿口算
3. 打开小猿口算 - pk - 比大小模块
4. 运行 waigua.py (命令：cd 到 .py 所在文件夹，输入 python waigua.py)



## 注意事项

1. 按下回车键（Enter）运行和暂停程序
2. 第146行		time.sleep(0.3)		数字 0.3 自行修改到程序能稳定运行
3. 第  96行		roi = image[420:640, 1050:1500]  420:640, 1050:1500 是题目在你电脑上的实际位置，自行修改