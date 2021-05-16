import KeyPressModule as kp
import time


def getKeyboardInput(drone):
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

    if kp.getKey("q"): drone.land(); time.sleep(3)
    if kp.getKey("e"): drone.takeoff()

    return [lr, fb, up, yv]
