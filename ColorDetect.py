import cv2
import numpy

image = cv2.imread(r"D:\Python\GitHub\ImageRecognize\Sample\HeatImageTest.jpg")

#偵測顏色範圍
lower = numpy.array([37, 174, 201])
upper = numpy.array([77, 274, 301])

filtered = cv2.inRange(image, lower, upper)
#高斯模糊
blurred = cv2.GaussianBlur(filtered, (15, 15), 0)

# find contours in the image
(cnts, _) = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#取全區域
# print ("Matches: " + str(len(cnts)))
# for cnt in sorted(cnts, key = cv2.contourArea, reverse = True):
#     rect = numpy.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
#     cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)

#取單一區域
if len(cnts) > 0:
    print ("Matches: " + str(len(cnts)))
    cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

# compute the (rotated) bounding box around then
# contour and then draw it
rect = numpy.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)


#Show Image and Wait Any Key to Exit Program
cv2.imshow("Tracking", image)
cv2.waitKey(0)
cv2.destroyAllWindows()