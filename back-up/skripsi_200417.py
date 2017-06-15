import numpy as np, cv2, pyautogui, urllib, pyautogui, progressbar, time
from matplotlib import pyplot as plt

stream = urllib.urlopen('http://192.168.43.1:8080/video')

bytes  = ''

xv_stream = []
sbx_stream = []
roiPts = []
bar = progressbar.ProgressBar(redirect_stdout=True, max_value=4)
m = 0


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



while(True):
    bytes+=stream.read(16384)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    
    if a!=-1 and b!=-1:
        
        jpg     = bytes[a:b+2]
        bytes   = bytes[b+2:]
        frame   = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

        camheight     = len(frame)
        camwidth      = len(np.rot90(frame))
        screenheight  = pyautogui.size()[1]
        screenwidth   = pyautogui.size()[0]

        factor_y = screenheight / float(camheight)
        factor_x = screenwidth / float(camwidth)
        print factor_y, factor_x
#        print camheight, camwidth, screenheight, screenwidth
        
        hsv     = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        sl, sh, hl, hh, vl, vh          = averaging_hsv(hsv)
        output                          = masking_image(frame, hsv, sl, sh, hl, hh, vl, vh)

        minVal, maxVal, minLoc, maxLoc = most_bright(output)
        if maxVal > 1:
            cv2.circle(frame, maxLoc, 5, (255, 0, 0), 2)
            xv      = maxLoc[0]
            yv      = maxLoc[1]
            hsvcspc = hsv[:,:,1]

            #calibrate
            if len(roiPts) < 4:
                
                pyautogui.moveTo(xv*factor_x,yv*factor_y)
                xv_stream.append(xv)

                if len(xv_stream) > 30:
                    del xv_stream[0]
                    
                    sbxstd = np.std(xv_stream)
                    
                    if sbxstd < 3:
                        roiPts.append((xv, yv))
                        xv_stream = []
                        print "*" * len(roiPts)

            #detection
            else:
                print "program running..."

            
#            print "terdeteksi"
        

        cv2.imshow("frame", frame)
        cv2.imshow("frame2", output)
 
        if cv2.waitKey(1) ==27:
            exit(0)  

cap.release()
cv2.destroyAllWindows()
