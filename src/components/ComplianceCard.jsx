function ComplianceCard({ check }) {
  let background = "#fef9c3";
  let color = "#854d0e";
  let icon = "⚠️";

  if (check.status === "PASS") {
    background = "#dcfce7";
    color = "#166534";
    icon = "✅";
  }

  if (check.status === "FAIL") {
    background = "#fee2e2";
    color = "#991b1b";
    icon = "❌";
  }

  return (
    <div
      style={{
        background: background,
        color: color,
        padding: "4px 8px",
        margin: "3px 0",
        borderRadius: "6px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        fontSize: "11px",
        height: "23px",
        boxSizing: "border-box",
      }}
    >
      <span>
        {icon} <strong>{check.name}</strong>
      </span>

      <span style={{ fontWeight: "bold" }}>
        {check.status}
      </span>
    </div>
  );
}

export default ComplianceCard;