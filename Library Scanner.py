import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# initiate id counter
id = 0

# names related to ids: example ==> id 1 is Rushal, id 2 is Librarian, etc
# Note: You must update this list manually to match the IDs you used in Step 1
names = ['None', 'Rushal', 'Librarian', 'Student_3', 'Student_4', 'Student_5'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

print("Starting Library Scanner...")
print("Press 'ESC' to quit.")

while True:
    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less than 100 ==> "0" is perfect match 
        if (confidence < 100):
            name = names[id]
            confidence_text = "  {0}%".format(round(100 - confidence))
            
            # --- LIBRARY LOGIC HERE ---
            if name == "Librarian":
                 cv2.putText(img, "ACCESS GRANTED: ADMIN", (x+5,y-25), font, 0.5, (0,255,0), 2)
            else:
                 cv2.putText(img, "Student Access Only", (x+5,y-25), font, 0.5, (255,255,0), 2)
            # --------------------------
            
        else:
            name = "unknown"
            confidence_text = "  {0}%".format(round(100 - confidence))
            cv2.putText(img, "LOCKED", (x+5,y-25), font, 0.5, (0,0,255), 2)
        
        cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
        
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()