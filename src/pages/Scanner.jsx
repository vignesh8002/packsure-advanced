import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Camera from "../components/Camera";
import ImageUpload from "../components/ImageUpload";

function Scanner() {
  const navigate = useNavigate();

  const [cameraImages, setCameraImages] = useState([]);
  const [uploadImages, setUploadImages] = useState([]);

  // Scan images analyze
  const handleAnalyzeScanned = () => {
    if (cameraImages.length === 0) {
      alert("Please scan at least one product.");
      return;
    }

    navigate("/processing", {
      state: {
        productCount: cameraImages.length,
      },
    });
  };

  // Uploaded images analyze
  const handleAnalyzeUploaded = () => {
    if (uploadImages.length === 0) {
      alert("Please choose at least one product image.");
      return;
    }

    navigate("/processing", {
      state: {
        productCount: uploadImages.length,
      },
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
      {/* PAGE TITLE */}
      <div
        style={{
          textAlign: "center",
          marginBottom: "25px",
        }}
      >
        <div style={{ fontSize: "50px" }}>📦</div>

        <h1 style={{ color: "#1e3a8a", margin: "5px 0" }}>
          Scan Your Products
        </h1>

        <p
          style={{
            color: "#64748b",
            fontSize: "17px",
          }}
        >
          Scan products using camera or choose product images
        </p>
      </div>

      {/* CAMERA SECTION */}
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

        {/* ANALYZE SCANNED PRODUCTS */}
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

      {/* UPLOAD SECTION */}
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

        {/* ANALYZE UPLOADED PRODUCTS */}
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