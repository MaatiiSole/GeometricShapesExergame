import cv2
import numpy as np
import matplotlib.pyplot as plt


def getContours(img):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 4000:

            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            objectType = "None"

            if objCor == 3:
                objectType = "Tri"
            elif objCor == 4:
                aspRatio = w / float(h)
                if aspRatio > 0.98 and aspRatio < 1.03:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor > 4:
                # Encontrar el círculo mínimo que encierra el contorno
                (x_circle, y_circle), radius = cv2.minEnclosingCircle(cnt)
                circle_area = np.pi * (radius ** 2)
                if abs(area - circle_area) < 0.2 * circle_area:
                    objectType = "Circle"
                else:
                    objectType = "Complex"
                
            if objectType != "None":
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    imgContour,
                    objectType,
                    (x + (w // 2) - 10, y + (h // 2) - 10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                )
                cv2.putText(
                    imgContour,
                    "A: " + str(area),
                    (x + (w // 2) - 10, y + (h) - 10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                )


def preprocess(image):
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    return imgCanny


def color_segmentation(img, params):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = params[0]
    h_max = params[1]
    s_min = params[2]
    s_max = params[3]
    v_min = params[4]
    v_max = params[5]
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    return imgResult


# --------------------------------------------------- main --------------------------------------------------
frameWidth = 640
frameHeight = 480
frame_number = 1
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# cap.set(10, 150)
cap.set(cv2.CAP_PROP_FPS , frame_number)

# params_orange = [0, 14, 66, 255, 130, 255]
# params_green = [40, 70, 0, 255, 100, 255]
# params_green2 = [15, 60, 30, 255, 100, 255]
# params_green3 = [70, 120, 50, 255, 100, 255]
# params_papel = [60, 105, 20, 80, 90, 255]
params_blue = [90, 125, 20, 180, 0, 255]

mode = 2

while True:
    success, img = cap.read()
    # color segmentation
    img_seg = color_segmentation(img, params_blue)
    imgContour = img.copy()
    imgCanny = preprocess(img_seg)
    getContours(imgCanny)

    if mode == 1:
        cv2.imshow("Result", img_seg)
    elif mode == 2:
        cv2.imshow("Result", imgCanny)
    elif mode == 3:
        cv2.imshow("Result", imgContour)
    else:
        cv2.imshow("Result", img)
        
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    else:
        if chr(key).isdigit():
            mode = int(chr(key))
            print("mode:", mode)
