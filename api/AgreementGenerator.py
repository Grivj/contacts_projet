import os
from dataclasses import dataclass, field
from datetime import datetime

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


@dataclass
class AgreementGenerator:
    """Generate a good for agreement pdf file"""

    id: int
    name: str
    company: str
    siren: str
    pdf: canvas.Canvas = field(init=False)

    @property
    def title(self) -> str:
        return f"{self.company}-{self.siren}"

    @property
    def dir(self) -> str:
        return "/bpa"

    @property
    def filename(self) -> str:
        return f"{self.siren}.pdf"

    @property
    def is_already_exists(self) -> bool:
        return bool(os.path.isfile(f"/{self.dir}/{self.filename}"))

    def generate_pdf(self) -> None:
        pdf = canvas.Canvas(f"{self.dir}/{self.filename}")
        pdf.setTitle(self.title)
        self.pdf = pdf

    def draw_header(self) -> None:
        self.pdf.setFont("Helvetica-Bold", 20)
        self.pdf.drawCentredString(300, 700, "BON POUR ACCORD")

    def draw_paragraph(self) -> None:
        paragraph_base = f"""
        Je soussigné {self.name}, 
        Président de la société {self.company} ({self.siren})
        donne mon accord pour devenir client de la société Ayomi.
        """
        self.pdf.setFont("Helvetica", 14)
        styles = ParagraphStyle(name="Normal", fontName="Helvetica", fontSize=14)
        paragraph = Paragraph(paragraph_base, style=styles)
        paragraph.wrapOn(self.pdf, 400, 400)
        paragraph.drawOn(self.pdf, 100, 550)

    def draw_time(self) -> None:
        today = datetime.now()
        string_time = (
            f"Le {today.day}/{today.month}/{today.year} à {today.hour}h{today.minute}"
        )
        self.pdf.drawString(100, 420, "Fait à Paris,")
        self.pdf.drawString(100, 400, string_time)

    def draw_signatures(self) -> None:
        self.pdf.drawString(100, 300, "Signature Ayomi")
        self.pdf.drawString(400, 300, "Signature Client")

    def generate(self) -> canvas.Canvas:
        self.generate_pdf()
        self.draw_header()
        self.draw_paragraph()
        self.draw_time()
        self.draw_signatures()
        self.pdf.save()
        return self.pdf
