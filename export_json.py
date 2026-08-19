import sqlite3
import json
import os

DB = "stocks.db"
OUTPUT = "data"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("""
SELECT DISTINCT ticker
FROM ohlcv
ORDER BY ticker
""")

tickers = cursor.fetchall()

os.makedirs(OUTPUT, exist_ok=True)

for row in tickers:

    ticker = row["ticker"]

    cursor.execute("""
    SELECT ticker, date, open, high, low, close, volume
    FROM ohlcv
    WHERE ticker = ?
    ORDER BY date ASC
    """, (ticker,))

    data = [dict(x) for x in cursor.fetchall()]

    filename = f"{OUTPUT}/{ticker}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print("✓", filename)

conn.close()

print("=== JSON SELESAI ===")
