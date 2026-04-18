"""
make_prospectus.py
------------------
Builds the final one-page prospectus PDF.
Output: ../docs/prospectus.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "docs", "prospectus.pdf"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)

styles = getSampleStyleSheet()
ACCENT = colors.HexColor("#3b2e7e")
INK = colors.HexColor("#1b1f24")
MUTED = colors.HexColor("#5d6570")
RULE = colors.HexColor("#e6e8ec")
SOFT = colors.HexColor("#f1efff")

def mk(name, parent, **kw):
    return ParagraphStyle(name, parent=parent, **kw)

TITLE = mk("T", styles["Title"], fontName="Helvetica-Bold", textColor=INK,
           fontSize=18, leading=22, alignment=TA_LEFT, spaceAfter=4)
HINT = mk("Hint", styles["Normal"], fontName="Helvetica-Bold", fontSize=8.4,
          textColor=MUTED, leading=11, spaceAfter=2)
BODY = mk("B", styles["Normal"], fontName="Helvetica", fontSize=9.6,
          textColor=INK, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=5)
LABEL = mk("Lbl", styles["Normal"], fontName="Helvetica-Bold", fontSize=8.6,
           textColor=ACCENT, leading=11.5, spaceAfter=2)
SMALL = mk("S", BODY, fontSize=8.6, leading=11.8, spaceAfter=3)
META = mk("M", styles["Normal"], fontName="Helvetica", fontSize=8.2,
          textColor=MUTED, leading=11)

PAGE_W, PAGE_H = LETTER

def build():
    doc = BaseDocTemplate(OUT, pagesize=LETTER,
                          leftMargin=0.6*inch, rightMargin=0.6*inch,
                          topMargin=0.55*inch, bottomMargin=0.55*inch,
                          title="Prospectus - Taken by Surprise",
                          author="McAlarney, Hu, Farquharson, Vaddeboina")
    frame = Frame(0.6*inch, 0.55*inch, PAGE_W - 1.2*inch, PAGE_H - 1.1*inch,
                  id="only", showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame])])

    s = []
    s.append(Paragraph("CS 573 &middot; DATA VISUALIZATION &middot; FINAL PROJECT PROSPECTUS", HINT))
    s.append(Paragraph("Taken by Surprise: Mapping U.S. Cargo Theft in 2024", TITLE))
    s.append(Paragraph(
        "Matthew McAlarney &middot; Hongchao Hu &middot; Duncan Farquharson &middot; "
        "Sai Krishna Vaddeboina  <font color='#5d6570'>&nbsp;&bull;&nbsp; "
        "Prof. Lane T. Harrison &middot; Worcester Polytechnic Institute &middot; "
        "Spring 2026</font>", META))
    s.append(Spacer(1, 8))

    # ---- Abstract ----
    s.append(Paragraph("Abstract", LABEL))
    s.append(Paragraph(
        "Cargo theft costs U.S. shippers, insurers, and consumers approximately half "
        "a billion dollars annually, but the FBI's own public visualization &mdash; a "
        "raw-dollar choropleth &mdash; is dominated by a single outlier state and a "
        "repeated population pattern. We will build an interactive Bayesian Surprise "
        "Map web application over the 2024 FBI Cargo Theft release that exposes "
        "which states' per-capita cargo theft rates deviate most from the population-"
        "adjusted national baseline, using the de Moivre funnel formulation of "
        "Correll &amp; Heer (2017) and the design considerations of Ndlovu, Shrestha "
        "&amp; Harrison (2023). The deliverable is a single-page D3 + Bulma app, a "
        "reproducible Python data pipeline, a reference Process Book, and a 4-minute "
        "screencast.", BODY))

    # ---- Research questions ----
    s.append(Paragraph("Research Questions", LABEL))
    s.append(Paragraph(
        "(1) Which U.S. states exhibit cargo-theft rates that deviate most from the "
        "population-adjusted national baseline, and in which direction? "
        "(2) Does the conventional raw-dollar choropleth produce a materially "
        "different impression of regional risk than a Surprise encoding? "
        "(3) For regions where stolen value and incident rate disagree, does "
        "exposing both axes help the viewer avoid a one-metric conclusion?", BODY))

    # ---- Data + method ----
    two_col = Table([[
        [
            Paragraph("Data &amp; Sources", LABEL),
            Paragraph(
                "<b>FBI Crime Data Explorer</b> - Cargo Theft Tables 1-5, 2024 release "
                "(state, offense, location, victim granularity). <b>U.S. Census "
                "Bureau</b> - Vintage 2024 Annual Population Estimates for Incorporated "
                "Places (SUB-IP-EST2024-POP). Both are public-domain government files; "
                "we version them in-repo. Coverage: 47 reporting states, 2,300 "
                "agencies, 16,183 incidents, $483.4 M stolen.", SMALL)
        ],
        [
            Paragraph("Methodology", LABEL),
            Paragraph(
                "For each state i we compute rate r<sub>i</sub>=k<sub>i</sub>/n<sub>i</sub>, "
                "the national rate p<super>&#x005E;</super>=&Sigma;k/&Sigma;n, standard error "
                "SE<sub>i</sub>=&radic;(p<super>&#x005E;</super>(1-p<super>&#x005E;</super>)/n<sub>i</sub>), z-score "
                "Z<sub>i</sub>=(r<sub>i</sub>-p<super>&#x005E;</super>)/SE<sub>i</sub>, and a bounded "
                "visual statistic s<sub>i</sub>=sign(Z<sub>i</sub>)&middot;&radic;|Z<sub>i</sub>|. "
                "Value-per-capita surprise is built analogously as a cross-state "
                "Gaussian z-score. All computation lives in "
                "<font face='Courier'>src/build_data.py</font>.", SMALL)
        ]
    ]], colWidths=[3.55*inch, 3.55*inch])
    two_col.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0,0), (-1,-1), SOFT),
        ("BOX", (0,0), (-1,-1), 0.4, RULE),
        ("INNERGRID", (0,0), (-1,-1), 0.4, RULE),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    s.append(two_col)
    s.append(Spacer(1, 6))

    # ---- Design ----
    s.append(Paragraph("Visualization Design", LABEL))
    s.append(Paragraph(
        "Single-page app with a 960&times;560 geoAlbersUsa choropleth, seven "
        "view-toggle tabs (raw value, value per capita, incidents per 100k, "
        "surprise on rate, surprise on value, population, percent recovered), a "
        "hover tooltip that exposes rate + value + population + z + surprise "
        "simultaneously, a hover-to-filter interactive legend, and a synchronized "
        "Top-5 / Bottom-5 ranked list. Diverging surprise views use an RdBu palette "
        "over a symmetric domain; sequential views use nine-bin "
        "<font face='Courier'>scaleQuantize</font> per Ndlovu et al. design "
        "consideration #4.", BODY))

    # ---- Tools + timeline ----
    tt = Table([[
        [
            Paragraph("Tools &amp; Libraries", LABEL),
            Paragraph(
                "D3 v7, topojson-client v3, Bulma CSS v1, us-atlas v3, Python 3 "
                "(openpyxl, reportlab, matplotlib). No build step, deploys to "
                "GitHub Pages as-is.", SMALL),
        ],
        [
            Paragraph("Timeline", LABEL),
            Paragraph(
                "<b>Mar 25</b> proposal submitted. "
                "<b>Apr 7</b> Prof. Harrison feedback, scope narrowed to cargo theft. "
                "<b>Apr 10</b> implementation plan signed off, GitHub repo shared. "
                "<b>Apr 13</b> 2024 Cargo Theft dataset selected. "
                "<b>Apr 14</b> Datawrapper prototype shared. "
                "<b>Apr 18</b> data pipeline + Process Book draft complete. "
                "Target class delivery mid-May 2026.", SMALL),
        ]
    ]], colWidths=[3.55*inch, 3.55*inch])
    tt.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0,0), (-1,-1), colors.white),
        ("BOX", (0,0), (-1,-1), 0.4, RULE),
        ("INNERGRID", (0,0), (-1,-1), 0.4, RULE),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    s.append(tt)
    s.append(Spacer(1, 6))

    # ---- Deliverables ----
    s.append(Paragraph("Deliverables", LABEL))
    s.append(Paragraph(
        "(a) Live GitHub Pages site &mdash; <font face='Courier'>index.html</font>; "
        "(b) reproducible pipeline &mdash; <font face='Courier'>src/build_data.py</font> "
        "and <font face='Courier'>data/cargo_theft_surprise_2024.csv</font>; "
        "(c) Process Book PDF &mdash; <font face='Courier'>docs/process_book.pdf</font> "
        "(11 pages, 5 figures, 8 references); "
        "(d) 4-minute screencast walkthrough; "
        "(e) this prospectus.", BODY))

    # ---- Anticipated challenges ----
    s.append(Paragraph("Anticipated Challenges", LABEL))
    s.append(Paragraph(
        "(i) The de Moivre funnel saturates p-values for rare events (cargo theft is "
        "~7.7 per 100k); we handle this with the signed &radic;|Z| visual statistic "
        "and flag it as a limitation. "
        "(ii) Reporting coverage is uneven &mdash; several states have near-zero "
        "participation; we do not silently impute. "
        "(iii) The Census place-level population file omits unincorporated residents; "
        "aggregated totals undershoot rural-state populations by 15-25%. All three "
        "limitations are documented in the Process Book.", BODY))

    # ---- Footer ----
    s.append(Spacer(1, 6))
    s.append(Paragraph(
        "Repository: <font color='#3b2e7e'>github.com/MacCode7110/grad-final</font> "
        "&middot; Advisor: Akim Ndlovu (WPI Vis Group) "
        "&middot; Prospectus v2 &middot; 17 April 2026", META))

    doc.build(s)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
