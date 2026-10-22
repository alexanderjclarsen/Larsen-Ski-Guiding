"""Lager PDF med turprogram og pakkeliste for Larsen Ski & Guiding."""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether)
from reportlab.lib.styles import ParagraphStyle

F = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Sans", F + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", F + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", F + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                              italic="Sans-Italic", boldItalic="Sans-Bold")

NAVY = colors.HexColor("#1F3A4D")
ACCENT = colors.HexColor("#5B8DB8")
LIGHT = colors.HexColor("#EEF3F7")
GREY = colors.HexColor("#5A6670")

S = {
    "title": ParagraphStyle("t", fontName="Sans-Bold", fontSize=22, leading=26, textColor=NAVY),
    "sub": ParagraphStyle("s", fontName="Sans", fontSize=11.5, leading=15, textColor=GREY),
    "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=13, leading=17, textColor=NAVY,
                         spaceBefore=10, spaceAfter=4),
    "day": ParagraphStyle("d", fontName="Sans-Bold", fontSize=11.5, leading=15, textColor=NAVY),
    "time": ParagraphStyle("tm", fontName="Sans-Bold", fontSize=9.5, leading=13, textColor=ACCENT),
    "body": ParagraphStyle("b", fontName="Sans", fontSize=10, leading=14, textColor=colors.black),
    "note": ParagraphStyle("n", fontName="Sans-Italic", fontSize=9.5, leading=13, textColor=GREY),
    "foot": ParagraphStyle("f", fontName="Sans", fontSize=8, leading=10, textColor=GREY),
}

def header_footer(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, h - 14 * mm, w, 14 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Sans-Bold", 10.5)
    c.drawString(18 * mm, h - 9 * mm, "LARSEN SKI & GUIDING")
    c.setFont("Sans", 8.5)
    c.drawRightString(w - 18 * mm, h - 9 * mm, "@larsenskiguiding")
    c.setFillColor(GREY)
    c.setFont("Sans", 7.5)
    c.drawString(18 * mm, 10 * mm, "Programmet kan endres på grunn av vær, føre eller skredfare.")
    c.drawRightString(w - 18 * mm, 10 * mm, f"Side {doc.page}")
    c.restoreState()

def day_block(dag, tid, tekst):
    inner = [Paragraph(dag, S["day"]), Paragraph(tid, S["time"]), Spacer(1, 3),
             Paragraph(tekst, S["body"])]
    t = Table([[inner]], colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return KeepTogether([t, Spacer(1, 6)])

def pakkeliste(grupper):
    rows = []
    for navn, ting in grupper:
        rows.append([Paragraph(f"<b>{navn}</b>", S["body"]),
                     Paragraph(" · ".join(ting), S["body"])])
    t = Table(rows, colWidths=[28 * mm, 146 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#D5DEE5")),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t

def bygg(ut):
    doc = SimpleDocTemplate(ut, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=24 * mm, bottomMargin=18 * mm,
                            title="Toppturhelg i Hemsedal – program",
                            author="Larsen Ski & Guiding")
    st = [
        Paragraph("Toppturhelg i Hemsedal", S["title"]),
        Spacer(1, 3),
        Paragraph("Guidede toppturer · 5.–7. februar 2027", S["sub"]),
        Spacer(1, 10),
        Paragraph("To dager med guidede toppturer, satt sammen for familien deres. Vi går opp i "
                  "fint fjellterreng og kjører ned der snøen er best. Turvalg og tempo tilpasses "
                  "dere, været og forholdene.", S["body"]),
        Paragraph("Program", S["h2"]),
        day_block("Fredag 5. februar – Ankomst", "Kveld",
                  "Dere ankommer Hemsedal. Jeg følger med på vær og skredvarsel i dagene før, "
                  "og fredag kveld sender jeg dere endelig plan med oppmøtested og tidspunkt."),
        day_block("Lørdag 6. februar – Hovedturen", "Oppmøte kl. 09:00 · nede igjen ca. kl. 16:00",
                  "Helgens store tur. Vi går mot en topp med god utsikt og en fin nedkjøring, "
                  "og jeg velger tur ut fra forholdene og dagsformen. Før vi starter, tar vi en "
                  "kort sikkerhetsgjennomgang og sjekker at alle sender/mottakere virker."),
        day_block("Søndag 7. februar – Andre turdag", "Oppmøte kl. 09:00 · nede igjen ca. kl. 15:00",
                  "En litt kortere tur der vi leter etter den beste snøen. Dere er ferdige i god "
                  "tid til hjemreisen."),
        Paragraph("Hvis forholdene tilsier det, endrer jeg planen og velger et tryggere alternativ. "
                  "Sikkerheten går alltid foran toppen.", S["note"]),
        Paragraph("Pakkeliste", S["h2"]),
        pakkeliste([
            ("Utstyr", ["Toppturski eller splitboard med feller", "toppturstøvler", "staver",
                        "sender/mottaker", "spade", "søkestang", "sekk 25–35 liter",
                        "hjelm (anbefalt)", "skibriller og solbriller"]),
            ("Klær", ["Ullundertøy", "fleece eller annet mellomlag",
                      "isolerende jakke (dun eller syntetisk)", "skalljakke og skallbukse",
                      "lue og buff", "to par hansker, gjerne votter i tillegg"]),
            ("Mat og drikke", ["Niste og snacks for en lang dag", "termos med varm drikke", "vann"]),
            ("Annet", ["Solkrem og leppepomade", "eventuelt plaster og egne medisiner"]),
        ]),
        Spacer(1, 6),
        Paragraph("Mangler dere noe utstyr, særlig sender/mottaker, spade eller søkestang? "
                  "Gi meg beskjed, så finner vi en løsning.", S["note"]),
        Paragraph("Kontakt", S["h2"]),
        Paragraph("<b>Alexander Larsen</b> · Larsen Ski & Guiding · Instagram: @larsenskiguiding",
                  S["body"]),
    ]
    doc.build(st, onFirstPage=header_footer, onLaterPages=header_footer)

if __name__ == "__main__":
    bygg(sys.argv[1])
