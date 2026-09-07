import { useLocation, useNavigate } from "react-router-dom";
import ComplianceCard from "../components/ComplianceCard";

function Results() {
  const navigate = useNavigate();
  const location = useLocation();

  const results = location.state?.results || [];

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

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #dcfce7 0%, #fbcfe8 50%, #fef08a 100%)",
        padding: "20px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          textAlign: "center",
          marginBottom: "20px",
        }}
      >
        {/* PACKSURE - GREEN + PINK + YELLOW */}
        <h1
          style={{
            margin: "5px 0",
            fontSize: "30px",
            background:
              "linear-gradient(90deg, #16a34a, #ec4899, #eab308)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
          }}
        >
          PACKSURE
        </h1>

        <h2
          style={{
            margin: "5px 0",
            color: "#1e3a8a",
          }}
        >
          📊 Compliance Results
        </h2>

        <p
          style={{
            margin: "5px",
            fontSize: "14px",
            color: "#64748b",
          }}
        >
          {results.length} product{results.length > 1 ? "s" : ""} analyzed
        </p>
      </div>

      <div
        style={{
          maxWidth: "900px",
          margin: "0 auto",
        }}
      >
        {results.map((response, index) => {
          const result = response?.result || {};
          const summary = result.compliance?.summary || {};
          const score = Number(summary.score ?? 0);
          const status = summary.overall || "UNKNOWN";
          const rules = Array.isArray(result.compliance?.rules)
            ? result.compliance.rules
            : [];
          const entities = result.entities || {};
          return (
          <div
            key={response.scan_id || index}
            style={{
              background: "#ffffff",
              borderRadius: "16px",
              padding: "18px 22px",
              marginBottom: "18px",
              boxShadow:
                "0 3px 12px rgba(0,0,0,0.08)",
              boxSizing: "border-box",
            }}
          >
            <h2
              style={{
                textAlign: "center",
                color: "#1e3a8a",
                fontSize: "22px",
                margin: "0 0 8px",
              }}
            >
              📦 Product {index + 1}
            </h2>

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
                  ...getScoreStyle(score),
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
                  {score}/100
                </strong>

                <span
                  style={{
                    fontSize: "9px",
                    fontWeight: "bold",
                  }}
                >
                  {score >= 80
                    ? "HIGH"
                    : score >= 50
                    ? "PARTIAL"
                    : "LOW"}
                </span>
              </div>

              <span
                style={{
                  ...getStatusStyle(status),
                  display: "inline-block",
                  padding: "5px 12px",
                  borderRadius: "15px",
                  fontSize: "11px",
                  fontWeight: "bold",
                }}
              >
                {status}
              </span>
            </div>

            <h3
              style={{
                fontSize: "15px",
                margin: "10px 0 5px",
              }}
            >
              Compliance Checks
            </h3>
            <p>
              {summary.passed ?? 0} passed, {summary.failed ?? 0} failed,{" "}
              {summary.review ?? 0} requiring review
            </p>

            {rules.map((rule, ruleIndex) => (
                <ComplianceCard
                  key={`${rule.rule_no}-${ruleIndex}`}
                  check={{
                    name: rule.requirement || rule.rule_no || "Compliance rule",
                    status: rule.status || "UNKNOWN",
                    message: rule.observation,
                  }}
                />
            ))}

            <h3 style={{ fontSize: "15px", margin: "10px 0 5px" }}>
              Extracted Information
            </h3>
            <p><strong>OCR:</strong> {result.ocr?.full_text || "No text detected."}</p>
            <p><strong>Languages:</strong> {result.detected_languages?.join(", ") || "Not detected"}</p>
            <p><strong>Entities:</strong> {Object.entries(entities)
              .filter(([, value]) => value)
              .map(([key, value]) => `${key}: ${value}`)
              .join(" | ") || "No entities detected."}</p>
            <p><strong>Image quality:</strong> {result.quality?.quality_rating || "Unavailable"}
              {result.quality?.quality_score != null ? ` (${result.quality.quality_score}/100)` : ""}</p>
          </div>
          );
        })}

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