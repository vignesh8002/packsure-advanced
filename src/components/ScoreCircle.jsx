function ScoreCircle({ score }) {
  let status = "LOW";

  if (score >= 80) {
    status = "HIGH";
  } else if (score >= 50) {
    status = "PARTIAL";
  }

  return (
    <div
      style={{
        width: "160px",
        height: "160px",
        borderRadius: "50%",
        border: "10px solid #2563eb",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        margin: "20px auto",
        background: "#ffffff",
      }}
    >
      <strong style={{ fontSize: "32px" }}>{score}</strong>
      <span>/100</span>
      <small>{status}</small>
    </div>
  );
}

export default ScoreCircle;