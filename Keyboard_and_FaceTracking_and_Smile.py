from djitellopy import tello
import KeyPressModule as kp
import time
import cv2
import numpy as np

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError_x = 0
pError_y = 0
pError_fb = 0


def findFace(img):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i], [w, h]]
    else:
        return img, [[0, 0], 0, [0, 0]]


def findSmile(img):
    smileCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    smiles = smileCascade.detectMultiScale(imgGray, 1.3, 11)

    mySmileListC = []
    mySmileListArea = []
    mySmileListWH = []

    for (x, y, w, h) in smiles:
        #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        #cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        mySmileListC.append([cx, cy])
        mySmileListArea.append(area)
        mySmileListWH.append([w, h])

    if len(mySmileListArea) != 0:
        i = mySmileListArea.index(max(mySmileListArea))

        #cv2.rectangle(img, (mySmileListC[i][0], mySmileListC[i][1]), (mySmileListC[i][0] + w, mySmileListC[i][1] + h), (0, 0, 255), 2)
        cv2.circle(img, (mySmileListC[i][0], mySmileListC[i][1]), 5, (0, 255, 0), cv2.FILLED)

        return img, [mySmileListC[i], mySmileListArea[i], [w, h]]
    else:
        return img, [[0, 0], 0, [0, 0]]


def trackFace(info, w, pid, pError_x, pError_y, pError_fb):
    area = info[1]
    x, y = info[0]

    error_x = x - w // 2
    speed = pid[0] * error_x + pid[1] * (error_x - pError_x)
    speed = int(np.clip(speed, -100, 100))

    error_y = y - h // 2
    up = pid[0] * error_y + pid[1] * (error_y - pError_y)
    up = -1*int(np.clip(up, -100, 100))

    error_fb = area - 6200
    fb = 0.005 * error_fb + 0.005 * (error_fb - pError_fb)
    fb = -1*int(np.clip(fb, -30, 30))

    if x == 0:
        speed = 0
        error_x = 0
    if y == 0:
        up = 0
        error_y = 0
    if area == 0:
        fb = 0
        error_fb = 0

    return error_x, error_y, error_fb, speed, fb, up


def getKeyboardInput():
    lr, fb, up, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): up = speed
    elif kp.getKey("s"): up = -speed

    if kp.getKey("a"): yv = -int(speed*1.5)
    elif kp.getKey("d"): yv = int(speed*1.5)

    if kp.getKey("q"): me.land(); time.sleep(3)
    if kp.getKey("e"): me.takeoff()

    return [lr, fb, up, yv]


do_scan = False

while True:
    vals = getKeyboardInput()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))

    if not do_scan:
        img, infoFace = findFace(img)
        img, infoSmile = findSmile(img)

        print("Face: ", infoFace)
        print("Smile: ", infoSmile)
        if infoFace[1] != 0:
            if (infoFace[0][1]+10) < infoSmile[0][1] < (infoFace[0][1] + infoFace[2][1]/2 - 10): 
                print("SMILE DETECT ################################################")
                do_scan = True

        pError_x, pError_y, pError_fb, yv, fb, up = trackFace( infoFace, w, pid, pError_x, pError_y, pError_fb)

        # me.send_rc_control(0, fb, up, yv)

        # print(yv, fb)

    else:
        print("do circle")

    cv2.imshow("Image", img)
    cv2.waitKey(1)
