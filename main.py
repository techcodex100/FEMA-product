from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

app = FastAPI()

# ✅ Root route to avoid 404 on GET /
@app.get("/")
def read_root():
    return {"message": "FEMA Certificate PDF Generator is running 🎉"}

@app.post("/generate-fema-pdf/")
def generate_fema_pdf(
    duty: str = Form(...),
    invoice: str = Form(...),
    quota: str = Form(...),
    others: str = Form(...),
    exporter_name: str = Form(...),
    person_name: str = Form(...),
    person_designation: str = Form(...),
    division_head: str = Form(...),
    broker_name: str = Form(...),
    broker_designation: str = Form(...),
    identity_card: str = Form(...),
    date: str = Form(...),
    company_name: str = Form(...),
    duty_draw: str = Form(...),
    signatory: str = Form(...)
):
    try:
        output_path = "generated_fema_certificate.pdf"
        background_path = "static/bg.jpg"  # Background image path

        if not os.path.exists(background_path):
            raise FileNotFoundError(f"Image not found at {background_path}")

        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        # Draw background image
        c.drawImage(background_path, 0, 0, width=width, height=height)

        # Set font and color
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0, 0, 0)  # black

        # Draw strings at required coordinates
        c.drawString(350, 640, duty)
        c.drawString(400, 550, invoice)
        c.drawString(350, 515, quota)
        c.drawString(210, 470, others)
        c.drawString(170, 420, exporter_name)
        c.drawString(160, 370, person_name)
        c.drawString(90, 320, person_designation)
        c.drawString(250, 330, division_head)
        c.drawString(440, 430, broker_name)
        c.drawString(440, 380, broker_designation)
        c.drawString(440, 330, identity_card)
        c.drawString(120, 185, date)
        c.drawString(200, 165, company_name)
        c.drawString(200, 100, signatory)
        c.drawString(440, 470, duty_draw)

        c.save()

        return FileResponse(output_path, media_type="application/pdf", filename="fema_certificate.pdf")

    except Exception as e:
        return {"error": str(e)}
