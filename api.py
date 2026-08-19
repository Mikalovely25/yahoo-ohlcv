from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DB = "stocks.db"

@app.route("/")
def home():
    return "Stock API is running!"

@app.route("/api/<ticker>")
def stock(ticker):

    ticker = ticker.upper()

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT ticker, date, open, high, low, close, volume
        FROM ohlcv
        WHERE ticker = ?
        ORDER BY date DESC
        LIMIT 30
    """, (ticker,))

    rows = cursor.fetchall()

    conn.close()

    data = [dict(row) for row in rows]

    return jsonify(data)

app.run(
    host="0.0.0.0",
    port=5000
)
