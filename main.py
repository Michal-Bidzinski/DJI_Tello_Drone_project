from djitellopy import tello
import KeyPressModule as kp
import cv2
from utils.keyboard_input import getKeyboardInput
from utils.cascade_calssifier import findFace, findSmile
from utils.face_tracking import trackFace


def telloInit():
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    print(drone.get_battery())

    return drone


kp.init()

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError_x = 0
pError_y = 0
pError_fb = 0

do_scan = False


def main():
    drone = telloInit()
    
    while True:
        vals = getKeyboardInput(drone)
        img = drone.get_frame_read().frame
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

            pError_x, pError_y, pError_fb, yv, fb, up = trackFace(infoFace, w, h, pid, pError_x, pError_y, pError_fb)

            # me.send_rc_control(0, fb, up, yv)

            # print(yv, fb)

        else:
            print("do circle")

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
