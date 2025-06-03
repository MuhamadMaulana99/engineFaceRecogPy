from concurrent import futures
import grpc
import base64
import cv2
import numpy as np
import face_recognition_pb2
import face_recognition_pb2_grpc
import recognize
import register

class FaceRecognitionServicer(face_recognition_pb2_grpc.FaceRecognitionServicer):
    def RegisterFace(self, request, context):
        try:
            image_bytes = base64.b64decode(request.image)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            temp_path = "temp_register.jpg"
            cv2.imwrite(temp_path, img)

            result = register.register_face(temp_path, request.name)
            return face_recognition_pb2.RegisterReply(message=result, success=True)
        except Exception as e:
            return face_recognition_pb2.RegisterReply(message=f"❌ {str(e)}", success=False)

    def RecognizeFace(self, request, context):
        try:
            image_bytes = base64.b64decode(request.image)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            temp_path = "temp_recognize.jpg"
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
