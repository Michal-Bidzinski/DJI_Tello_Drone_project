import KeyPressModule as kp
import time


circle = False


def keyboardInit():
    kp.init()


def getKeyboardInput(drone):
    lr, fb, up, yv = 0, 0, 0, 0
    speed = 50
    global circle

    # left and right steering
    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    # forward and backward steering
    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    # up and down steering
    if kp.getKey("w"): up = speed
    elif kp.getKey("s"): up = -speed

    # yaw rotation steering
    if kp.getKey("a"): yv = -int(speed*1.5)
    elif kp.getKey("d"): yv = int(speed*1.5)

    # do circle
    if kp.getKey("z"): circle = True
    elif kp.getKey("x"): circle = False

    # land and takeoff
    if kp.getKey("q"): drone.land(); time.sleep(10)
    if kp.getKey("e"): drone.takeoff()

    return [lr, fb, up, yv, circle]
