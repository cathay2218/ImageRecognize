import cv2
import numpy
import argparse

#Argument Input via Command Prompt
parser = argparse.ArgumentParser()
parser.add_argument('-input', type = str, help = 'Image Path for Detect Color')
parser.add_argument('-lowerColor', type = str, help = 'Lower Detect Color Bound [B, G, R]')
parser.add_argument('-upperColor', type = str, help = 'Upper Detect Color Bound [B, G, R]')

arg = parser.parse_args()
print (arg)

#=====================================================================================

#cap = cv2.VideoCapture(arg.input)
cap = cv2.VideoCapture("rtsp://admin:9999@10.9.0.102:8557/PSIA/Streaming/channels/2?videoCodecType=H.264")


#要偵測的顏色範圍[B,G,R]
lower = numpy.array([245, 245, 245])
upper = numpy.array([255, 255, 255])

while(cap.isOpened()):
    #Take Frame from Camera
    ret, frame = cap.read()
    
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
    
    #取全區域輪廓, 並描繪
    for cnt in cnts:
        rect = numpy.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))     #輪廓矩形四角座標點
        cv2.drawContours(frame, [rect], -1, (0, 255, 0), 2)         #描繪輪廓

    cv2.imshow("Color Tracking", frame)
    
    #Waiting for Space Key to Leave Loop
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

#Release Memory and Exit Program
cap.release()
cv2.destroyAllWindows()