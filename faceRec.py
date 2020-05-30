''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition and Marcelo Rovai - MJRoBot.org  
Developed by David Plummer 19/05/20 SIT210 Project  

'''

import cv2
import numpy as np
import os
import time



def menu():
    print(" DOOR ACCESS \n 0:QUIT \n 1:ENABLE ")

enable = True

while enable:
    menu()
    choice = input(" :")
    if choice == "1":
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);
        font = cv2.FONT_HERSHEY_SIMPLEX

        #iniciate id counter
        id = 0

        # names related to ids: example ==> David: id=1,  etc
        names = ['None', 'David', 'Neo', 'Z', 'W']
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)
        run = True

        while run:
            

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

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    if id == "David":
                        print(id)
                        #send granted curl command to Argon 
                        granted = os.system('curl -H "Authorization:Bearer ab4c43dbdfabf60178a0593e29f93e7ad37ee220" https://api.particle.io/v1/devices/e00fce68da0d3a3426d0c163/door -d arg=granted')
                        run = False
                           
                    elif id == "Neo":
                        print(id)
                        #send denied curl command to Argon and email to deakin email 
                        denied = os.system('curl -H "Authorization:Bearer ab4c43dbdfabf60178a0593e29f93e7ad37ee220" https://api.particle.io/v1/devices/e00fce68da0d3a3426d0c163/door -d arg=denied')
                        cv2.imwrite("denied/Denied." + str(id) + ".jpg", gray[y:y+h,x:x+w])
                        email = os.system('mpack -s "Neo denied Access to Door" /home/pi/FR/denied/Denied.Neo.jpg dplummer@deakin.edu.au')
                        run = False
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    #send denied curl command to Argon and email to deakin email 
                    denied = os.system('curl -H "Authorization:Bearer ab4c43dbdfabf60178a0593e29f93e7ad37ee220" https://api.particle.io/v1/devices/e00fce68da0d3a3426d0c163/door -d arg=denied')
                    cv2.imwrite("denied/Denied.Unknown" + ".jpg", gray[y:y+h,x:x+w])
                    email = os.system('mpack -s "Unknown user denied Access to Door" /home/pi/FR/denied/Denied.Unknown.jpg dplummer@deakin.edu.au')
                    run = False
        cam.release()
        cv2.destroyAllWindows()
        
        
    elif choice == "0":
        enable = False
        
    else:
        input("Wrong choice, Please enter your selection \n :")


print("\n [INFO] Exiting Program and cleanup stuff")
cv2.destroyAllWindows()

