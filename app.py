import json
import os
import traceback
import urllib.request
from flask import Flask, jsonify, render_template

# index.html app.py bilan bir xil papkada turgani uchun yo'lni ko'rsatamiz
app = Flask(__name__, template_folder=".")

FALLBACK = {"USD": 1.0, "RUB": 85.0, "UZS": 12300.0}
cache = {"t": 0.0, "rates": FALLBACK, "live": False}

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        error_details = traceback.format_exc()
        return f"<pre style='color:red; font-size:16px;'>Xatolik yuz berdi:\n{error_details}</pre>", 500

@app.route("/api/rates")
def rates():
    if time.time() - cache["t"] > 3600:
        try:
            with urllib.request.urlopen("https://open.er-api.com/v6/latest/USD", timeout=4) as r:
                d = json.load(r)["rates"]
                cache.update(
                    t=time.time(),
                    rates={"USD": 1.0, "RUB": d.get("RUB", 85.0), "UZS": d.get("UZS", 12300.0)},
                    live=True
                )
        except Exception:
            cache["t"] = time.time() - 3300
    return jsonify(rates=cache["rates"], live=cache["live"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
