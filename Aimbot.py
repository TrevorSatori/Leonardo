import mss
import numpy as np
import cv2
import keyboard
import torch 
import serial
import time


# SETUP. arduino port may be different. Run movement testing to find name
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/Trevor/Documents/yolov5/yolov5/runs/train/exp2/weights/best.pt')
arduino = serial.Serial('COM5', 9600, timeout=0)

ScreenSizeX = 3840
ScreenSizeY = 2160
with mss.mss() as sct: 
    monitor = {'top': 0, 'left': 0, 'width': ScreenSizeX, 'height': ScreenSizeY}

while True:
    img = np.array(sct.grab(monitor))

    results = model(img)
    rl = results.xyxy[0].tolist()

    # if any results do the following
    if len(rl) > 0:
        # if the confidence is above 30%
        if rl[0][4] >= .3:
            # Class prediction
            if rl[0][5]  == 1:

                print(rl[0])

                # X Info
                xmax = int(rl[0][2])
                width = int(rl[0][2] - rl[0][0])
                screenCenterX = ScreenSizeX / 2
                centerX = int((xmax - (width/2)) - screenCenterX)
                
                # Y INFO
                ymax = int(rl[0][1])
                height = int(rl[0][1] - rl[0][3])
                screenCenterY = ScreenSizeY / 2
                centerY = int((ymax - (height/4)) - screenCenterY)

                # Change decimal as needed
                moveX = int(centerX * .1)
                moveY = int(centerY * .1)

                if centerY < screenCenterY:
                    moveY *= -1

                arduino.write((str(moveX) + ":" + str(moveY) + 'x').encode())
                time.sleep(.08)
    cv2.waitKey(1)

    if keyboard.is_pressed('q'):
        break

cv2.destroyAllWindows()



#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# 1  433.50  433.50   517.5  714.5    0.687988     27     tie
# 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# 3  986.00  304.00  1028.0  420.0    0.286865     27     tie
