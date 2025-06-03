# utils/image_quality.py
import cv2
import numpy as np

def is_blurry(image_path, threshold=100.0):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Gambar tidak ditemukan.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < threshold

def enhance_lighting_if_needed(image, clip_limit=2.0, tile_grid_size=(8,8)):
    # Gunakan CLAHE untuk memperbaiki pencahayaan
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return enhanced

def crop_face(image, face_location):
    # face_location = (top, right, bottom, left)
    top, right, bottom, left = face_location
    return image[top:bottom, left:right]
