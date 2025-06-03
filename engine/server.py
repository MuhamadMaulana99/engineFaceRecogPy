from concurrent import futures
import grpc
import base64
import cv2
import numpy as np
import os
import time
import face_recognition_pb2
import face_recognition_pb2_grpc
import recognize
import register

class FaceRecognitionServicer(face_recognition_pb2_grpc.FaceRecognitionServicer):
    def RegisterFace(self, request, context):
        try:
            # Decode base64
            image_bytes = base64.b64decode(request.image)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("❌ Gambar tidak valid atau gagal didecode")

            # Simpan ke folder: engine/images/registered_faces
            folder_path = os.path.join("engine", "images", "registered_faces")
            os.makedirs(folder_path, exist_ok=True)
            filename = f"{request.name or 'unknown'}_{int(time.time())}.jpg"
            temp_path = os.path.join(folder_path, filename)
            cv2.imwrite(temp_path, img)

            result = register.register_face(temp_path, request.name)
            return face_recognition_pb2.RegisterReply(message=result, success=True)

        except Exception as e:
            return face_recognition_pb2.RegisterReply(message=f"❌ {str(e)}", success=False)

    def RecognizeFace(self, request, context):
        try:
            # Decode base64
            image_bytes = base64.b64decode(request.image)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("❌ Gambar tidak valid atau gagal didecode")

            # Simpan ke folder: engine/images/recognized_faces
            folder_path = os.path.join("engine", "images", "recognized_faces")
            os.makedirs(folder_path, exist_ok=True)
            filename = f"recognized_{int(time.time())}.jpg"
            temp_path = os.path.join(folder_path, filename)
            cv2.imwrite(temp_path, img)

            result = recognize.recognize_face(temp_path)
            return face_recognition_pb2.RecognizeReply(message=result, success=True)

        except Exception as e:
            return face_recognition_pb2.RecognizeReply(message=f"❌ {str(e)}", success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    face_recognition_pb2_grpc.add_FaceRecognitionServicer_to_server(FaceRecognitionServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("🚀 gRPC Python Engine is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
