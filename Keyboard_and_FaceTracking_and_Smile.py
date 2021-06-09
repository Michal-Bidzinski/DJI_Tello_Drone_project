from djitellopy import tello
import KeyPressModule as kp
import cv2
from utils.keyboard_input import getKeyboardInput
from utils.cascade_calssifier import findFace, findSmile
from utils.face_tracking import trackFace
from time import sleep

# kp.init()
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

do_scan = False

it = 0
it_all = 0

# define video writer
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

while True:
    vals = getKeyboardInput(me)
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))

    img, infoFace = findFace(img)
    img, infoSmile = findSmile(img)

    do_scan = vals[4]

    if not do_scan:

        print("Face: ", infoFace)
        print("Smile: ", infoSmile)
        if infoFace[1] != 0:
            if ((infoFace[0][1] + 10) < infoSmile[0][1] < (infoFace[0][1] + infoFace[2][1] / 2 - 15)
                    and (infoFace[0][0] - 80) < infoSmile[0][0] < (infoFace[0][0] + 80)):
                print("SMILE DETECT ################################################")
                # do_scan = True

        pError_x, pError_y, pError_fb, yv, fb, up = trackFace(infoFace, w, h, pid, pError_x, pError_y, pError_fb)

        me.send_rc_control(0, fb, up, yv)

        # print(yv, fb)

    else:
        print("do circle")
        if 208 < it_all < 213:
            me.send_rc_control(0, 0, -20, 0)
        else:
            if it <= 2:
                me.send_rc_control(-20, 0, 0, 0)
                it += 1
            elif it > 2:
                me.send_rc_control(-20, 0, 0, 50)
                it += 1
            if it > 5:
                it = 0
        it_all += 1
        print(it_all)
        out.write(img)

    cv2.imshow("Image", img)
    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break

out.release()
cv2.destroyAllWindows()
