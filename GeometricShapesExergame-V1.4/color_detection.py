import cv2
import numpy as np


def color_segmentation(img, params):
    h_min, h_max, s_min, s_max, v_min, v_max = params

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if h_min <= h_max:
        # Caso simple: el rango no cruza el límite de 180 grados
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgHSV, lower, upper)
    else:
        # Caso cíclico: el rango cruza el límite de 180 grados
        lower1 = np.array([h_min, s_min, v_min])
        upper1 = np.array([180, s_max, v_max])
        mask1 = cv2.inRange(imgHSV, lower1, upper1)
        
        lower2 = np.array([0, s_min, v_min])
        upper2 = np.array([h_max, s_max, v_max])
        mask2 = cv2.inRange(imgHSV, lower2, upper2)
        
        mask = cv2.bitwise_or(mask1, mask2)

    imgResult = cv2.bitwise_and(img, img, mask=mask)
    return imgResult


def color_segmentation2(img, hsv_point, threshold):
    h_point, s_point, v_point = hsv_point

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    dist = np.sqrt((imgHSV[:,:,0] - h_point)**2 + (imgHSV[:,:,1] - s_point)**2 + (imgHSV[:,:,2] - v_point)**2)
    
    mask = np.zeros_like(imgHSV[:,:,0])
    mask[dist < threshold] = 255
    
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    return imgResult