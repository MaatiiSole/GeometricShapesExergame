import cv2
import numpy as np

def getEdges(image):
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    return imgCanny

def getContours(img,imgContour,shape):
    success = False
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:

            peri = cv2.arcLength(contour, True)
            # print(peri)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            # print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            objectType = "None"

            if objCor == 3:
                objectType = "triangulo"
            elif objCor == 4:
                aspRatio = w / float(h)
                if aspRatio > 0.9 and aspRatio < 1.1:
                    objectType = "cuadrado"
                else:
                    objectType = "rectangulo"
            elif objCor > 4:
                # Encontrar el círculo mínimo que encierra el contorno
                (x_circle, y_circle), radius = cv2.minEnclosingCircle(contour)
                circle_area = np.pi * (radius ** 2)
                if abs(area - circle_area) < 0.2 * circle_area:
                    objectType = "circulo"
                else:
                    objectType = "Complex"
                
            if objectType != "None":
                cv2.drawContours(imgContour, contour, -1, (255, 0, 0), 3)
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
                if objectType == shape:
                    success = True
                    
    return success, imgContour