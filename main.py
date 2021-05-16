from djitellopy import tello
import KeyPressModule as kp
import cv2
from utils.keyboard_input import getKeyboardInput, keyboardInit
from utils.cascade_calssifier import findFace, findSmile
from utils.face_tracking import trackFace


def telloInit():
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    print(drone.get_battery())

    return drone


def main():
    # parameters
    w, h = 360, 240
    fbRange = [6200, 6800]
    pid = [0.4, 0.4, 0]
    pError_x = 0
    pError_y = 0
    pError_fb = 0
    do_scan = False
    it = 0

    # init
    drone = telloInit()
    keyboardInit()

    # define video writer
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output2.mp4', fourcc, 20.0, (640, 480))

    # main loop
    while True:
        # get keyboatd inputs
        vals = getKeyboardInput(drone)

        # get image from camera
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

            # counting corrective control
            pError_x, pError_y, pError_fb, yv, fb, up = trackFace(infoFace, w, h, pid, pError_x, pError_y, pError_fb)
            # drone.send_rc_control(0, fb, up, yv)

        else:
            print("do circle")
            if it <= 2:
                # drone.send_rc_control(-12, 0, 0, 0)
                it += 1
            if it > 2:
                # drone.send_rc_control(-12, 0, 0, 60)
                it += 1
            if it > 5:
                it = 0
            out.write(img)

        cv2.imshow("Image", img)
        c = cv2.waitKey(1)
        if c & 0xFF == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
