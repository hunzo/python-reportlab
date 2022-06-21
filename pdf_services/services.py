from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Flowable, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import pdfencrypt
from reportlab.lib.validators import Auto
from reportlab.lib.units import inch

import io
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pdfmetrics.registerFont(
    TTFont('THSarabun', f'{BASE_DIR}/fonts/THSarabunNew.ttf'))
pdfmetrics.registerFont(
    TTFont('Prompt', f'{BASE_DIR}/fonts/Prompt-Regular.ttf'))

PromptStyle = ParagraphStyle('Prompt', fontName="Prompt", fontSize=12)
THSarabunStyle = ParagraphStyle('THSarabun', fontName="THSarabun", fontSize=18)


class CreateLine(Flowable):
    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def __repr__(self):
        return "Line(w=%s)" % self.width

    def draw(self):
        """
        draw the line
        """
        self.canv.line(0, self.height, self.width, self.height)


def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


def pie_chart_with_legend():
    data = list(range(15, 105, 15))
    drawing = Drawing(width=400, height=200)
    my_title = String(170, 40, 'My Pie Chart', fontSize=14)
    pie = Pie()
    pie.sideLabels = True
    pie.x = 150
    pie.y = 65
    pie.data = data
    pie.labels = [letter for letter in 'abcdefg']
    pie.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(pie)
    add_legend(drawing, pie, data)
    return drawing


def create_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        encrypt=pdfencrypt.StandardEncryption(
            "test",
            canPrint=0
        )
    )

    # line = CreateLine(500)
    # spacer = Spacer(0, 0.25*inch)

    element = []
    # styles = getSampleStyleSheet()

    # ptext = Paragraph("Text Normal style", styles["Normal"])
    # element.append(ptext)
    # element.append(spacer)

    # ptext = Paragraph("Text Prompt style", PromptStyle)
    # element.append(ptext)
    # element.append(spacer)

    # ptext = Paragraph("Text THSarabun style", THSarabunStyle)
    # element.append(ptext)
    # element.append(spacer)

    # element.append(line)

    # chart = pie_chart_with_legend()
    # element.append(chart)

    element.append(CreateLine(410))
    element.append(Spacer(0, 0.05*inch))
    ptext = Paragraph(
        "Account Information: ", PromptStyle)
    element.append(ptext)
    element.append(Spacer(0, 0.1*inch))
    element.append(CreateLine(410))

    data = {
        "username": "username",
        "password": "password",
        "time stamp": datetime.now().strftime("%Y%m%d-%H:%M:%S")
    }

    for k, v in data.items():
        ptext = Paragraph(f"{k}: {v}", THSarabunStyle)
        element.append(ptext)
        element.append(Spacer(0, 0.1*inch))

    doc.build(element)
    buffer.seek(0)

    return buffer
