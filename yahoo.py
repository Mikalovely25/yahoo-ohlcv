import requests
import csv
import datetime
import time
import os

# Baca daftar ticker
with open("tickers.txt", "r") as file:
    tickers = [line.strip().upper() for line in file if line.strip()]

period = "1y"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Buat folder data kalau belum ada
os.makedirs("data", exist_ok=True)

for ticker in tickers:

    print()
    print("Mengambil:", ticker)

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

    params = {
        "range": period,
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

        filename = f"data/{ticker.replace('.JK', '')}.csv"

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ])

            for i in range(len(timestamps)):

                writer.writerow([
                    datetime.datetime.fromtimestamp(
                        timestamps[i]
                    ).strftime("%Y-%m-%d"),

                    quote["open"][i],
                    quote["high"][i],
                    quote["low"][i],
                    quote["close"][i],
                    quote["volume"][i]
                ])

        print("✓ Berhasil:", filename)

        time.sleep(2)

    except Exception as e:
        print("✗ Error:", e)

print()
print("=== SEMUA SELESAI ===")
