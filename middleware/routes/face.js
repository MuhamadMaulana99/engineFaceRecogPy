const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const client = require("../grpc-client");

const router = express.Router();
const upload = multer({ dest: path.join(__dirname, "../uploads/") });

// Validasi tipe gambar
const allowedMimeTypes = ["image/jpeg", "image/jpg", "image/png"];

// Register wajah
router.post("/register", upload.single("photo"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "File tidak ditemukan." });
  }

  if (!allowedMimeTypes.includes(req.file.mimetype)) {
    fs.unlinkSync(req.file.path);
    return res.status(400).json({ error: "Hanya file gambar (JPG, JPEG, PNG) yang diperbolehkan." });
  }

  const imagePath = req.file.path;
  const name = req.body.name;

  try {
    const imageData = fs.readFileSync(imagePath);
    const base64Image = imageData.toString("base64");

    client.RegisterFace({ name, image: base64Image }, (err, response) => {
      fs.unlinkSync(imagePath);

      if (err) {
        return res.status(500).json({ error: err.message });
      }

      return res.json(response);
    });
  } catch (err) {
    if (fs.existsSync(imagePath)) fs.unlinkSync(imagePath);
    return res.status(500).json({ error: "Gagal membaca file gambar." });
  }
});

// Recognize wajah
router.post("/recognize", upload.single("photo"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "File tidak ditemukan." });
  }

  if (!allowedMimeTypes.includes(req.file.mimetype)) {
    fs.unlinkSync(req.file.path);
    return res.status(400).json({ error: "Hanya file gambar (JPG, JPEG, PNG) yang diperbolehkan." });
  }

  const imagePath = req.file.path;

  try {
    const imageData = fs.readFileSync(imagePath);
    const base64Image = imageData.toString("base64");

    client.RecognizeFace({ image: base64Image }, (err, response) => {
      fs.unlinkSync(imagePath);

      if (err) {
        return res.status(500).json({ error: err.message });
      }

      return res.json(response);
    });
  } catch (err) {
    if (fs.existsSync(imagePath)) fs.unlinkSync(imagePath);
    return res.status(500).json({ error: "Gagal membaca file gambar." });
  }
});

module.exports = router;
