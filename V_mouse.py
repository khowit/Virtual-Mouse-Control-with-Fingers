import  cv2
import numpy as np
import Hand_tracking as htm
import time
import pyautogui
import  os

#############################
wcam = 640
hcam = 480
frameR = 100
smoothn = 5
###########################

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
detector = htm.handDetector()
screenW, screenH = pyautogui.size()
pTime = 0
cTime = 0

plocalx, plocaly = 0,0
clocalx, clocaly = 0,0

while True:
    success, frame = cap.read()
    # frame = cv2.flip(frame,1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)

    if len(lmList) != 0:       
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(frame, (frameR, frameR), (wcam - frameR, hcam - frameR), (255,0,255), 2)

        if fingers[1]==1 and fingers[2]==0:
            
            x3 = np.interp(x1, (frameR, wcam - frameR), (0, screenW))
            y3 = np.interp(y1, (frameR, hcam - frameR), (0, screenH))

            clocalx = plocalx + (x3 - plocalx)
            clocaly = plocaly + (y3 - plocaly)
            
            pyautogui.moveTo(screenW - x3, y3)
            cv2.circle(frame, (x1, y1), 15, (255,0,255), cv2.FILLED)
            
            plocalx, plocaly = clocalx, clocaly

        
        if fingers[1]==1 and fingers[2]==1:
            length, info, frame = detector.findDistance(8, 12, frame)
            if length < 50:
                cv2.circle(frame, (info[4], info[5]), 15, (0,255,0), cv2.FILLED)
                pyautogui.click()
                

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
    cv2.imshow("Output", frame)
    if cv2.waitKey(1) & 0xFF == ord("e"):
        break


cap.release()
cv2.destroyAllWindows()