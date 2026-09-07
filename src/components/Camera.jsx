import { useEffect, useRef, useState } from "react";

function Camera({ onImagesChange }) {
  const videoRef = useRef(null);

  const [cameraOn, setCameraOn] = useState(false);
  const [stream, setStream] = useState(null);
  const [images, setImages] = useState([]);

  const MAX_PRODUCTS = 10;

  // Send images to Scanner
  useEffect(() => {
    if (onImagesChange) {
      onImagesChange(images);
    }
  }, [images, onImagesChange]);

  // Connect camera stream to video
  useEffect(() => {
    if (cameraOn && stream && videoRef.current) {
      videoRef.current.srcObject = stream;
    }
  }, [cameraOn, stream]);

  // Open camera
  const startCamera = async () => {
    try {
      const newStream =
        await navigator.mediaDevices.getUserMedia({
          video: true,
        });

      setStream(newStream);
      setCameraOn(true);
    } catch (error) {
      alert(
        "Camera Error:\n\n" +
          error.name +
          "\n" +
          error.message
      );
    }
  };

  // Capture product
  const captureImage = () => {
    if (images.length >= MAX_PRODUCTS) {
      alert("Maximum 10 products can be scanned.");
      return;
    }

    const video = videoRef.current;

    if (!video) {
      alert("Camera is not ready.");
      return;
    }

    if (video.videoWidth === 0 || video.videoHeight === 0) {
      alert("Camera is still loading. Please try again.");
      return;
    }

    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    const imageData = canvas.toDataURL("image/jpeg");

    setImages((currentImages) => [
      ...currentImages,
      imageData,
    ]);
  };

  // Delete one product
  const deleteImage = (index) => {
    setImages((currentImages) =>
      currentImages.filter((_, i) => i !== index)
    );

    // If camera was stopped because we reached 10,
    // open it again automatically after deleting.
    if (!cameraOn) {
      startCamera();
    }
  };

  // Clear all products
  const clearAll = () => {
    setImages([]);
    startCamera();
  };

  // Stop camera
  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => {
        track.stop();
      });
    }

    setStream(null);
    setCameraOn(false);
  };

  // Automatically stop camera when 10 products are reached
  useEffect(() => {
    if (images.length === MAX_PRODUCTS && cameraOn) {
      stopCamera();
    }
  }, [images.length]);

  // Cleanup camera when component is removed
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => {
          track.stop();
        });
      }
    };
  }, [stream]);

  return (
    <div style={{ textAlign: "center" }}>

      <h2>📷 Scan Products</h2>

      <p>
        Place products one by one in front of the camera.
      </p>

      <h3 style={{ color: "#2563eb" }}>
        Products Scanned: {images.length} / {MAX_PRODUCTS}
      </h3>

      {/* OPEN CAMERA BUTTON */}
      {!cameraOn && images.length < MAX_PRODUCTS && (
        <button onClick={startCamera}>
          📷 Open Camera
        </button>
      )}

      {/* CAMERA */}
      {cameraOn && images.length < MAX_PRODUCTS && (
        <div>

          <video
            ref={videoRef}
            autoPlay
            playsInline
            style={{
              width: "100%",
              maxWidth: "500px",
              borderRadius: "12px",
              marginTop: "15px",
            }}
          />

          <br />

          <button onClick={captureImage}>
            📸 Scan Product {images.length + 1}
          </button>

          <button
            onClick={stopCamera}
            style={{
              background: "#64748b",
            }}
          >
            ⏹️ Stop Camera
          </button>

        </div>
      )}

      {/* 10 PRODUCTS MESSAGE */}
      {images.length === MAX_PRODUCTS && (
        <div>
          <h2 style={{ color: "green" }}>
            ✅ 10 Products Scanned
          </h2>

          <p>
            Delete a product if you want to scan another one.
          </p>
        </div>
      )}

      {/* PRODUCT LIST */}
      {images.length > 0 && (
        <div>

          <h3>📦 Scanned Products</h3>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(150px, 1fr))",
              gap: "15px",
            }}
          >

            {images.map((image, index) => (
              <div
                key={index}
                style={{
                  border: "1px solid #ddd",
                  padding: "10px",
                  borderRadius: "12px",
                  background: "#ffffff",
                }}
              >

                <strong>
                  Product {index + 1}
                </strong>

                <img
                  src={image}
                  alt={`Product ${index + 1}`}
                  style={{
                    width: "100%",
                    marginTop: "8px",
                    borderRadius: "8px",
                  }}
                />

                <button
                  onClick={() => deleteImage(index)}
                  style={{
                    background: "#dc2626",
                    marginTop: "8px",
                  }}
                >
                  🗑️ Delete
                </button>

              </div>
            ))}

          </div>

          <br />

          <button
            onClick={clearAll}
            style={{
              background: "#64748b",
            }}
          >
            🗑️ Clear All
          </button>

        </div>
      )}

    </div>
  );
}

export default Camera;