
from fpdf import FPDF
from io import BytesIO

def generate_pdf(tasks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Görev Listesi", ln=True, align="C")
    for task in tasks:
        pdf.cell(200, 10, txt=f"{task['tarih']} - {task['sehir']} - {task['gorev_adi']} - {task['atanan']} - {task['durum']}", ln=True)
    output = BytesIO()
    pdf.output(output)
    return output
