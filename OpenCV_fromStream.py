import cv2
import dlib
import imutils

FeaturePoints = False

#Open Camera via Method: VideoCapture(FileName or Camera Index Start from 0)
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("D:\Python\Sample_AVC_768Ks_720p_15fps.mp4")

if FeaturePoints:
    #According to Method: shape_predictor, Load 68 Feature Points Model, this Method is for Faces Emotion Detect
    predictor = dlib.shape_predictor("D:\Python\shape_predictor_68_face_landmarks.dat")

#Declare dlib Component
detector = dlib.get_frontal_face_detector()

#if Camera is Open, then Start Loop, until 'q' Key Pressed
while(cap.isOpened()):
    #Take Frame from Camera
    ret, frame = cap.read()
    #Filp Image Horizontal
    #frame = cv2.flip(frame, 1, dst = None)
    
    #Run Image Detect
    #Parameter: Source, Unsample(if Image too Small, Set this Parameter to 1), Detect Threshold
    #Output: Enum Result, Detect Score, Face Direction Sub-Detector Index
    face_rects, scores, idx = detector.run(frame, 0, 0)
    
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
        for i in range(68):
            cv2.circle(frame,(shape.part(i).x,shape.part(i).y), 3,( 0, 0, 255), 2)
            cv2.putText(frame, str(i),(shape.part(i).x,shape.part(i).y),cv2. FONT_HERSHEY_COMPLEX, 0.5,( 255, 0, 0), 1)
    
    #Downsize
    frame = imutils.resize(frame, width=960)

    #Create ImageWindow and Show Image
    cv2.imshow("Face Detection", frame)

    #Waiting for 'q' to Leave Loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Release Memory and Exit Program
cap.release()
cv2.destroyAllWindows()