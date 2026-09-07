import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { processScan, uploadScan } from "../services/api";

function Processing() {
  const navigate = useNavigate();
  const location = useLocation();

  const files = location.state?.files || [];
  const productCount = files.length;

  const messages = [
    "📖 Reading product labels...",
    "🔍 Extracting text using OCR...",
    "📦 Identifying product information...",
    "⚖️ Checking legal requirements...",
  ];

  const [messageIndex, setMessageIndex] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    const messageTimer = setInterval(() => {
      setMessageIndex(
        (current) => (current + 1) % messages.length
      );
    }, 1000);

    let cancelled = false;

    async function processFiles() {
      if (files.length === 0) {
        setError("No product image was selected.");
        return;
      }

      try {
        const results = [];
        for (const file of files) {
          const upload = await uploadScan(file);
          if (!upload.scan_id) {
            throw new Error("The backend did not return a scan ID.");
          }
          const result = await processScan(upload.scan_id);
          results.push(result);
        }
        if (!cancelled) {
          navigate("/results", { state: { results } });
        }
      } catch (processingError) {
        if (!cancelled) {
          setError(processingError.message || "Unable to process the product image.");
        }
      }
    }

    processFiles();

    return () => {
      clearInterval(messageTimer);
      cancelled = true;
    };
  }, [files, navigate]);

  return (
    <div
      style={{
        minHeight: "70vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        padding: "20px",
      }}
    >
      {/* PACKSURE - BLUE */}
      <h1 style={{ color: "#2563eb" }}>
        PACKSURE
      </h1>

      <h2>{error ? "⚠️ Processing failed" : "🔍 Analyzing Products..."}</h2>

      <div style={{ fontSize: "55px", margin: "15px" }}>
        ⏳
      </div>

      {error ? (
        <p style={{ color: "#b91c1c", maxWidth: "600px" }}>{error}</p>
      ) : (
        <p style={{ fontSize: "18px" }}>{messages[messageIndex]}</p>
      )}

      <p style={{ color: "#64748b" }}>
        Analyzing {productCount} product
        {productCount > 1 ? "s" : ""}...
      </p>

      {!error && <p>Please wait...</p>}
      {error && <button onClick={() => navigate("/scanner")}>Back to Scanner</button>}
    </div>
  );
}

export default Processing;