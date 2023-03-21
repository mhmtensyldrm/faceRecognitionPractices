import numpy as np
import cv2
import pickle
import time
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
   
    #result1 firebaseden ilk veriyi alıyor daha sonra program 10 saniye bekliyor result2 ise firebaseden ikinci veriyi alıyor
    result1 = firebase.get('/enes','EveGirdi')
    time.sleep(10)
    result2 = firebase.get('/enes','EveGirdi')
    
    #eğer o 10 saniye içinde databasedeki veri değişmiş ise(bu senaryoda verinin değişmesi bize kişinin evin önündeki kamerada gözüktüğünü yani kişinin eve giriş yaptığını anlatıyor) program işlevini gerçekleştirmeye başlıyor
    if result1 != result2:
        while(True):
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
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
            
                    resultPut = firebase.put(name, 'EliniYikadi', {'Elini yikadigi saat': dt_string})
                    
                img_item = "my-image.png"
                cv2.imwrite(img_item, roi_gray)
        
                color = (255, 0, 0)
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)   
            
            cv2.imshow('frame', frame)
            result3 = firebase.get('/enes','EliniYikadi')
            time.sleep(300) #lavaboya gelmesi icin 5 dk bekliyor
            result4 = firebase.get('/enes','EliniYikadi')
            if result3 == result4:
                resultPut2 = firebase.put('enes', 'EliniYikadi', {'Elini yikamayi biraktigi saat': 'Elini Yikamadi!'}) 
                
            break
    #eve giris yapmamissa kamerayi acmayip eve giris yapmasini bekliyor
    else:
        continue
    
    
