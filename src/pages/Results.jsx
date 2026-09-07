import { useLocation, useNavigate } from "react-router-dom";
import ComplianceCard from "../components/ComplianceCard";

function Results() {
  const navigate = useNavigate();
  const location = useLocation();

  const productCount = location.state?.productCount || 1;

  const scores = [82, 65, 94, 48, 76, 91, 55, 88, 42, 97];

  const statuses = [
    "PASS",
    "UNCERTAIN",
    "PASS",
    "FAIL",
    "UNCERTAIN",
    "PASS",
    "UNCERTAIN",
    "PASS",
    "FAIL",
    "PASS",
  ];

  const products = Array.from({ length: productCount }, (_, i) => ({
    number: i + 1,
    score: scores[i] || 70,
    status: statuses[i] || "PASS",
  }));

  const getScoreStyle = (score) => {
    if (score >= 80) {
      return {
        background: "#22c55e",
        color: "white",
      };
    }

    if (score >= 50) {
      return {
        background: "#eab308",
        color: "white",
      };
    }

    return {
      background: "#ef4444",
      color: "white",
    };
  };

  const getStatusStyle = (status) => {
    if (status === "PASS") {
      return {
        background: "#dcfce7",
        color: "#166534",
      };
    }

    if (status === "FAIL") {
      return {
        background: "#fee2e2",
        color: "#991b1b",
      };
    }

    return {
      background: "#fef9c3",
      color: "#854d0e",
    };
  };

  const getChecks = (number) => {
    if (number % 2 === 1) {
      return [
        ["Product Name", "PASS"],
        ["Net Quantity", "PASS"],
        ["Country of Origin", "FAIL"],
        ["Packing Date", "UNCERTAIN"],
        ["Expiry Date", "PASS"],
        ["MRP", "PASS"],
      ];
    }

    return [
      ["Product Name", "PASS"],
      ["Net Quantity", "FAIL"],
      ["Country of Origin", "UNCERTAIN"],
      ["Packing Date", "PASS"],
      ["MRP", "FAIL"],
    ];
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#eef6ff",
        padding: "20px",
        boxSizing: "border-box",
      }}
    >
      {/* Heading */}
      <div
        style={{
          textAlign: "center",
          marginBottom: "20px",
        }}
      >
        <h1
          style={{
            margin: "5px 0",
            fontSize: "30px",
            color: "#1e3a8a",
          }}
        >
          📊 Compliance Results
        </h1>

        <p
          style={{
            margin: "5px",
            fontSize: "14px",
            color: "#64748b",
          }}
        >
          {productCount} product{productCount > 1 ? "s" : ""} analyzed
        </p>
      </div>

      {/* Products */}
      <div
        style={{
          maxWidth: "900px",
          margin: "0 auto",
        }}
      >
        {products.map((product) => (
          <div
            key={product.number}
            style={{
              background: "#ffffff",
              borderRadius: "16px",
              padding: "18px 22px",
              marginBottom: "18px",
              boxShadow: "0 3px 12px rgba(0,0,0,0.08)",
              boxSizing: "border-box",
            }}
          >
            {/* Product title */}
            <h2
              style={{
                textAlign: "center",
                color: "#1e3a8a",
                fontSize: "22px",
                margin: "0 0 8px",
              }}
            >
              📦 Product {product.number}
            </h2>

            {/* Score */}
            <div
              style={{
                textAlign: "center",
                marginBottom: "8px",
              }}
            >
              <div
                style={{
                  fontSize: "13px",
                  fontWeight: "bold",
                  marginBottom: "4px",
                }}
              >
                Compliance Score
              </div>

              <div
                style={{
                  ...getScoreStyle(product.score),
                  width: "105px",
                  height: "58px",
                  margin: "0 auto 6px",
                  borderRadius: "9px",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <strong style={{ fontSize: "20px" }}>
                  {product.score}/100
                </strong>

                <span
                  style={{
                    fontSize: "9px",
                    fontWeight: "bold",
                  }}
                >
                  {product.score >= 80
                    ? "HIGH"
                    : product.score >= 50
                    ? "PARTIAL"
                    : "LOW"}
                </span>
              </div>

              <span
                style={{
                  ...getStatusStyle(product.status),
                  display: "inline-block",
                  padding: "5px 12px",
                  borderRadius: "15px",
                  fontSize: "11px",
                  fontWeight: "bold",
                }}
              >
                {product.status}
              </span>
            </div>

            {/* Compliance checks */}
            <h3
              style={{
                fontSize: "15px",
                margin: "10px 0 5px",
              }}
            >
              Compliance Checks
            </h3>

            {getChecks(product.number).map(([name, status]) => (
              <ComplianceCard
                key={name}
                check={{
                  name: name,
                  status: status,
                }}
              />
            ))}
          </div>
        ))}

        {/* New Scan */}
        <button
          onClick={() => navigate("/scanner")}
          style={{
            width: "100%",
            padding: "13px",
            marginBottom: "20px",
            fontSize: "16px",
            fontWeight: "bold",
            borderRadius: "10px",
            background: "#2563eb",
            color: "white",
          }}
        >
          🔄 New Scan
        </button>
      </div>
    </div>
  );
}

export default Results;