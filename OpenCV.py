import cv2
import dlib
import imutils

FeaturePoints = True

#Import Image via OpenCV
img = cv2.imread("D:\Python\SampleImage.jpg")

if FeaturePoints:
    #According to Method: shape_predictor, Load 68 Feature Points Model, this Method is for Faces Emotion Detect
    predictor = dlib.shape_predictor("D:\Python\shape_predictor_68_face_landmarks.dat")

#Declare dlib Component
detector = dlib.get_frontal_face_detector()

#Run Image Detect
#Parameter: Source, Unsample(if Image too Small, Set this Parameter to 1), Detect Threshold
#Output: Enum Result, Detect Score, Face Direction Sub-Detector Index
face_rects, scores, idx = detector.run(img, 0, 0)

for i, d in enumerate(face_rects):
    #Take Effective Range from Enumerator
    x1 = d.left()
    y1 = d.top()
    x2 = d.right()
    y2 = d.bottom()
    #Take Score and Face Direction Sub-Detector Index from Enumerator
    text = "%2.2f(%d)" % (scores[i], idx[i])

    #Draw Rectangle and Show Score, Face Direction Sub-Detector Index Tag
    #cv2.rectangle(Image, Orig Coordinate, Oppo-Side Coordinate, Color(BGR), Line Width, Line Kind)
    #cv2.putText(Image, Text, Text Coordinate, Font, Size, Color(BGR), Line Width, Line Kind)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 10, cv2.LINE_AA)
    cv2.putText(img, text, (x1, y1-15), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 255, 255), 1, cv2.LINE_AA)

    if FeaturePoints:    
        #Get Trans-Color Frame for Feature Points
        landmarks_frame = cv2.cvtColor(img, cv2. COLOR_BGR2RGB)
        #Find Feature Points Position
        shape = predictor(landmarks_frame, d)
        #Draw Feature Points
        for i in range(68):
            cv2.circle(img,(shape.part(i).x,shape.part(i).y), 3,( 0, 0, 255), 2)
            cv2.putText(img, str(i),(shape.part(i).x,shape.part(i).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
    
#Downsize
img = imutils.resize(img, width=960)

#Create ImageWindow and Show Image
cv2.imshow("Face Detection", img)

#Waiting for AnyKey to Exit Program
cv2.waitKey(0)
cv2.destroyAllWindows()