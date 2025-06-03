const express = require("express");
const multer = require("multer");
const path = require("path");
const faceRoutes = require("./routes/face");

const app = express();
const PORT = 3000;

// Setup static and uploads folder
app.use("/uploads", express.static(path.join(__dirname, "../uploads")));

// Routing
app.use("/face", faceRoutes);

app.listen(PORT, () => {
  console.log(`🟢 Middleware running on http://localhost:${PORT}`);
});
