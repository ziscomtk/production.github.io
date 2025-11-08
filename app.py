from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)
DATA_FILE = "attendance.json"

# โหลดข้อมูลจากไฟล์ (ถ้ามี)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# บันทึกข้อมูลลงไฟล์
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    records = load_data()
    return render_template("index.html", records=records)

@app.route("/check", methods=["POST"])
def check():
    name = request.form.get("name")
    action = request.form.get("action")  # 'in' หรือ 'out'
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = {"name": name, "action": action, "time": now}
    data = load_data()
    data.append(record)
    save_data(data)

    return jsonify({"status": "success", "record": record})

if __name__ == "__main__":
    app.run(debug=True)
