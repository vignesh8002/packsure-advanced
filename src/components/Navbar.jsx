import { Link } from "react-router-dom";

function Navbar() {
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
          textDecoration: "none",
          fontSize: "22px",
          fontWeight: "bold",
          color: "#2563eb",
        }}
      >
        📦 PACKSURE 
      </Link>

      
    </nav>
  );
}

export default Navbar;