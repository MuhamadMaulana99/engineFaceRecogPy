# recognize.py

import face_recognition
import json
import numpy as np
import cv2
from preprocessing import (
    is_blurry,
    needs_lighting_enhancement,
    enhance_lighting_array
)

def recognize_face(image_path, threshold=0.5):
    if is_blurry(image_path):
        return "Gambar terlalu blur."

    image = cv2.imread(image_path)
    if needs_lighting_enhancement(image_path):
        image = enhance_lighting_array(image)

    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return "Wajah tidak ditemukan"

    encodings = face_recognition.face_encodings(image, face_locations)
    if not encodings:
        return "Gagal menghasilkan embedding"

    encoding = encodings[0]

    with open("faces.json", "r") as f:
        database = json.load(f)

    for person in database:
        known_encoding = np.array(person["encoding"])
        distance = np.linalg.norm(encoding - known_encoding)
        if distance < threshold:
            return f"Wajah dikenali: {person['name']} (jarak: {distance:.4f})"

    return f"Wajah tidak dikenali (jarak: {distance:.4f}"

# Contoh
if __name__ == "__main__":
    print(recognize_face("images/ivan5.jpg"))
