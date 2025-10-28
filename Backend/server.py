from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__, static_folder="../Frontend/build", static_url_path="/")
CORS(app)  # penting biar bisa diakses dari React (port 3000)

def predict_category(num):
    num = re.sub(r'\D', '', num)
    score = {"scarcity": 1, "pattern": 1, "memorability": 2, "lucky": 1, "uniqueness": 1}

    # === PLATINUM ===
    # Pola full angka sama (≥4x berulang) atau urutan 1234/4321/8888/9999
    if re.search(r"(\d)\1{3,}", num) or re.search(r"(1234|4321|8888|9999)", num):
        score = {"scarcity": 5, "pattern": 5, "memorability": 5, "lucky": 5, "uniqueness": 4}
        cat = "Platinum"

    # === GOLD ===
    # 3–4 angka berulang di AKHIR nomor atau pola naik/turun parsial (123, 234, 9876)
    elif (
        re.search(r"(\d)\1{2,3}$", num)  # tiga/empat angka sama di akhir
        or re.search(r"(\d{2})\1", num)  # dua digit berulang (1212, 7878)
        or re.search(r"(123|234|345|456|543|432|321|8765|9876)", num)  # urutan parsial
    ):
        score = {"scarcity": 4, "pattern": 4, "memorability": 5, "lucky": 3, "uniqueness": 3}
        cat = "Gold"

    # === SILVER ===
    # Pola setengah berulang atau ada sedikit keteraturan (naik/turun ringan)
    elif (
        re.search(r"(56|65|67|76|78|87|89|98)", num)
        or re.search(r"(\d)\d\1", num)  # pantulan seperti 818, 525
        or re.search(r"(\d)\1{2}", num)  # 3 angka sama tapi bukan di akhir
    ):
        score = {"scarcity": 3, "pattern": 3, "memorability": 4, "lucky": 3, "uniqueness": 2}
        cat = "Silver"

    # === CLASSIC ===
    elif re.search(r"19\d{2}|20\d{2}", num):
        score = {"scarcity": 2, "pattern": 2, "memorability": 3, "lucky": 2, "uniqueness": 5}
        cat = "Classic"

    # === REGULAR ===
    else:
        score = {"scarcity": 1, "pattern": 1, "memorability": 2, "lucky": 1, "uniqueness": 1}
        cat = "Regular"

    total = sum(score.values()) / 5
    confidence = round(min(1.0, total / 5), 2)

    return {"category": cat, "confidence": confidence, "score": score}

@app.route("/api/checkNumber", methods=["POST"])
def check_number():
    data = request.get_json()
    num = data.get("number", "")
    result = predict_category(num)
    return jsonify(result)

# === Serve React build ===
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# === Run server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
