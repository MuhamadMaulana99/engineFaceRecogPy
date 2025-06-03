const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const client = require("../grpc-client");
// const { getDistanceFromLatLonInM } = require("../helper");

const router = express.Router();
const upload = multer({ dest: path.join(__dirname, "../uploads/") });

const allowedMimeTypes = ["image/jpeg", "image/jpg", "image/png"];
const kantor = { lat: -6.1754, lon: 106.8272 }; // Lokasi kantor (Monas)
const maxRadius = 100; // meter


// ========== REGISTER ==========
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
      return res.json({ success: true, message: "Wajah berhasil diregistrasi.", data: response });
    });
  } catch (err) {
    if (fs.existsSync(imagePath)) fs.unlinkSync(imagePath);
    return res.status(500).json({ error: "Gagal membaca file gambar." });
  }
});

// ========== RECOGNIZE + VALIDASI LOKASI ==========
router.post("/recognize", upload.single("photo"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "File tidak ditemukan." });
  }

  if (!allowedMimeTypes.includes(req.file.mimetype)) {
    fs.unlinkSync(req.file.path);
    return res.status(400).json({ error: "Hanya file gambar (JPG, JPEG, PNG) yang diperbolehkan." });
  }

  const { latitude, longitude } = req.body;
  if (!latitude || !longitude) {
    fs.unlinkSync(req.file.path);
    return res.status(400).json({ error: "Latitude dan longitude wajib dikirim." });
  }

  const userLat = parseFloat(latitude);
  const userLong = parseFloat(longitude);

  const kantorLat = -6.200000; // contoh latitude kantor
  const kantorLong = 106.816666; // contoh longitude kantor
  const radiusMaksimum = 100; // dalam meter

  const getDistanceFromLatLonInMeters = (lat1, lon1, lat2, lon2) => {
    const R = 6371e3; // radius bumi dalam meter
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
      Math.cos(φ1) * Math.cos(φ2) *
      Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c; // dalam meter
  };

  const distance = getDistanceFromLatLonInMeters(userLat, userLong, kantorLat, kantorLong);

  if (distance > radiusMaksimum) {
    fs.unlinkSync(req.file.path);
    return res.status(400).json({
      success: false,
      message: `❌ Lokasi kamu di luar area kantor (jarak: ${distance.toFixed(2)} meter).`,
    });
  }

  // Lokasi valid, lanjut ke pengecekan wajah
  try {
    const imageData = fs.readFileSync(req.file.path);
    const base64Image = imageData.toString("base64");

    client.RecognizeFace({ image: base64Image }, (err, response) => {
      fs.unlinkSync(req.file.path);

      if (err) {
        return res.status(500).json({ error: err.message });
      }

      const recognizedMessage = response?.message?.toLowerCase() || "";

      if (recognizedMessage.includes("tidak dikenali")) {
        return res.status(400).json({
          success: false,
          message: `❌ Wajah tidak dikenali. Jarak dari kantor: ${distance.toFixed(2)} meter.`,
          recognized: response,
        });
      }

      // Lokasi dan wajah valid ✅
      return res.json({
        success: true,
        message: `✅ Absensi berhasil. Jarak kamu dari kantor: ${distance.toFixed(2)} meter.`,
        recognized: response,
      });
    });
  } catch (err) {
    if (fs.existsSync(req.file.path)) fs.unlinkSync(req.file.path);
    return res.status(500).json({ error: "Gagal membaca file gambar." });
  }
});

module.exports = router;
