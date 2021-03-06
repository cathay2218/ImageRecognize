# 紅色色塊辨識 + 存圖  ->  python ColorDetect_Stream.py -input D:\ImageRecognize\Video\00269.MTS -savePicture=true
#                         python ColorDetect_Stream.py -input D:\ImageRecognize\Video\00270.MTS -savePicture=true

# 軌旁22KV 黃色       ->   python ColorDetect_Stream.py -input D:\ImageRecognize\Video\0520.mp4 -savePicture=true
#python ColorDetect_Stream.py -input D:\ImageRecognize\Video\0520.mp4 -savePicture=true -detectSection=4


# python ColorDetect_Stream.py -input rtsp://admin:9999@10.9.0.102:8557/PSIA/Streaming/channels/2?videoCodecType=H.264
# python ColorDetect_Stream.py -input screen -saveVideo True
# python ColorDetect_Stream.py -input screen -saveVideo true -windowTitle 小算盤

import os
import sys
import cv2
import numpy
import imutils
import argparse
import win32gui
from PIL import ImageGrab
from datetime import datetime

#函式區段==============================================================================
def reginCheck():       #True = 顯示目標輪廓
    try:                                                                                    #嘗試將參數轉為int, 如無法轉換則跳脫函式(視同不偵測目標輪廓分區位置)
        reginSection = int(arg.detectSection)
    except:
        return True
        
    margin_x = width / 2
    margin_y = height / 2
    coordinate1 = rect[0]
    coordinate2 = rect[1]
    coordinate3 = rect[2]
    coordinate4 = rect[3]
    
    if (arg.showSectionLine and reginSection >= 1 and reginSection <= 4):                   #是否描繪區間分割線
        cv2.line(frame, (int(margin_x), 0), (int(margin_x), height), (255, 0, 0), 2)        #垂直分割線
        cv2.line(frame, (0, int(margin_y)), (width, int(margin_y)), (255, 0, 0), 2)         #水平分割線
        
    #判斷目標輪廓是否在偵測需求區(平均四分割[左上, 右上, 左下, 右下])
    if (reginSection == 1):
        if (coordinate3[0] < width / 2) and (coordinate4[0] < width / 2) and (coordinate1[1] < height / 2) and (coordinate4[1] < height / 2):
            return True
    elif (reginSection == 2):
        if (coordinate1[0] > width / 2) and (coordinate2[0] > width / 2) and (coordinate1[1] < height / 2) and (coordinate4[1] < height / 2):
            return True
    elif (reginSection == 3):
        if (coordinate3[0] < width / 2) and (coordinate4[0] < width / 2) and (coordinate2[1] > height / 2) and (coordinate3[1] > height / 2):
            return True
    elif (reginSection == 4):
        if (coordinate1[0] > width / 2) and (coordinate2[0] > width / 2) and (coordinate2[1] > height / 2) and (coordinate3[1] > height / 2):
            return True
    else:   #參數值非1~4, 視同不偵測目標輪廓分區位置
        return True

#Argument Input via Command Prompt=====================================================
parser = argparse.ArgumentParser()
parser.add_argument('-input', type = str, help = 'Image Path for Detect Color')
parser.add_argument('-lowerColor', type = str, help = 'Lower Detect Color Bound [B, G, R]')
parser.add_argument('-upperColor', type = str, help = 'Upper Detect Color Bound [B, G, R]')
parser.add_argument('-saveVideo', type = str, help = 'Save Image to Video File')
parser.add_argument('-windowTitle', type = str, help = 'Window Title for Screen Capture')
parser.add_argument('-detectSection', type = str, help = 'Set Detect Section (Section 1~4, None for All Section)')
parser.add_argument('-showSectionLine', type = str, help = 'Show Section Separate Line on Canvas')
parser.add_argument('-savePicture', type = str, help = 'Save Picture, if Target Color Detected')

Output_ReSizeWidth = 1200      #Value is 0, Means Skip to Resize

arg = parser.parse_args()
print (arg)

#要偵測的顏色範圍[B,G,R]
#22KV TragetColor = 100, 180, 160
# 軌旁22KV(黃色色塊)  [※會辨識到較多的彩虹橋塗裝]   offset = +/- 20
# lower = numpy.array([80, 160, 140])
# upper = numpy.array([120, 200, 180])

# 軌旁22KV(黃色色塊)  [※會辨識到少許彩虹橋塗裝] offset = +/- 15       >>>>> OK
lower = numpy.array([85, 165, 145])
upper = numpy.array([115, 195, 175])

