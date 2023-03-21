# Face Recognition Exercises

In this project I used haarcascades frontal face datas. We train the datas in faces-train.py which we collected from yuzler.xml. After that we have an image folder where we store person's face pictures with names. 

In the ev-giris-facerecognition.py we are using camera to detect person's face and after detecting the face, algorithm takes a snapshot. After that, algorithm search the images we stored before to match with that snapshot. If the images match, we are connecting Firebase to update database as, "The person entered the home at DD/MM/YY H:M:S" format.

In the el-yikama-facesrecognition.py firstly we listen Firebase database time by time to check if the database is updated and if the database is updated our algorithm starts. We are waiting 5 mins for that person who entered home to clean his hands in the bathroom. If the camera in the bathroom detects that person, we are updating database as, "The person cleaned his hands". If the camera in the bathroom doesn't detect that person entered home in 5 mins, we are updating database as, "The person didn't clean his hands".
