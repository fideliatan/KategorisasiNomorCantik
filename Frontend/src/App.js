import React, { useState } from "react";
import "./App.css";

function App() {
  const [number, setNumber] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [category, setCategory] = useState("");
  const [biayaList, setBiayaList] = useState([]);

  // Data tabel biaya PSB
  const biayaData = [
    { kategori: 1, nama: "Biaya PSB Tunai Didepan PSTN Kategori 1", nominal: 20000000 },
    { kategori: 2, nama: "Biaya PSB Tunai Didepan PSTN Kategori 2", nominal: 19000000 },
    { kategori: 3, nama: "Biaya PSB Tunai Didepan PSTN Kategori 3", nominal: 18000000 },
    { kategori: 4, nama: "Biaya PSB Tunai Didepan PSTN Kategori 4", nominal: 17000000 },
    { kategori: 5, nama: "Biaya PSB Tunai Didepan PSTN Kategori 5", nominal: 16000000 },
    { kategori: 6, nama: "Biaya PSB Tunai Didepan PSTN Kategori 6", nominal: 15500000 },
    { kategori: 7, nama: "Biaya PSB Tunai Didepan PSTN Kategori 7", nominal: 14000000 },
    { kategori: 8, nama: "Biaya PSB Tunai Didepan PSTN Kategori 8", nominal: 13000000 },
    { kategori: 9, nama: "Biaya PSB Tunai Didepan PSTN Kategori 9", nominal: 12000000 },
    { kategori: 10, nama: "Biaya PSB Tunai Didepan PSTN Kategori 10", nominal: 11000000 },
    { kategori: 11, nama: "Biaya PSB Tunai Didepan PSTN Kategori 11", nominal: 10000000 },
    { kategori: 12, nama: "Biaya PSB Tunai Didepan PSTN Kategori 12", nominal: 9000000 },
    { kategori: 13, nama: "Biaya PSB Tunai Didepan PSTN Kategori 13", nominal: 8000000 },
    { kategori: 14, nama: "Biaya PSB Tunai Didepan PSTN Kategori 14", nominal: 7000000 },
    { kategori: 15, nama: "Biaya PSB Tunai Didepan PSTN Kategori 15", nominal: 6000000 },
    { kategori: 16, nama: "Biaya PSB Tunai Didepan PSTN Kategori 16", nominal: 5000000 },
    { kategori: 17, nama: "Biaya PSB Tunai Didepan PSTN Kategori 17", nominal: 4000000 },
    { kategori: 18, nama: "Biaya PSB Tunai Didepan PSTN Kategori 18", nominal: 3000000 },
    { kategori: 19, nama: "Biaya PSB Tunai Didepan PSTN Kategori 19", nominal: 2000000 },
    { kategori: 20, nama: "Biaya PSB Tunai Didepan PSTN Kategori 20", nominal: 1000000 },
    { kategori: 21, nama: "Biaya PSB Tunai Didepan PSTN Kategori 21", nominal: 500000 },
  ];

const checkCategory = async (num) => {
  try {
    const res = await fetch("http://localhost:5000/api/checkNumber", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ number: num }),
  });


    const data = await res.json();
    console.log("AI Result:", data);

    const cat = data.category;
    const confidence = data.confidence;

    let label = `${cat} (Confidence ${Math.round(confidence * 100)}%)`;

    if (cat === "Platinum") {
      setCategory(`${label} – Kategori 1–3`);
      setBiayaList(biayaData.filter((b) => b.kategori >= 1 && b.kategori <= 3));
    } else if (cat === "Gold") {
      setCategory(`${label} – Kategori 4–7`);
      setBiayaList(biayaData.filter((b) => b.kategori >= 4 && b.kategori <= 7));
    } else if (cat === "Silver") {
      setCategory(`${label} – Kategori 8–12`);
      setBiayaList(biayaData.filter((b) => b.kategori >= 8 && b.kategori <= 12));
    } else if (cat === "Classic") {
      setCategory(`${label} – Kategori 13–17`);
      setBiayaList(biayaData.filter((b) => b.kategori >= 13 && b.kategori <= 17));
    } else {
      setCategory(`${label} – Kategori 18–21`);
      setBiayaList(biayaData.filter((b) => b.kategori >= 18 && b.kategori <= 21));
    }
  } catch (err) {
    console.error("Error connecting to API:", err);
    alert("Gagal menghubungkan ke server AI.");
  }
};

  const handleSubmit = () => {
    if (number.length >= 7 && number.length <= 8) {
      checkCategory(number);
      setShowResult(true);
    } else {
      alert("Nomor harus berisi 7-8 angka.");
    }
  };

  return (
    <div className="homepage">
      <img src={`${process.env.PUBLIC_URL}/Background.png`} alt="Background" className="bg-img"/>

      <div className="header">
        <img src={`${process.env.PUBLIC_URL}/Danantara_Indonesia.png`} alt="Danantara" className="logo danantara"/>
        <img src={`${process.env.PUBLIC_URL}/logo_telkom_indonesia.png`} alt="Telkom Indonesia" className="logo telkom"/>
      </div>

      <div className="form-box">
        <h2>Kategorisasi Nomor Cantik</h2>

        <label>Masukkan No. PTSN (Tanpa Kode Area)</label>
        <input
          type="text"
          placeholder="Cth: 80005000"
          value={number}
          onChange={(e) => setNumber(e.target.value.replace(/\D/g, ""))}
        />
        <p className="note">*Harus berisikan 7–8 angka</p>

        {!showResult ? (
          <button onClick={handleSubmit}>Lanjut</button>
        ) : (
          <>
            <label>Kategori</label>
            <div className={`category-box ${category.toLowerCase().split(" ")[0]}`}>
              {category}
            </div>

            <label>Nominal Harga Biaya</label>
            <table className="biaya-table">
              <thead>
                <tr>
                  <th>Fitur</th>
                  <th>Nominal</th>
                </tr>
              </thead>
              <tbody>
                {biayaList.map((item) => (
                  <tr key={item.kategori}>
                    <td>{item.nama}</td>
                    <td>Rp. {item.nominal.toLocaleString("id-ID")}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <button onClick={() => window.location.reload()}>Kembali</button>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
