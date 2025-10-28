from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_folder="../Frontend/build", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Rate limiter untuk cegah brute-force / spam
limiter = Limiter(get_remote_address, app=app, default_limits=["20 per minute"])


# === LOGIC SESUAI TABEL BARU ===
def predict_category(num):
    num = re.sub(r"\D", "", num)  # hapus non-digit

    # 1️⃣ Semua angka sama (contoh: 88888888)
    if re.fullmatch(r"(\d)\1{6,7}", num):
        category = "Platinum"
        sub_category = "Semua Angka Sama"
        price = "≈ 75–100 juta"

    # 2️⃣ 7–8 angka sama (contoh: 99999998)
    elif re.search(r"(\d)\1{5,6}", num):
        category = "Platinum"
        sub_category = "7–8 Angka Sama"
        price = "≈ 40–75 juta"

    # 3️⃣ Berurutan penuh / terbalik (12345678 / 87654321)
    elif re.search(r"12345678|87654321", num) or re.search(r"(0123|1234|2345|3456|4567|5678|6789|9876|8765|7654|6543)", num):
        category = "Gold"
        sub_category = "Berurutan Penuh/Terbalik"
        price = "≈ 20–40 juta"

    # 4️⃣ 6 angka sama (misal 77777123)
    elif re.search(r"(\d)\1{4,5}", num):
        category = "Gold"
        sub_category = "6 Angka Sama"
        price = "≈ 10–20 juta"

    # 5️⃣ Pola kuat (ABAB, AABB)
    elif (
        re.search(r"^(\d\d)\1{1,3}$", num)  # ABABAB atau AABB penuh
        or re.search(r"(\d{2})(\1){1,2}", num)  # dua digit berulang minimal dua kali
        or re.search(r"(\d)(\d)\1\2(\d)?$", num)  # diakhiri dengan pola kuat
    ):
        category = "Silver"
        sub_category = "Pola Kuat (ABAB/AABB)"
        price = "≈ 5–10 juta"


    # 6️⃣ 4–5 angka sama (55551234)
    elif re.search(r"(\d)\1{3,4}", num):
        category = "Silver"
        sub_category = "4–5 Angka Sama"
        price = "≈ 3–5 juta"

    # 7️⃣ Pola sedang / parsial urutan (5678, 7890, 3456, dll)
    elif re.search(r"(0123|1234|2345|3456|4567|5678|6789|7890|0987|9876|8765|7654|6543)", num):
        category = "Bronze"
        sub_category = "Pola Sedang/Parsial Urutan"
        price = "≈ 1–3 juta"

    # 8️⃣ Tidak punya pola khusus
    else:
        category = "Standard"
        sub_category = "Tidak Ada Pola"
        price = "< 1 juta"

    # Confidence per tier
    confidence_map = {
        "Platinum": 1.00,
        "Gold": 0.85,
        "Silver": 0.65,
        "Bronze": 0.45,
        "Standard": 0.3
    }
    confidence = confidence_map.get(category, 0.3)

    return {
        "category": category,
        "sub_category": sub_category,
        "confidence": confidence,
        "estimated_price": price
    }


# === API Endpoint ===
@app.route("/api/checkNumber", methods=["POST"])
@limiter.limit("10 per minute")
def check_number():
    data = request.get_json()
    num = data.get("number", "")

    # Validasi format input (7–8 angka)
    if not re.match(r"^\d{7,8}$", num):
        return jsonify({"error": "Nomor harus berisi 7–8 digit angka."}), 400

    result = predict_category(num)
    return jsonify(result), 200


# === Serve React Build ===
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

# === Run Server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
