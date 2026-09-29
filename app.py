import json
import os
import time
import urllib.request

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Zaxira kurslar (API ishlamasa sayt baribir ishlaydi)
FALLBACK = {"USD": 1.0, "RUB": 85.0, "UZS": 12300.0}
cache = {"t": 0.0, "rates": FALLBACK, "live": False}


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/rates")
def rates():
  if time.time() - cache["t"] > 3600:
    try:
      with urllib.request.urlopen(
          "https://open.er-api.com/v6/latest/USD", timeout=4
      ) as r:
        d = json.load(r)["rates"]
        cache.update(
            t=time.time(),
            rates={
                "USD": 1.0,
                "RUB": d.get("RUB", 85.0),
                "UZS": d.get("UZS", 12300.0),
            },
            live=True,
        )
    except Exception:
      cache["t"] = time.time() - 3300  # Xatolik bo'lsa zaxirada qoladi
  return jsonify(rates=cache["rates"], live=cache["live"])


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
