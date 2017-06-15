import numpy as np, cv2, pyautogui, urllib, pyautogui, time
from matplotlib import pyplot as plt

stream = urllib.urlopen('http://192.168.43.1:8080/video')

bytes  = ''

xv_stream = []
sbx_stream = []
roiPts = []
m = 0
roiBox = None
inputMode = False
def equalizate(frame):
    hist,bins = np.histogram(frame.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    img2 = cdf[frame]
    return img2

def averaging_hsv(hsv):
    avr_pr_row = np.average(hsv, axis=0)
    avr_pr_row = np.average(avr_pr_row, axis=0)

    avrh    = avr_pr_row[0]
    avrs    = avr_pr_row[1]
    avrv    = avr_pr_row[2]

    nrs     = 130
    nrv     = 100


    if avrs < nrs and avrv > nrv:
        sl  = avrs * 0.5
        sh  = 130
        vl  = 190
        vh  = 255
    elif avrs > nrs and avrv > nrv:
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
        sl  = 25
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
    #   kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

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

cv2.namedWindow("frame")
cv2.setMouseCallback("frame", selectROI)

custom_camheight = 1
custom_camwidth  = 1

while(True):
    bytes+=stream.read(16384)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    
    if a!=-1 and b!=-1:
        
        jpg     = bytes[a:b+2]
        bytes   = bytes[b+2:]
        frame   = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

        height_video    = len(frame)
        width_video     = len(np.rot90(frame))
        height_desktop  = pyautogui.size()[1]
        width_desktop   = pyautogui.size()[0]

        factor_y_2 = (height_desktop / float(height_video))
        factor_x_2 = (width_desktop / float(width_video))
        #print factor_y, factor_x
#        print camheight, camwidth, screenheight, screenwidth
        
        hsv     = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        sl, sh, hl, hh, vl, vh          = averaging_hsv(hsv)
        output                          = masking_image(frame, hsv, sl, sh, hl, hh, vl, vh)

        minVal, maxVal, minLoc, maxLoc = most_bright(output)
        
        



        if roiBox is not None and maxVal > 1:
            cv2.circle(frame, maxLoc, 5, (255, 0, 0), 2)
            xv      = maxLoc[0]
            yv      = maxLoc[1]
            hsvcspc = hsv[:,:,1]

            
            aaa = (((xv - indenx) * factor_x_2) * factor_x_1) 
            bbb = (((yv - indeny) * factor_y_2) * factor_y_1)

            
            print xv, yv, aaa, bbb

            if aaa < 0:
                aaa = 0
            if bbb < 0:
                bbb = 0
                
            if aaa != 0 or bbb != 0:
                pyautogui.moveTo(aaa,bbb)




        cv2.imshow("frame", frame)
        cv2.imshow("frame2", output)

        

        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("i") and len(roiPts) < 4:
            inputMode = True
            orig = frame.copy()

            while len(roiPts) < 4:
                    cv2.imshow("frame", frame)
                    cv2.waitKey(0)

            roiPts = np.array(roiPts)
            s = roiPts.sum(axis = 1)
            tl = roiPts[np.argmin(s)]
            br = roiPts[np.argmax(s)]

            roi = orig[tl[1]:br[1], tl[0]:br[0]]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            #roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

            roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
            roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
            roiBox = (tl[0], tl[1], br[0], br[1])

           # print roiPts
            if len(roiPts) == 4:
                a1 = roiPts[0]
                a2 = roiPts[1]
                a3 = roiPts[2]
                a4 = roiPts[3]

                indenx = a1[0]
                indeny = a1[1]
                

                wid1 = a2[0]-a1[0]
                wid2 = a4[0]-a3[0]
                wid  = int(round((wid1 + wid2)/float(2)))
        
                hei1 = a4[1]-a2[1]
                hei2 = a3[1]-a1[1]
                hei  = int(round((hei1 + hei2)/float(2)))

                height_calibration  = hei
                width_calibration   = wid
                factor_y_1     = int(height_video / float(height_calibration))
                factor_x_1     = int(width_video / float(width_calibration))

                
        if cv2.waitKey(1) ==27:
            exit(0)  

cap.release()
cv2.destroyAllWindows()
