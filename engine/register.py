import cv2
import face_recognition
import uuid
import json
import os
from utils.image_quality import is_blurry, enhance_lighting_if_needed, crop_face

def register_face(image_path, name):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise "❌ Gambar tidak ditemukan atau path salah."

    # Cek kualitas gambar
    if is_blurry(image_path):
        raise " ❌ Register Gambar terlalu blur."
    
    # Tingkatkan pencahayaan jika perlu
    image = enhance_lighting_if_needed(image)

    # Convert ke RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Deteksi wajah (face_locations) dalam gambar
    face_locations = face_recognition.face_locations(rgb_image)
    if len(face_locations) == 0:
        raise ValueError(" ❌ Tidak ada wajah yang terdeteksi pada gambar.")
    if len(face_locations) > 1:
        raise ValueError(" ❌ Lebih dari satu wajah terdeteksi, gunakan gambar dengan satu wajah.")

    # Ambil encoding wajah dengan koordinat lokasi
    encoding = face_recognition.face_encodings(rgb_image, known_face_locations=face_locations)[0]

    # Baca data faces.json jika ada
    database_path = "faces.json"
    if os.path.exists(database_path):
        with open(database_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Validasi duplikat nama
    if any(entry['name'].lower() == name.lower() for entry in data):
        return f"❌ Nama = {name} sudah terdaftar."

    # Validasi duplikat encoding (bisa dengan threshold jarak)
    import numpy as np
    for entry in data:
        existing_encoding = np.array(entry['encoding'])
        dist = np.linalg.norm(existing_encoding - encoding)
        if dist < 0.6:  # threshold biasanya 0.6 untuk face_recognition
              return f"❌ Foto dengan nama {entry['name']} sudah terdaftar."

    # Buat id unik
    id_face = str(uuid.uuid4())

    # Simpan data baru
    new_data = {
        "id": id_face,
        "name": name,
        "encoding": encoding.tolist()
    }
    data.append(new_data)

    # Simpan ke JSON
    with open(database_path, "w") as f:
        json.dump(data, f)

    return f"✔️ Berhasil mendaftarkan {name} dengan ID {id_face}"

# Contoh panggil:
# if __name__ == "__main__":
#     print(register_face("images/zay 2.jpg", "Zayadi 2"))
