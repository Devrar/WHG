import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyautogui as pa
import time

vid = cv2.VideoCapture('LivelliWHG/Level1.mov')
cen_ar = []
moving_ar = []
action_ar = []
while (vid.isOpened()):
    ret, frame = vid.read()

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blu = np.array([170, 50, 50])
        upper_blu = np.array([180, 255, 255])

        mask = cv2.inRange(hsv, lower_blu, upper_blu)

        if mask.any() != 0:
            res = cv2.bitwise_and(frame, frame, mask = mask)
            gray_res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            _, res1 = cv2.threshold(res, 127, 255, cv2.THRESH_BINARY_INV)
            M = cv2.moments(gray_res)

            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            cen_ar.append((cx, cy))
            #print((cx, cy))

        #cv2.imshow('Frame', frame)
        #cv2.imshow('mask', mask)
        #cv2.imshow('res', res1)

        #if cv2.waitKey(1) == ord('q'):
        #    break

    else:
        break

vid.release()
cv2.destroyAllWindows()

for j in range(len(cen_ar) - 1):
    moving_ar.append((cen_ar[j + 1][0] - cen_ar[j][0], cen_ar[j + 1][1] - cen_ar[j][1]))

i = 0
j = 0

while i < len(moving_ar):
    if moving_ar[i][0] == moving_ar[i][1] == 0:
        while (moving_ar[i + j][0] == moving_ar[i + j][1] == 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Stop", j))
        i += j
        j = 0
    elif (moving_ar[i][0] > 0) & (moving_ar[i][1] == 0):
        while (moving_ar[i + j][0] > 0) & (moving_ar[i + j][1] == 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Right", j))
        i += j
        j = 0
    elif (moving_ar[i][0] < 0) & (moving_ar[i][1] == 0):
        while (moving_ar[i + j][0] < 0) & (moving_ar[i + j][1] == 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Left", j))
        i += j
        j = 0
    elif (moving_ar[i][0] == 0) & (moving_ar[i][1] > 0):
        while (moving_ar[i + j][0] == 0) & (moving_ar[i + j][1] > 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Down", j))
        i += j
        j = 0
    elif (moving_ar[i][0] == 0) & (moving_ar[i][1] < 0):
        while (moving_ar[i + j][0] == 0) & (moving_ar[i + j][1] < 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Up", j))
        i += j
        j = 0
    elif (moving_ar[i][0] > 0) & (moving_ar[i][1] > 0):
        while (moving_ar[i + j][0] > 0) & (moving_ar[i + j][1] > 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Down&Right", j))
        i += j
        j = 0
    elif (moving_ar[i][0] > 0) & (moving_ar[i][1] < 0):
        while (moving_ar[i + j][0] > 0) & (moving_ar[i + j][1] < 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Up&Right", j))
        i += j
        j = 0
    elif (moving_ar[i][0] < 0) & (moving_ar[i][1] > 0):
        while (moving_ar[i + j][0] < 0) & (moving_ar[i + j][1] > 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Down&Left", j))
        i += j
        j = 0
    elif (moving_ar[i][0] < 0) & (moving_ar[i][1] < 0):
        while (moving_ar[i + j][0] < 0) & (moving_ar[i + j][1] < 0):
            j += 1
            if i + j >= len(moving_ar):
                break
        action_ar.append(("Up&Left", j))
        i += j
        j = 0

action_ar1 = []
i = 0

while i < len(action_ar):
    if (action_ar[i][0] == "Stop") & (action_ar[i][1] < 4):
        action_ar1.append((action_ar[i + 1][0], action_ar[i][1] + action_ar[i + 1][1]))
        i = i + 2
    else:
        action_ar1.append(action_ar[i])
        i += 1

i = 0
j = 0
z = 0
action_ar2 = []

while i < len(action_ar1):
    while (action_ar1[i + j][0] == action_ar1[i][0]):
        z += action_ar1[i + j][1]
        j += 1
        if i + j >= len(action_ar1):
            break
    action_ar2.append((action_ar1[i][0], z))
    i += j
    j = 0
    z = 0

print(action_ar2)

'''
time.sleep(4)
pa.keyDown("command")
pa.press("space")
pa.keyUp("command")
pa.typewrite("g")
pa.press("enter")
time.sleep(2)
pa.typewrite("il")
pa.press("enter")
time.sleep(10)
pa.scroll(-5)
pa.click(700, 430)
pa.moveTo(350, 200, 1)
pa.click()
pa.moveTo(700, 410, 2)
pa.click()
time.sleep(8)
pa.moveTo(500, 500, 1)
pa.click()
pa.moveTo(850, 550, 1)
pa.click()
time.sleep(2)

start_time = time.time()
for (a, b) in action_ar2:
    if a == "Stop":
        time.sleep(b/59.76)
    elif a == "Right":
        while time.time() - start_time < b/59.76:
            pa.keyDown("right")
        pa.keyUp("right")
    elif a == "Left":
        while time.time() - start_time < b/59.76:
            pa.keyDown("left")
        pa.keyUp("left")
    elif a == "Down":
        while time.time() - start_time < b/59.76:
            pa.keyDown("down")
        pa.keyUp("down")
    elif a == "Left":
        while time.time() - start_time < b/59.76:
            pa.keyDown("left")
        pa.keyUp("left")
    elif a == "Up":
        while time.time() - start_time < b/59.76:
            pa.keyDown("up")
        pa.keyUp("up")
    elif a == "Down&Right":
        while time.time() - start_time < b/59.76:
            pa.keyDown("down")
            pa.keyDown("right")
        pa.keyUp("down")
        pa.keyUp("right")
    elif a == "Up&Right":
        while time.time() - start_time < b/59.76:
            pa.keyDown("up")
            pa.keyDown("right")
        pa.keyUp("up")
        pa.keyUp("right")
    elif a == "Down&Left":
        while time.time() - start_time < b/59.76:
            keyDown("down")
            keyDown("left")
        keyUp("down")
        keyUp("left")
    elif a == "Up&Left":
        while time.time() - start_time < b/59.76:
            pa.keyDown("up")
            pa.keyDown("left")
        pa.keyUp("up")
        pa.keyUp("left")
'''
