import numpy as np
import cv2
import pickle
from firebase import firebase
from datetime import datetime

firebase = firebase.FirebaseApplication('https://proje-yuztanima.firebaseio.com')

face_cascade = cv2.CascadeClassifier(r"C:\Users\mhmte\Desktop\staj\FaceRecognition\yuzler.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
   og_labels = pickle.load(f)
   labels = {v:k for k,v in og_labels.items()}
    
cap = cv2.VideoCapture(0)

while(True):
    
    now = datetime.now()
    # gun/ay/yil saat:dakika:saniye formati
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #ekran yakalama
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    for(x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        id_, conf = recognizer.predict(roi_gray)
        if conf >=45:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            
            resultPut = firebase.put(name, 'EveGirdi', {'Saat': dt_string})
            
        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_gray)
        
        color = (255, 0, 0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        
         
    #display the resulting frame
    cv2.imshow('frame', frame)
    tus = cv2.waitKey(30) & 0xff
    if tus==27:
        break
    
#when everything done, release the capture
cap.release()
cv2.destroyAllWindows()