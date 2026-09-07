import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function Processing() {
  const navigate = useNavigate();
  const location = useLocation();

  const productCount = location.state?.productCount || 1;

  const messages = [
    "📖 Reading product labels...",
    "🔍 Extracting text using OCR...",
    "📦 Identifying product information...",
    "⚖️ Checking legal requirements...",
  ];

  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const messageTimer = setInterval(() => {
      setMessageIndex((current) => (current + 1) % messages.length);
    }, 1000);

    const resultTimer = setTimeout(() => {
      navigate("/results", {
        state: { productCount: productCount },
      });
    }, 5000);

    return () => {
      clearInterval(messageTimer);
      clearTimeout(resultTimer);
    };
  }, [navigate, productCount]);

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
      <h1>🔍 Analyzing Products...</h1>

      <div style={{ fontSize: "55px", margin: "15px" }}>
        ⏳
      </div>

      <p style={{ fontSize: "18px" }}>
        {messages[messageIndex]}
      </p>

      <p style={{ color: "#64748b" }}>
        Analyzing {productCount} product
        {productCount > 1 ? "s" : ""}...
      </p>

      <p>Please wait...</p>
    </div>
  );
}

export default Processing;