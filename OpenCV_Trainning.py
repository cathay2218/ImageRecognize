from __future__ import print_function
import dlib
import argparse
from skimage import io
from imutils import paths
import imutils
from scipy.io import loadmat

#Read Argument
#ap = argparse.ArgumentParser()
#ap.add_argument("-c", "--class", required=True, help="Path to the CALTECH-101 class images")
#ap.add_argument("-a", "--annotations", required=True, help="Path to the CALTECH-101 class annotations")
#ap.add_argument("-o", "--output", required=True, help="Path to the output detector")
#args = vars(ap.parse_args())

#==================================PreDefine Section==================================
SampleImagePath = r"C:\aa\wheelchair_image"
AnnotationsPath = r"C:\aa\wheelchair_annotations"
HOG_OutputPath = r"C:\aa\output.svm"
#==================================PreDefine Section==================================

images = [] #存放相片圖檔
boxes = [] #存放Annotations

options = dlib.simple_object_detector_training_options()
options.add_left_right_images_filps = False   #非對稱物體
options.C = 5                       #比對值
options.epsilon = 0.001

#依序處理path下的每張圖片
for imagePath in paths.list_images(SampleImagePath):
    #從圖片路徑名稱中取出ImageID
    imageID = imagePath[imagePath.rfind("\\") + 1:].split("_")[1]
    imageID = imageID.replace(".jpg", "")
    #載入Annotation
    p = r"{}\annotation_{}.mat".format(annotationsPath, imageID)
    annotations = loadmat(p)["box_coord"]
    
#取出annotations資訊繪成矩形物件，放入boxes變數中。
    bb = [dlib.rectangle(left=int(x), top=int(y), right=int(w), bottom=int(h))for (y, h, x, w) in annotations]
    boxes.append(bb)
 
#將圖片放入images變數
    images.append(io.imread(imagePath))

#---------------------------------------------------------------------

#丟入三個參數開始訓練
print("[INFO] training detector...")
detector = dlib.train_simple_object_detector(images, boxes, options)
 
# 將訓練結果匯出到檔案
print("[INFO] dumping classifier to file...")
detector.save(outputPath)

#Show Histogram of Oriented Gradients Graphic
win = dlib.image_window()
win.set_image(detector)
dlib.hit_enter_to_continue()