# 軌旁22KV(黃色色塊)  [※較不會辨識到彩虹橋塗裝]   offset = +/- 10, 其中 blue +/- 5
# lower = numpy.array([95, 170, 150])
# upper = numpy.array([105, 190, 170])

# 推車(紅色色塊)Target = 70, 60, 120   offset = +/- 20       >>>>> OK
# lower = numpy.array([50, 40, 100])
# upper = numpy.array([90, 80, 140])

saveVideo = arg.saveVideo                                           #bool: 是否將影像儲存為檔案
savePicture = arg.savePicture                                       #bool: 是否於偵測到目標顏色時儲存截圖
showSectionLine = arg.showSectionLine                               #bool: 是否描繪區間分隔線
windowTitle = win32gui.FindWindow(None, arg.windowTitle)            #螢幕擷取模式: 目標視窗

#輸入串流==============================================================================
if not arg.input == 'screen':
    #cap = cv2.VideoCapture("rtsp://admin:9999@10.9.0.102:8557/PSIA/Streaming/channels/2?videoCodecType=H.264")
    if arg.input == '0':                                            #內建鏡頭(cv2.VideoCapture(0))，須將arg input string 換型為 int
        cap = cv2.VideoCapture(int(arg.input))
    else:                                                           #檔案或RSTP串流，維持string type
        cap = cv2.VideoCapture(arg.input)
    
    #檢查串流是否存在(timeout需一段時間)
    ret, _ = cap.read()
    if not ret:
        print("Can't receive frame (stream exist?). Exiting ...")
        sys.exit()

#==============================================================================
#Video 存檔僅能開一檔
#RTSP or File Record
if saveVideo and not arg.input == 'screen':
    #(輸出檔名, 編碼方式, FPS, FrameSize, 彩色)
    out = cv2.VideoWriter('output_{0}.mp4'.format(datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")), cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))), True)
#Screen Record
elif saveVideo:
    try:
        left, top, right, bot = win32gui.GetWindowRect(windowTitle)             #找出目標視窗矩形範圍
    except:
        print ("Can't captrue window (external program end?). Exiting ...")     #當無任何目標視窗可供抓取時，結束程式
        sys.exit()
    width = right - left                                                    #Get Window width
    height = bot - top                                                      #Get Window height
    out = cv2.VideoWriter('output_{0}.mp4'.format(datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")), cv2.VideoWriter_fourcc(*'mp4v'), 30, (int(width), int(height)), True)

#MainFunction=========================================================================
while(True):
    #Screen Source
    if arg.input == 'screen':
        try:
            left, top, right, bot = win32gui.GetWindowRect(windowTitle)             #找出目標視窗矩形範圍
            img = ImageGrab.grab(bbox = (left, top, right, bot))                    #抓取矩形範圍影像
            frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2RGB)               #將來源矩形影像自BGR色彩模式轉為RGB模式       
            width = right - left                                                    #Get Window width
            height = bot - top                                                      #Get Window height
        except:
            print ("Can't captrue window (external program end?). Exiting ...")
            break
    #RTSP or File Source
    else:
        #Take Frame from Stream
        ret, frame = cap.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
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
        rect = numpy.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))     #取輪廓矩形四角座標點
        if reginCheck():                                            #確認結果是否在偵測需求區域
            cv2.drawContours(frame, [rect], -1, (0, 255, 0), 2)     #描繪輪廓
    
    #Show Resize
    if Output_ReSizeWidth != 0:
        frame_show = imutils.resize(frame, width = Output_ReSizeWidth)
    else:
        frame_show = frame
        
    cv2.imshow("Color Tracking", frame_show)                             #顯示偵測結果
    
    #當有偵測標的顏色出現時、符合偵測區域且有開啟存檔功能，則儲存圖片
    if savePicture and len(cnts) > 0 and reginCheck():
        if not os.path.isdir('.\DetectedPicture'):                  #當存檔資料夾不存在時，建立資料夾
            print ('Depository Path not Exist, Create!')
            os.makedirs('.\DetectedPicture')

        cv2.imwrite('DetectedPicture\ScreenShot_{0}.png'.format(datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S.%f")), frame)   #儲存偵測結果
            
    if saveVideo:                                                   #儲存影像至mp4檔
        out.write(frame)
    
    #Waiting for Space Key to Leave Loop
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

#Release Memory and Exit Program
if saveVideo:                           #當有進行錄影存檔，結束程式時需釋放cv2.VideoWriter資源
    out.release()
    
if not arg.input == 'screen':           #當來源非螢幕擷取，結束程式時需釋放cv2.VideoCapture資源
    cap.release()
    
cv2.destroyAllWindows()                 #釋放所有圖形視窗資源