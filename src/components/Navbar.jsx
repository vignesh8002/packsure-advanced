import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();

  let textColor = "#7e22ce";

  // Scanner + Analysing → Blue
  if (
    location.pathname === "/scanner" ||
    location.pathname === "/processing"
  ) {
    textColor = "#2563eb";
  }

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "15px 25px",
        background: "#ffffff",
        borderBottom: "1px solid #e2e8f0",
      }}
    >
      <Link
        to="/"
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          textDecoration: "none",
          fontSize: "22px",
          fontWeight: "bold",
        }}
      >
        {/* BOX LOGO - SANDAL COLOUR ONLY */}
        <span
          style={{
            fontSize: "22px",
            color: "#b8956a",
          }}
        >
          📦
        </span>

        {/* PACKSURE TEXT */}
        {location.pathname === "/results" ? (
          <span
            style={{
              background:
                "linear-gradient(90deg, #16a34a, #ec4899, #eab308)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
            }}
          >
            PACKSURE
          </span>
        ) : (
          <span style={{ color: textColor }}>
            PACKSURE
          </span>
        )}
      </Link>
    </nav>
  );
}

export default Navbar;