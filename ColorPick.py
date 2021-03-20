import cv2
import numpy

#Sub Function: 滑鼠左鍵KeyDownEvent
def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixelColor = image[y,x]      #Get Single Px's Color(Return Value [BGR] Array)
        
        #取得顏色範圍(含offset), 並用numpy.array組成陣列
        upper = numpy.array([pixelColor[0] + 20, pixelColor[1] + 50, pixelColor[2] + 50])
        lower = numpy.array([pixelColor[0] - 20, pixelColor[1] - 50, pixelColor[2] - 50])
        print ("OriginalColor, Color Low Bound, Color Up Bound")
        print (pixelColor, lower, upper)

        image_mask = cv2.inRange(image,lower,upper)
        #cv2.imshow("mask",image_mask)

#Main Function
image = cv2.imread(r"D:\Python\GitHub\ImageRecognize\Sample\HeatImage.jpg") #320 x 240 px

#Show Image and Set Mouse Key Down Event
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', pick_color)
cv2.imshow("Image",image)

#Wait Next Mouse Key Down Event or Any Key to Exit Program
cv2.waitKey(0)
cv2.destroyAllWindows()