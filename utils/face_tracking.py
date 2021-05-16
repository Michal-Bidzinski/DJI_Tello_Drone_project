import numpy as np


# count errors and control for error elimination
def trackFace(info, w, h, pid, pError_x, pError_y, pError_fb):
    area = info[1]
    x, y = info[0]

    # yaw rotation
    error_x = x - w // 2
    yv = pid[0] * error_x + pid[1] * (error_x - pError_x)
    yv = int(np.clip(yv, -100, 100))

    # up/down
    error_y = y - h // 2
    up = pid[0] * error_y + pid[1] * (error_y - pError_y)
    up = -1*int(np.clip(up, -100, 100))

    # forward/backward
    error_fb = area - 6200
    fb = 0.005 * error_fb + 0.005 * (error_fb - pError_fb)
    fb = -1*int(np.clip(fb, -30, 30))

    if x == 0:
        yv = 0
        error_x = 0
    if y == 0:
        up = 0
        error_y = 0
    if area == 0:
        fb = 0
        error_fb = 0

    return error_x, error_y, error_fb, yv, fb, up
