import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (event) => {
    event.preventDefault();

    if (username.trim() === "" || password.trim() === "") {
      alert("Please enter username and password.");
      return;
    }

    navigate("/home");
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background:
          "linear-gradient(135deg, #f9b77d 0%, #93b9e8 50%, #e2e8f0 100%)",
        padding: "20px",
        boxSizing: "border-box",
        position: "relative",
        overflow: "hidden",
      }}
    >
      

      

      {/* Login Card */}
      <div
        style={{
          position: "relative",
          width: "100%",
          maxWidth: "390px",
          background: "rgba(255, 255, 255, 0.96)",
          padding: "38px 32px",
          borderRadius: "24px",
          boxShadow: "0 15px 40px rgba(30, 58, 138, 0.18)",
          boxSizing: "border-box",
          border: "1px solid rgba(255,255,255,0.8)",
        }}
      >
        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: "30px" }}>
          <div
            style={{
              width: "78px",
              height: "78px",
              margin: "0 auto 12px",
              borderRadius: "22px",
              background: "#2563eb",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "42px",
              boxShadow: "0 8px 20px rgba(37,99,235,0.25)",
            }}
          >
            📦
          </div>

          <h1
            style={{
              margin: 0,
              color: "#1e3a8a",
              fontSize: "34px",
              letterSpacing: "3px",
            }}
          >
            PACKSURE
          </h1>

          <div
            style={{
              width: "55px",
              height: "4px",
              background: "#2563eb",
              borderRadius: "5px",
              margin: "10px auto 0",
            }}
          />
        </div>

        <form onSubmit={handleLogin}>
          {/* Username */}
          <label
            style={{
              display: "block",
              marginBottom: "8px",
              color: "#334155",
              fontWeight: "bold",
            }}
          >
            👤 Username
          </label>

          <input
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Enter username"
            style={{
              width: "100%",
              padding: "14px",
              marginBottom: "20px",
              border: "1px solid #cbd5e1",
              borderRadius: "11px",
              fontSize: "15px",
              boxSizing: "border-box",
              outline: "none",
              background: "#f8fafc",
            }}
          />

          {/* Password */}
          <label
            style={{
              display: "block",
              marginBottom: "8px",
              color: "#334155",
              fontWeight: "bold",
            }}
          >
            🔒 Password
          </label>

          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter password"
            style={{
              width: "100%",
              padding: "14px",
              marginBottom: "25px",
              border: "1px solid #cbd5e1",
              borderRadius: "11px",
              fontSize: "15px",
              boxSizing: "border-box",
              outline: "none",
              background: "#f8fafc",
            }}
          />

          {/* Login Button */}
          <button
            type="submit"
            style={{
              width: "100%",
              padding: "15px",
              background: "#2563eb",
              color: "#ffffff",
              border: "none",
              borderRadius: "11px",
              fontSize: "16px",
              fontWeight: "bold",
              cursor: "pointer",
              boxShadow: "0 7px 18px rgba(37,99,235,0.25)",
            }}
          >
            🔐 LOGIN
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;