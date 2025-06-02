# preprocessing.py

import cv2
import face_recognition
import numpy as np

def is_blurry(image_path, threshold=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    lap = cv2.Laplacian(img, cv2.CV_64F)
    variance = lap.var()
    return variance < threshold

def needs_lighting_enhancement(image_path, brightness_threshold=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    avg_brightness = np.mean(img)
    return avg_brightness < brightness_threshold

def enhance_lighting_array(img_array):
    img_yuv = cv2.cvtColor(img_array, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img_output

def crop_face_array(image_array):
    face_locations = face_recognition.face_locations(image_array)
    if not face_locations:
        return None
    top, right, bottom, left = face_locations[0]
    face_image = image_array[top:bottom, left:right]
    return face_image
