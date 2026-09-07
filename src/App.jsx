import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Scanner from "./pages/Scanner";
import Processing from "./pages/Processing";
import Results from "./pages/Results";

function Home() {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        background:
          "linear-gradient(135deg, #fce7f3 0%, #ede9fe 50%, #f5f3ff 100%)",
      }}
    >
      <section style={{ padding: "70px 20px 50px", textAlign: "center" }}>
        <div style={{ fontSize: "60px" }}>📦</div>

        <h1 style={{ fontSize: "42px", color: "#581c87" }}>
          PACKSURE
        </h1>

        <p style={{ fontSize: "20px", color: "#4c1d95" }}>
          Smart Packaged Product Compliance Checker
        </p>

        <p style={{ color: "#6b21a8", maxWidth: "600px", margin: "20px auto 30px" }}>
          Scan or upload a packaged product image to check Legal Metrology compliance.
        </p>

        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "15px",
            flexWrap: "wrap",
          }}
        >
          <button
            onClick={() => (window.location.href = "/scanner")}
            style={{
              width: "220px",
              padding: "16px",
              fontSize: "17px",
              fontWeight: "bold",
              background: "#9333ea",
              color: "white",
              border: "none",
              borderRadius: "12px",
            }}
          >
            📷 Scan Product
          </button>

          <button
            onClick={() => (window.location.href = "/scanner")}
            style={{
              width: "220px",
              padding: "16px",
              fontSize: "17px",
              fontWeight: "bold",
              background: "white",
              color: "#9333ea",
              border: "2px solid #9333ea",
              borderRadius: "12px",
            }}
          >
            🖼️ Upload Image
          </button>
        </div>
      </section>

      <main
        style={{
          flex: 1,
          maxWidth: "900px",
          width: "100%",
          margin: "0 auto",
          padding: "45px 20px",
          boxSizing: "border-box",
        }}
      >
        <h2 style={{ textAlign: "center", color: "#581c87" }}>
          ⚖️ What PACKSURE Checks
        </h2>

        <p style={{ textAlign: "center", color: "#6b21a8" }}>
          Important information displayed on packaged products
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "18px",
            marginTop: "30px",
          }}
        >
          {[
            ["📦", "Product Name"],
            ["⚖️", "Net Quantity"],
            ["🌍", "Country of Origin"],
            ["📅", "Packing Date"],
          ].map(([icon, title]) => (
            <div
              key={title}
              style={{
                background: "rgba(255,255,255,0.75)",
                padding: "22px",
                borderRadius: "16px",
                textAlign: "center",
                boxShadow: "0 5px 15px rgba(88,28,135,0.10)",
              }}
            >
              <div style={{ fontSize: "35px" }}>{icon}</div>
              <h3 style={{ color: "#581c87" }}>{title}</h3>
            </div>
          ))}
        </div>
      </main>

      <footer
        style={{
          textAlign: "center",
          padding: "22px",
          background: "#581c87",
          color: "white",
        }}
      >
        PACKSURE AI • Legal Metrology Compliance
      </footer>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route
          path="/home"
          element={
            <>
              <Navbar />
              <Home />
            </>
          }
        />

        <Route
          path="/scanner"
          element={
            <>
              <Navbar />
              <Scanner />
            </>
          }
        />

        <Route
          path="/processing"
          element={
            <>
              <Navbar />
              <Processing />
            </>
          }
        />

        <Route
          path="/results"
          element={
            <>
              <Navbar />
              <Results />
            </>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;