import cv2


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
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        # cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        mySmileListC.append([cx, cy])
        mySmileListArea.append(area)
        mySmileListWH.append([w, h])

    if len(mySmileListArea) != 0:
        i = mySmileListArea.index(max(mySmileListArea))

        cv2.circle(img, (mySmileListC[i][0], mySmileListC[i][1]), 5, (0, 255, 0), cv2.FILLED)

        return img, [mySmileListC[i], mySmileListArea[i], [w, h]]
    else:
        return img, [[0, 0], 0, [0, 0]]