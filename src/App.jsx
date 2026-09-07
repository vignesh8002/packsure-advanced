import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Navbar from "./components/Navbar";
import Scanner from "./pages/Scanner";
import Results from "./pages/Results";
import Processing from "./pages/Processing";

function Home() {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Hero Section */}
      <section
        style={{
          padding: "70px 20px 50px",
          textAlign: "center",
          background:
            "linear-gradient(135deg, #dbeafe 0%, #eff6ff 50%, #ffffff 100%)",
        }}
      >
        <div
          style={{
            fontSize: "60px",
            marginBottom: "10px",
          }}
        >
          📦
        </div>

        <h1
          style={{
            fontSize: "42px",
            margin: "10px 0",
            color: "#1e3a8a",
          }}
        >
          PACKSURE 
        </h1>

        <p
          style={{
            fontSize: "20px",
            color: "#475569",
            margin: "10px auto",
            maxWidth: "600px",
            lineHeight: "1.6",
          }}
        >
          Smart Packaged Product Compliance Checker
        </p>

        <p
          style={{
            fontSize: "16px",
            color: "#64748b",
            maxWidth: "600px",
            margin: "15px auto 30px",
            lineHeight: "1.7",
          }}
        >
          Scan or upload a packaged product image to check
          Legal Metrology compliance.
        </p>

        {/* Buttons */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "15px",
            flexWrap: "wrap",
          }}
        >
          <Link to="/scanner" style={{ textDecoration: "none" }}>
            <button
              style={{
                width: "220px",
                padding: "16px",
                fontSize: "17px",
                fontWeight: "bold",
                background: "#2563eb",
                borderRadius: "12px",
                boxShadow: "0 5px 15px rgba(37, 99, 235, 0.25)",
              }}
            >
              📷 Scan Product
            </button>
          </Link>

          <Link to="/scanner" style={{ textDecoration: "none" }}>
            <button
              style={{
                width: "220px",
                padding: "16px",
                fontSize: "17px",
                fontWeight: "bold",
                background: "#ffffff",
                color: "#2563eb",
                border: "2px solid #2563eb",
                borderRadius: "12px",
              }}
            >
              🖼️ Upload Image
            </button>
          </Link>
        </div>
      </section>

      {/* Main Content */}
      <main
        style={{
          flex: 1,
          maxWidth: "900px",
          width: "100%",
          margin: "0 auto",
          padding: "45px 20px",
        }}
      >
        <h2
          style={{
            textAlign: "center",
            color: "#1e293b",
            marginBottom: "10px",
          }}
        >
          ⚖️ What PACKSURE Checks
        </h2>

        <p
          style={{
            textAlign: "center",
            color: "#64748b",
            marginBottom: "30px",
          }}
        >
          Important information displayed on packaged products
        </p>

        {/* Check Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "18px",
          }}
        >
          <div
            style={{
              background: "#ffffff",
              padding: "25px 20px",
              borderRadius: "16px",
              textAlign: "center",
              boxShadow: "0 5px 20px rgba(0,0,0,0.08)",
            }}
          >
            <div style={{ fontSize: "35px" }}>🏷️</div>
            <h3>Product Name</h3>
            <p style={{ color: "#64748b" }}>
              Checks whether the product name is mentioned.
            </p>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "25px 20px",
              borderRadius: "16px",
              textAlign: "center",
              boxShadow: "0 5px 20px rgba(0,0,0,0.08)",
            }}
          >
            <div style={{ fontSize: "35px" }}>⚖️</div>
            <h3>Net Quantity</h3>
            <p style={{ color: "#64748b" }}>
              Checks whether the net quantity is available.
            </p>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "25px 20px",
              borderRadius: "16px",
              textAlign: "center",
              boxShadow: "0 5px 20px rgba(0,0,0,0.08)",
            }}
          >
            <div style={{ fontSize: "35px" }}>🌍</div>
            <h3>Country of Origin</h3>
            <p style={{ color: "#64748b" }}>
              Checks country of origin information.
            </p>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "25px 20px",
              borderRadius: "16px",
              textAlign: "center",
              boxShadow: "0 5px 20px rgba(0,0,0,0.08)",
            }}
          >
            <div style={{ fontSize: "35px" }}>📅</div>
            <h3>Packing Date</h3>
            <p style={{ color: "#64748b" }}>
              Checks whether packing date is available.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer
        style={{
          textAlign: "center",
          padding: "22px",
          background: "#1e3a8a",
          color: "#ffffff",
        }}
      >
        <p style={{ margin: 0 }}>
          PACKSURE  • Legal Metrology Compliance
        </p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/scanner" element={<Scanner />} />
        <Route path="/processing" element={<Processing />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;