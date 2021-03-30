# python ColorDetect_Stream.py -input rtsp://admin:9999@10.9.0.102:8557/PSIA/Streaming/channels/2?videoCodecType=H.264
# python ColorDetect_Stream.py -input screen -saveVideo True
# python ColorDetect_Stream.py -input screen -saveVideo true -windowTitle 小算盤

import cv2
import time
import numpy
import argparse
import win32gui
from PIL import ImageGrab

#Argument Input via Command Prompt
parser = argparse.ArgumentParser()
parser.add_argument('-input', type = str, help = 'Image Path for Detect Color')
parser.add_argument('-lowerColor', type = str, help = 'Lower Detect Color Bound [B, G, R]')
parser.add_argument('-upperColor', type = str, help = 'Upper Detect Color Bound [B, G, R]')
parser.add_argument('-saveVideo', type = str, help = 'Save Image to Video File')
parser.add_argument('-windowTitle', type = str, help = 'Window Title for Screen Capture')

arg = parser.parse_args()
print (arg)

#要偵測的顏色範圍[B,G,R]
lower = numpy.array([245, 245, 245])
upper = numpy.array([255, 255, 255])

#輸入參數==============================================================================
saveVideo = arg.saveVideo                                           #bool: 是否將影像儲存為檔案
windowTitle = win32gui.FindWindow(None, arg.windowTitle)            #螢幕擷取模式: 目標視窗

#輸入串流==============================================================================
if not arg.input == 'screen':
    #cap = cv2.VideoCapture("rtsp://admin:9999@10.9.0.102:8557/PSIA/Streaming/channels/2?videoCodecType=H.264")
    cap = cv2.VideoCapture(arg.input)

#==============================================================================
#Video 存檔僅能開一檔
#RTSP or File Record
if saveVideo and not arg.input == 'screen':
    #(輸出檔名, 編碼方式, FPS, FrameSize, 彩色)
    out = cv2.VideoWriter('output_{0}.mp4'.format(time.strftime("%Y%m%d_%H%M%S", time.localtime())), cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))), True)
#Screen Record
elif saveVideo:
    left, top, right, bot = win32gui.GetWindowRect(windowTitle)             #找出目標視窗矩形範圍
    width = right - left                                                    #Get Window width
    height = bot - top                                                      #Get Window height
    out = cv2.VideoWriter('output_{0}.mp4'.format(time.strftime("%Y%m%d_%H%M%S", time.localtime())), cv2.VideoWriter_fourcc(*'mp4v'), 30, (int(width), int(height)), True)

#MainFunction=========================================================================
while(True):
    #Screen Record
    if arg.input == 'screen':
        try:
            left, top, right, bot = win32gui.GetWindowRect(windowTitle)             #找出目標視窗矩形範圍
            img = ImageGrab.grab(bbox = (left, top, right, bot))                    #抓取矩形範圍影像
            frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2RGB)               #將來源矩形影像自BGR色彩模式轉為RGB模式    
        except:
            print ("Can't captrue window (external program end?). Exiting ...")
    #RTSP or File Record
    else:
        #Take Frame from Stream
        ret, frame = cap.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
    
    #以HSV色彩空間模型抓取目標影像顏色範圍(簡化輸出為黑白遮罩二值圖)
    filtered = cv2.inRange(frame, lower, upper)
    #cv2.imshow('color mask_HSV Color Space', filtered)
    
    #將HSV色彩空間黑白遮罩二值圖進行高斯模糊處理
    #此為必須處理項目, 如未經過高斯模糊處理則輪廓搜索結果數會大幅上升且範圍會變零碎
    blurred = cv2.GaussianBlur(filtered, (15, 15), 0)
    #cv2.imshow('color mask_GaussianBlur', blurred)
    
    #尋找目標輪廓
    (cnts, _) = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #輸入影像為高斯模糊的副本
    #print ("Matches Area Counts: " + str(len(cnts)))
    
    #取所有輪廓, 並描繪
    for cnt in cnts:
        rect = numpy.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))     #輪廓矩形四角座標點
        cv2.drawContours(frame, [rect], -1, (0, 255, 0), 2)         #描繪輪廓
    
    cv2.imshow("Color Tracking", frame)
    
    if saveVideo:
        out.write(frame)
    
    #Waiting for Space Key to Leave Loop
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

#Release Memory and Exit Program
if saveVideo:
    out.release()
    
cap.release()
cv2.destroyAllWindows()