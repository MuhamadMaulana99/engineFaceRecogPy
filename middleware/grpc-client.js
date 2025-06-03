const path = require("path");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const PROTO_PATH = path.join(__dirname, "../engine/face_recognition.proto");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const faceProto = grpc.loadPackageDefinition(packageDefinition).face;

const client = new faceProto.FaceRecognition(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

module.exports = client;
