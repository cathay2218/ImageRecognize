import cv2
import dlib
import imutils

#==================================PreDefine Section==================================
RootDir = r"D:\ImageRecognize\GitHub\Sample"
ImageName = ""
HOGFile = ""        #(Histogram of Oriented Gradient, HOG)
#==================================PreDefine Section==================================

#Import Image via OpenCV
img = cv2.imread("D:\ImageRecognize\wheelchair_Sample2.jpg")

#Declare dlib Component with Trainning Result
detector = dlib.simple_object_detector(r"C:\aa\output.svm")

#Run Image Detect
#Parameter: 
#Output: Enum Result
result = detector(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

for d in result:
    #Take Effective Range from Enumerator
    x1 = d.left()
    y1 = d.top()
    x2 = d.right()
    y2 = d.bottom()
    
    #Draw Rectangle and Show Score, Face Direction Sub-Detector Index Tag
    #cv2.rectangle(Image, Orig Coordinate, Oppo-Side Coordinate, Color(BGR), Line Width, Line Kind)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 10, cv2.LINE_AA)

#Downsize
img = imutils.resize(img, width=720)

#Create ImageWindow and Show Image
cv2.imshow("Object Detection", img)

#Waiting for AnyKey to Exit Program
cv2.waitKey(0)
cv2.destroyAllWindows()