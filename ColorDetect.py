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

#image = cv2.imread(arg.input)
image = cv2.imread(r"D:\ImageRecognize\Github\Sample\HeatImageTest.jpg")                #for company path
#image = cv2.imread(r"D:\Python\GitHub\ImageRecognize\Sample\HeatImageTest.jpg")        #for home path

#要偵測的顏色範圍
lower = numpy.array([37, 174, 201])
upper = numpy.array([77, 274, 301])

#以HSV色彩空間模型抓取目標影像顏色範圍(簡化輸出為黑白遮罩二值圖)
filtered = cv2.inRange(image, lower, upper)
cv2.imshow('color mask_HSV Color Space', filtered)

#將HSV色彩空間黑白遮罩二值圖進行高斯模糊處理
#此為必須處理項目, 如未經過高斯模糊處理則輪廓搜索結果數會大幅上升且範圍會變零碎
blurred = cv2.GaussianBlur(filtered, (15, 15), 0)
cv2.imshow('color mask_GaussianBlur', blurred)

#尋找目標輪廓
(cnts, _) = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #輸入影像為高斯模糊的副本
print ("Matches Area Counts: " + str(len(cnts)))

#取全區域輪廓
for cnt in cnts:
    rect = numpy.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
    cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)     #描繪輪廓

#取單一輪廓
# if len(cnts) > 1:
#     cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]      #Sort by Contour Area, Ordey by DESC (reverse = True)

# # compute the (rotated) bounding box around then
# # contour and then draw it
# rect = numpy.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
# cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)


#Show Image and Wait Any Key to Exit Program
cv2.imshow("Color Tracking", image)
cv2.waitKey(0)
cv2.destroyAllWindows()