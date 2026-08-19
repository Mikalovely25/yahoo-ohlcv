import requests
import sqlite3
import datetime
import time

DB = "stocks.db"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Baca daftar ticker
with open("tickers.txt", "r") as file:
    tickers = [
        line.strip().upper()
        for line in file
        if line.strip()
    ]

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ohlcv (
    ticker TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    PRIMARY KEY (ticker, date)
)
""")

for ticker in tickers:

    print()
    print("Mengambil:", ticker)

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

    params = {
        "range": "1y",
        "interval": "1d"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            print("Gagal:", response.status_code)
            continue

        result = response.json()["chart"]["result"]

        if not result:
            print("Data tidak ditemukan")
            continue

        data = result[0]

        timestamps = data["timestamp"]
        quote = data["indicators"]["quote"][0]

        for i in range(len(timestamps)):

            if quote["open"][i] is None:
                continue

            date = datetime.datetime.fromtimestamp(
                timestamps[i]
            ).strftime("%Y-%m-%d")

            cursor.execute("""
            INSERT OR REPLACE INTO ohlcv
            (ticker, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ticker.replace(".JK", ""),
                date,
                quote["open"][i],
                quote["high"][i],
                quote["low"][i],
                quote["close"][i],
                quote["volume"][i]
            ))

        conn.commit()

        print("✓ Berhasil:", ticker)

        time.sleep(2)

    except Exception as e:
        print("✗ Error:", e)

conn.close()

print()
print("=== UPDATE DATABASE SELESAI ===")
