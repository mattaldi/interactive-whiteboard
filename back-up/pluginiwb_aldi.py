import numpy as np, cv2, pyautogui, urllib, pyautogui, time
from matplotlib import pyplot as plt

def averaging_hsv(hsv):
    avr_pr_row  = np.average(hsv, axis=0)
    avr_pr_row  = np.average(avr_pr_row, axis=0)
    avrh        = avr_pr_row[0]
    avrs        = avr_pr_row[1]
    avrv        = avr_pr_row[2]
    nrs, nrv    = 130, 100

    if avrs > nrs and avrv > nrv:
        sl  = avrs / 1.5
        sh  = avrs * 1.2
        vl  = avrv * 1.2
        vh  = 255
    elif avrs > nrs and avrv < nrv:
        sl  = avrs / 1.5
        sh  = avrs * 1.2
        vl  = avrv * 8.0
        vh  = 255
    else:
        sl  = avrs * 0.5
        sh  = 130
        vl  = 190
        vh  = 255

    vl = vl + 80
    if vl > 250:
        vl = 250
    sl = sl + 20
    hl, hh = 30, 90
    
    return sl, sh, hl, hh, vl, vh

def most_bright(image):
    gray    = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    radius  = 5
    gray    = cv2.GaussianBlur(gray, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    return minVal, maxVal, minLoc, maxLoc

def masking_image(frame, hsv, sl, sh, hl, hh, vl, vh):
    mask    = cv2.inRange(hsv, (hl, sl, vl), (hh, sh, vh))
    mask    = cv2.dilate(mask, None, iterations=16)
    mask    = cv2.erode(mask, None, iterations=14)
    output  = cv2.bitwise_and(frame, frame, mask = mask)
    return output

def selectROI(event, x, y, flags, param):
    global frame, roiPts, inputMode
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts.append((x, y))
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.imshow("frame", frame)

