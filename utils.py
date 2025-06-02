import cv2
import numpy as np

def average_eye_color(image_path, eye_box):
    img = cv2.imread(image_path)
    x1, y1, x2, y2 = eye_box
    eye_img = img[y1:y2, x1:x2]
    avg_color_per_row = np.average(eye_img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color  # [B, G, R]

def compare_eye_color(color1, color2, threshold=30):
    diff = np.linalg.norm(color1 - color2)
    return diff < threshold
