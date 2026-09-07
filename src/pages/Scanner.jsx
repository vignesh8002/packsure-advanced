import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Camera from "../components/Camera";
import ImageUpload from "../components/ImageUpload";

function dataUrlToFile(dataUrl, index) {
  const [header, encoded] = dataUrl.split(",");
  const mime = header.match(/data:(.*?);base64/)?.[1] || "image/jpeg";
  const binary = atob(encoded);
  const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
  return new File([bytes], `camera-product-${index + 1}.jpg`, { type: mime });
}

function Scanner() {
  const navigate = useNavigate();
  const [cameraImages, setCameraImages] = useState([]);
  const [uploadImages, setUploadImages] = useState([]);

  const handleAnalyzeScanned = () => {
    if (cameraImages.length === 0) {
      alert("Please scan at least one product.");
      return;
    }

    navigate("/processing", {
      state: {
        files: cameraImages.map((image, index) =>
          typeof image === "string" ? dataUrlToFile(image, index) : image.file
        ),
      },
    });
  };

  const handleAnalyzeUploaded = () => {
    if (uploadImages.length === 0) {
      alert("Please choose at least one product image.");
      return;
    }

    navigate("/processing", {
      state: { files: uploadImages.map((image) => image.file) },
    });
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        maxWidth: "900px",
        margin: "0 auto",
        padding: "30px 20px",
        boxSizing: "border-box",
      }}
    >
      <div style={{ textAlign: "center", marginBottom: "25px" }}>
        <div style={{ fontSize: "50px" }}>📦</div>

        {/* PACKSURE - BLUE */}
        <h1 style={{ color: "#2563eb", margin: "5px 0" }}>
          PACKSURE
        </h1>

        <h2 style={{ color: "#1e3a8a" }}>
          Scan Your Products
        </h2>

        <p style={{ color: "#64748b", fontSize: "17px" }}>
          Scan products using camera or choose product images
        </p>
      </div>

      <div
        style={{
          background: "#ffffff",
          padding: "25px",
          borderRadius: "18px",
          marginBottom: "25px",
          boxShadow: "0 5px 20px rgba(0,0,0,0.08)",
        }}
      >
        <Camera onImagesChange={setCameraImages} />

        <button
          onClick={handleAnalyzeScanned}
          disabled={cameraImages.length === 0}
          style={{
            width: "100%",
            marginTop: "20px",
            padding: "16px",
            fontSize: "17px",
            fontWeight: "bold",
            borderRadius: "12px",
            border: "none",
            background:
              cameraImages.length === 0 ? "#cbd5e1" : "#2563eb",
            color: "#ffffff",
            cursor:
              cameraImages.length === 0
                ? "not-allowed"
                : "pointer",
          }}
        >
          🔍 Analyze Scanned Products ({cameraImages.length})
        </button>
      </div>

      <div
        style={{
          background: "#ffffff",
          padding: "25px",
          borderRadius: "18px",
          marginBottom: "25px",
          boxShadow: "0 5px 20px rgba(0,0,0,0.08)",
        }}
      >
        <ImageUpload onImagesChange={setUploadImages} />

        <button
          onClick={handleAnalyzeUploaded}
          disabled={uploadImages.length === 0}
          style={{
            width: "100%",
            marginTop: "20px",
            padding: "16px",
            fontSize: "17px",
            fontWeight: "bold",
            borderRadius: "12px",
            border: "none",
            background:
              uploadImages.length === 0 ? "#cbd5e1" : "#2563eb",
            color: "#ffffff",
            cursor:
              uploadImages.length === 0
                ? "not-allowed"
                : "pointer",
          }}
        >
          🔍 Analyze Uploaded Products ({uploadImages.length})
        </button>
      </div>
    </div>
  );
}

export default Scanner;