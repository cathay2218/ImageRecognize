from PIL import ImageGrab
import numpy
import cv2
import win32gui
 
windowTitle = win32gui.FindWindow(None, '小算盤')

while True:
    try :
        left, top, right, bot = win32gui.GetWindowRect(windowTitle)
    except :
        print("找不到視窗")
        break
    
    img = ImageGrab.grab(bbox = (left, top, right, bot))
    
    frame = numpy.array(img)
    
    #frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2GRAY)
    cv2.imshow("screen box", frame)
        
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cv2.destroyAllWindows()