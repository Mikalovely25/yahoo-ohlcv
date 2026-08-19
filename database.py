import sqlite3
import csv
import os

DB = "stocks.db"

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

data_folder = "data"

for filename in os.listdir(data_folder):

    if not filename.endswith(".csv"):
        continue

    ticker = filename.replace(".csv", "").upper()

    filepath = os.path.join(data_folder, filename)

    with open(filepath, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Open"] == "" or row["Close"] == "":
                continue

            cursor.execute("""
            INSERT OR REPLACE INTO ohlcv
            (ticker, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ticker,
                row["Date"],
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"]
            ))

conn.commit()
conn.close()

print("Database berhasil dibuat!")
print("File:", DB)
