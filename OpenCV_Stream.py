import os
import cv2
import dlib
import imutils

#==================================PreDefine Section==================================
RootDir = r"D:\ImageRecognize\GitHub\Sample"
VideoName = "Sample_AVC_768Ks_720p_15fps.mp4"
LandMarksName = "shape_predictor_68_face_landmarks.dat"
InputHorizontalFlip = False
FeaturePoints = False
DetectAccuracyThreshold = -0.3
Output_ReSizeWidth = 0      #Value is 0, Means Skip to Resize
#==================================PreDefine Section==================================

#==================================Stream Source Define Section=======================
#Open Camera via Method: VideoCapture(Stream Address, File Path or Camera Index Start from 0)
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(os.path.join(RootDir, VideoName))
#cap = cv2.VideoCapture("rtsp://admin:9999@10.9.0.102:8557/PSIA/Streaming/channels/2?videoCodecType=H.264")
#==================================Stream Source Define Section=======================

if FeaturePoints:
    #According to Method: shape_predictor, Load 68 Feature Points Model, this Method is for Faces Emotion Detect
    predictor = dlib.shape_predictor(os.path.join(RootDir, LandMarksName))

#Declare dlib Component
detector = dlib.get_frontal_face_detector()

#if Camera is Open, then Start Loop until to End of Stream or Space Key Pressed
while(cap.isOpened()):
    #Take Frame from Camera
    ret, frame = cap.read()
    
    #Filp Image Horizontal
    if InputHorizontalFlip:
        frame = cv2.flip(frame, 1, dst = None)
       
    #Run Image Detect
    #Parameter: Source, Unsample(if Image too Small, Set this Parameter to 1, and it will Decrease FPS), Detect Threshold
    #Output: Enum Result, Detect Score, Face Direction Sub-Detector Index
    face_rects, scores, idx = detector.run(frame, 0, DetectAccuracyThreshold)
    
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
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)
        cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

        if FeaturePoints:    
            #Get Trans-Color Frame for Feature Points
            landmarks_frame = cv2.cvtColor(frame, cv2. COLOR_BGR2RGB)
            #Find Feature Points Position
            shape = predictor(landmarks_frame, d)
            #Draw Feature Points
            for j in range(68):
                cv2.circle(frame,(shape.part(j).x,shape.part(j).y), 3,( 0, 0, 255), 2)
                cv2.putText(frame, str(j),(shape.part(j).x,shape.part(j).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
    
    #Output Resize
    if Output_ReSizeWidth != 0:
        frame = imutils.resize(frame, width = Output_ReSizeWidth)

    #Create ImageWindow and Show Image
    cv2.imshow("Face Detection", frame)

    #Waiting for Space Key to Leave Loop
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

#Release Memory and Exit Program
cap.release()
cv2.destroyAllWindows()