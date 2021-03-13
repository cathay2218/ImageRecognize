import os
import cv2
import numpy
import imutils
import time
#==================================PreDefine Section==================================
RootDir = r"D:\ImageRecognize\GitHub\Sample"
VideoName = ""
InputHorizontalFlip = False
Output_ReSizeWidth = 0      #Value is 0, Means Skip to Resize
ImageWidth = 1280
ImageHeight = 960
#==================================PreDefine Section==================================

#==================================Stream Source Define Section=======================
#Open Camera via Method: VideoCapture(Stream Address, File Path or Camera Index Start from 0)
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(os.path.join(RootDir, VideoName))
#cap = cv2.VideoCapture("rtsp://admin:9999@10.9.0.102:8557/PSIA/Streaming/channels/2?videoCodecType=H.264")
#==================================Stream Source Define Section=======================

#Get Stream Size
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('size:'+repr(size))

#Set Input Image Size
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, ImageWidth)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ImageHeight)

#Calc Image Area
#Area = ImageWidth * ImageHeight

#Initail Average Image
ret, frame = cap.read()
avg = cv2.blur(frame, (4, 4))
avg_float = numpy.float32(avg)

while(cap.isOpened()):
    #Take Frame from Camera
    ret, frame = cap.read()
    
    #Filp Image Horizontal
    if InputHorizontalFlip:
        frame = cv2.flip(frame, 1, dst = None)

    #When End of Stream, Exit Loop
    if ret == False:
        break

    #Fuzzy Image
    blur = cv2.blur(frame, (4, 4))

    #計算目前影格與平均影像的差異值
    diff = cv2.absdiff(avg, blur)

    #Transfer Image to GrayScale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    #篩選出變動程度大於門檻值的區域
    ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

    #使用型態轉換函數去除雜訊
    kernel = numpy.ones((5, 5), numpy.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    #Generate Contour Line
    cntImg, cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
    for c in cntImg:
        #Ignore those too Small Area
        if cv2.contourArea(c) < 10000:
            continue

        #Detect Activate Handle Section
        print (time.ctime(time.time()) + "  Motion Detect Activate!!")

        #Calculate Outter Rectangle of Contour Line
        (x, y, w, h) = cv2.boundingRect(c)

        #Draw Rectangle
        #cv2.rectangle(Image, Orig Coordinate, Oppo-Side Coordinate, Color(BGR), Line Width)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #Draw Contour Line (for Debug)
        #cv2.drawContours(frame, cntImg, -1, (0, 255, 255), 2)

    #Output Resize
    if Output_ReSizeWidth != 0:
        frame = imutils.resize(frame, width = Output_ReSizeWidth)

    #Create ImageWindow and Show Image
    cv2.imshow('Object Motion Detect', frame)

    #Waiting for Space Key to Leave Loop
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

    #Update Average Image
    cv2.accumulateWeighted(blur, avg_float, 0.01)
    avg = cv2.convertScaleAbs(avg_float)

#Release Memory and Exit Program
cap.release()
cv2.destroyAllWindows()