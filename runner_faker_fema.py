import os
import time
import datetime
import requests
import psutil
from faker import Faker

fake = Faker()
RENDER_URL = "https://fema-product.onrender.com/generate-fema-pdf/"
 # Replace with your actual URL
OUTPUT_DIR = "rendered_fema_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_dummy_data():
    return {
        "duty": fake.word(),
        "invoice": fake.bothify(text="INV-####"),
        "quota": fake.word(),
        "others": fake.sentence(nb_words=3),
        "exporter_name": fake.company(),
        "person_name": fake.name(),
        "person_designation": fake.job(),
        "division_head": fake.name(),
        "broker_name": fake.name(),
        "broker_designation": fake.job(),
        "identity_card": fake.bothify(text="ID-#####"),
        "date": fake.date(),
        "company_name": fake.company(),
        "duty_draw": fake.word(),
        "signatory": fake.name()
    }

for i in range(1, 51):
    start_time = time.time()
    payload = generate_dummy_data()

    try:
        response = requests.post(RENDER_URL, data=payload)
        if response.status_code == 200:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filepath = os.path.join(OUTPUT_DIR, f"fema_certificate_{i}_{timestamp}.pdf")
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"✅ [{i}] PDF Generated: {filepath}")
        else:
            print(f"❌ [{i}] Failed - Status Code {response.status_code}")
    except Exception as e:
        print(f"❌ [{i}] Exception: {e}")

    elapsed = round(time.time() - start_time, 2)
    print(f"   CPU: {psutil.cpu_percent()}% | MEM: {psutil.virtual_memory().percent}% | Time: {elapsed}s")
    print("-" * 40)
    time.sleep(1)

print("🎉 All FEMA Certificate PDFs generated!")
