from datetime import datetime

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


def get_pdf(title: str) -> canvas.Canvas:
    pdf = canvas.Canvas(f"{title}.pdf")
    pdf.setTitle(title)
    return pdf


def draw_header(pdf: canvas.Canvas) -> None:
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(300, 700, "BON POUR ACCORD")


def draw_paragraph(
    pdf: canvas.Canvas, contact_name: str, company_name: str, siren_number: str
) -> None:
    paragraph_base = f"""
    Je soussigné {contact_name}, 
    Président de la société {company_name} ({siren_number})
    donne mon accord pour devenir client de la société Ayomi.
    """
    pdf.setFont("Helvetica", 14)
    styles = ParagraphStyle(name="Normal", fontName="Helvetica", fontSize=14)
    paragraph = Paragraph(paragraph_base, style=styles)
    paragraph.wrapOn(pdf, 400, 400)
    paragraph.drawOn(pdf, 100, 550)


def draw_time(pdf: canvas.Canvas) -> None:
    today = datetime.now()
    string_time = (
        f"Le {today.day}/{today.month}/{today.year} à {today.hour}h{today.minute}"
    )
    pdf.drawString(100, 420, "Fait à Paris,")
    pdf.drawString(100, 400, string_time)


def draw_signatures(pdf: canvas.Canvas) -> None:
    pdf.drawString(100, 300, "Signature Ayomi")
    pdf.drawString(400, 300, "Signature Client")


def generate_bpa(contact_name: str, company_name: str, siren_number: str):
    pdf = get_pdf(f"bpa_{siren_number}")
    draw_header(pdf)
    draw_paragraph(pdf, contact_name, company_name, siren_number)
    draw_time(pdf)
    draw_signatures(pdf)
    pdf.save()
