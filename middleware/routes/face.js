const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const client = require("../grpc-client");

const router = express.Router();
const upload = multer({ dest: path.join(__dirname, "../uploads/") });


// Register wajah
router.post("/register", upload.single("photo"), (req, res) => {
  const imagePath = req.file.path;
  const name = req.body.name;

  const imageData = fs.readFileSync(imagePath);
  const base64Image = imageData.toString("base64");

  client.RegisterFace({ name, image: base64Image }, (err, response) => {
    fs.unlinkSync(imagePath); // delete temp file

    if (err) {
      return res.status(500).json({ error: err.message });
    }

    return res.json(response);
  });
});

// Recognize wajah
router.post("/recognize", upload.single("photo"), (req, res) => {
  const imagePath = req.file.path;
  const imageData = fs.readFileSync(imagePath);
  const base64Image = imageData.toString("base64");

  client.RecognizeFace({ image: base64Image }, (err, response) => {
    fs.unlinkSync(imagePath);

    if (err) {
      return res.status(500).json({ error: err.message });
    }

    return res.json(response);
  });
});

module.exports = router;
