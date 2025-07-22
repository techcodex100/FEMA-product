import csv
import os
import time
import datetime
import requests
import psutil

# Configuration
INPUT_CSV = "fema_input.csv"
RENDER_URL = "https://fema-product.onrender.com/generate-fema-pdf/"
OUTPUT_DIR = "rendered_fema_pdfs"
MAX_RETRIES = 5
DELAY = 2

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read CSV and send POST requests
with open(INPUT_CSV, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader, 1):
        success = False
        start_time = time.time()

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Send POST request with form data
                response = requests.post(RENDER_URL, data=row)
                if response.status_code == 200:
                    success = True
                    break
                else:
                    print(f"[{i}] ⚠️ Attempt {attempt} failed - Status {response.status_code}")
            except Exception as e:
                print(f"[{i}] ❌ Exception: {e}")
            time.sleep(2)

        if not success:
            print(f"[{i}] ❌ Skipped after {MAX_RETRIES} attempts.")
            continue

        # Save PDF file
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"fema_certificate_{i}_{timestamp}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        # System stats
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        elapsed = round(time.time() - start_time, 2)

        print(f"✅ [{i}] PDF Generated: {filename}")
        print(f"   CPU: {cpu}% | RAM: {mem}% | Time: {elapsed}s")
        print("-" * 40)
        time.sleep(DELAY)

print("🎉 All FEMA Certificates generated successfully.")
