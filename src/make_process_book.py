"""
make_process_book.py
--------------------
Builds the Process Book PDF deliverable for the CS 573 Final Project
"Taken by Surprise: Mapping U.S. Cargo Theft in 2024."

Output: ../docs/process_book.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, Image, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "docs", "process_book.pdf"))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "assets"))

os.makedirs(os.path.dirname(OUT), exist_ok=True)

# ----------------------------------------------------------------- #
# Styles                                                            #
# ----------------------------------------------------------------- #
styles = getSampleStyleSheet()

ACCENT = colors.HexColor("#3b2e7e")
INK = colors.HexColor("#1b1f24")
MUTED = colors.HexColor("#5d6570")
RULE = colors.HexColor("#e6e8ec")
SOFT = colors.HexColor("#f1efff")

def make_style(name, parent, **kw):
    s = ParagraphStyle(name, parent=parent, **kw)
    return s

TITLE = make_style("Title", styles["Title"], fontName="Helvetica-Bold",
                   textColor=INK, fontSize=26, leading=30, alignment=TA_LEFT,
                   spaceAfter=6)
SUBTITLE = make_style("Subtitle", styles["Normal"], fontName="Helvetica",
                      textColor=MUTED, fontSize=13, leading=17, spaceAfter=20)
H1 = make_style("H1", styles["Heading1"], fontName="Helvetica-Bold",
                textColor=ACCENT, fontSize=17, leading=22, spaceBefore=18,
                spaceAfter=8)
H2 = make_style("H2", styles["Heading2"], fontName="Helvetica-Bold",
                textColor=INK, fontSize=12.5, leading=17, spaceBefore=12,
                spaceAfter=4)
BODY = make_style("Body", styles["Normal"], fontName="Helvetica",
                  textColor=INK, fontSize=10.2, leading=14.6,
                  alignment=TA_JUSTIFY, spaceAfter=8)
QUOTE = make_style("Quote", BODY, leftIndent=18, rightIndent=18,
                   fontName="Helvetica-Oblique", textColor=MUTED)
CAPTION = make_style("Caption", styles["Normal"], fontName="Helvetica-Oblique",
                     textColor=MUTED, fontSize=8.8, leading=11.5,
                     alignment=TA_LEFT, spaceAfter=14, spaceBefore=3)
SMALL = make_style("Small", BODY, fontSize=9.2, leading=12.8)
BULLET = make_style("Bullet", BODY, leftIndent=18, bulletIndent=6,
                    spaceAfter=3)
REF = make_style("Ref", BODY, fontSize=9, leading=12.6, leftIndent=14,
                 firstLineIndent=-14, spaceAfter=4)
META = make_style("Meta", styles["Normal"], fontName="Helvetica",
                  textColor=MUTED, fontSize=9, leading=12)
COVERLINE = make_style("CoverLine", styles["Normal"], fontName="Helvetica-Bold",
                       fontSize=10, textColor=MUTED, leading=14,
                       alignment=TA_LEFT)
KPI_NUM = make_style("KPINum", styles["Normal"], fontName="Helvetica-Bold",
                     textColor=ACCENT, fontSize=14, leading=18,
                     alignment=TA_CENTER)
KPI_LBL = make_style("KPILbl", styles["Normal"], fontName="Helvetica",
                     textColor=MUTED, fontSize=7.8, leading=10,
                     alignment=TA_CENTER)

# ----------------------------------------------------------------- #
# Page frame                                                        #
# ----------------------------------------------------------------- #
PAGE_W, PAGE_H = LETTER
MARGIN = 0.8 * inch

def on_page(canvas, doc):
    canvas.saveState()
    # Header rule on pages 2+
    if doc.page > 1:
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)
        canvas.line(MARGIN, PAGE_H - 0.5 * inch, PAGE_W - MARGIN, PAGE_H - 0.5 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN, PAGE_H - 0.4 * inch,
                          "Taken by Surprise  -  Process Book")
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.4 * inch,
                               "CS 573  -  Worcester Polytechnic Institute  -  Spring 2026")
    # Footer page number.
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(PAGE_W / 2, 0.45 * inch, f"{doc.page}")
    canvas.restoreState()


# ----------------------------------------------------------------- #
# Content helpers                                                   #
# ----------------------------------------------------------------- #
def section(title, story):
    story.append(Paragraph(title, H1))

def sub(title, story):
    story.append(Paragraph(title, H2))

def p(text, story, style=BODY):
    story.append(Paragraph(text, style))

def bullets(items, story):
    for it in items:
        story.append(Paragraph("&bull;&nbsp;&nbsp;" + it, BULLET))

def figure(path, caption, story, width=6.5 * inch):
    if os.path.exists(path):
        img = Image(path, width=width, height=width * 0.62)
        img.hAlign = "CENTER"
        story.append(Spacer(1, 4))
        story.append(img)
        story.append(Paragraph(caption, CAPTION))

def rule(story):
    story.append(Spacer(1, 6))
    story.append(Table([[""]], colWidths=[6.8*inch], rowHeights=[0.6],
                       style=TableStyle([("LINEABOVE", (0,0), (-1,0), 0.4, RULE)])))
    story.append(Spacer(1, 8))


# ----------------------------------------------------------------- #
# Build document                                                    #
# ----------------------------------------------------------------- #
def build():
    doc = BaseDocTemplate(OUT, pagesize=LETTER,
                          leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=0.9 * inch, bottomMargin=0.7 * inch,
                          title="Taken by Surprise: Mapping U.S. Cargo Theft in 2024",
                          author="McAlarney, Hu, Farquharson, Vaddeboina",
                          subject="CS 573 Final Project - Surprise Map Web Application")
    frame = Frame(MARGIN, 0.7 * inch, PAGE_W - 2 * MARGIN,
                  PAGE_H - 1.6 * inch, id="normal", showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="body", frames=[frame], onPage=on_page)])

    story = []

    # ---------- Cover ----------
    story.append(Spacer(1, 1.1 * inch))
    story.append(Paragraph("CS 573 &middot; DATA VISUALIZATION &middot; SPRING 2026", COVERLINE))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Taken by Surprise", TITLE))
    story.append(Paragraph("Mapping U.S. Cargo Theft in 2024 with Bayesian Surprise Maps",
                           SUBTITLE))
    story.append(Spacer(1, 0.3 * inch))

    cover_table = Table(
        [
            [Paragraph("<b>Project</b>", META), Paragraph("Final Project &mdash; Surprise Map Web Application", BODY)],
            [Paragraph("<b>Team</b>", META),
             Paragraph("Matthew McAlarney &middot; Hongchao Hu &middot; Duncan Farquharson &middot; Sai Krishna Vaddeboina", BODY)],
            [Paragraph("<b>Instructor</b>", META), Paragraph("Prof. Lane T. Harrison", BODY)],
            [Paragraph("<b>Advisor</b>", META), Paragraph("Akim Ndlovu", BODY)],
            [Paragraph("<b>Institution</b>", META), Paragraph("Worcester Polytechnic Institute", BODY)],
            [Paragraph("<b>Repository</b>", META), Paragraph("github.com/MacCode7110/grad-final", BODY)],
        ],
        colWidths=[1.2 * inch, 5.3 * inch]
    )
    cover_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE),
    ]))
    story.append(cover_table)

    story.append(Spacer(1, 0.45 * inch))
    p("This Process Book documents the full research, design, and engineering arc of an "
      "interactive Surprise Map web application built on the FBI Crime Data Explorer 2024 "
      "Cargo Theft release and U.S. Census Bureau 2024 incorporated-place population "
      "estimates. It is the Step-5 written deliverable of the team's five-step "
      "implementation plan, and accompanies the live web application, the prospectus, "
      "and the screencast walkthrough.", story)

    story.append(Spacer(1, 0.4 * inch))
    kpis = Table([
        [Paragraph("<b>47</b>", KPI_NUM), Paragraph("<b>16,183</b>", KPI_NUM),
         Paragraph("<b>$483.4M</b>", KPI_NUM), Paragraph("<b>9.7%</b>", KPI_NUM),
         Paragraph("<b>2,300</b>", KPI_NUM)],
        [Paragraph("States reporting", KPI_LBL), Paragraph("Incidents (2024)", KPI_LBL),
         Paragraph("Total stolen value", KPI_LBL), Paragraph("Recovery rate", KPI_LBL),
         Paragraph("Reporting agencies", KPI_LBL)],
    ], colWidths=[1.3*inch]*5)
    kpis.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOX", (0,0), (-1,-1), 0.3, RULE),
        ("INNERGRID", (0,0), (-1,-1), 0.3, RULE),
        ("BACKGROUND", (0,0), (-1,-1), colors.white),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(kpis)

    story.append(PageBreak())

    # ---------- 1. Overview & Motivation ----------
    section("1.&nbsp;&nbsp;Overview and Motivation", story)
    p("Cargo theft is an under-reported, under-measured crime with disproportionate downstream "
      "impact on supply-chain pricing, insurance markets, and household goods availability. "
      "The FBI Crime Data Explorer (CDE) began publishing a dedicated cargo-theft release in "
      "2013 to close this gap. The 2024 release, used in this project, aggregates reports "
      "from 2,300 law-enforcement agencies covering 47 reporting states and logs 16,183 "
      "incidents and $483.4 million in stolen property, of which only 9.7&thinsp;% was recovered.",
      story)
    p("Presenting such a dataset fairly is non-trivial. A naive choropleth of the raw stolen "
      "dollar amount is dominated by one state &mdash; Kentucky, which reports $150.2 million "
      "across only 70 incidents &mdash; and by population-scaled patterns that repeat the "
      "population map rather than tell a story about crime. Our project takes this as a design "
      "challenge: build a visualization that communicates <i>where cargo theft deviates most "
      "from what a reasonable baseline would predict</i>, given population. We pursue this "
      "using the <b>Bayesian Surprise</b> encoding originally proposed by Correll and Heer "
      "(2017) and empirically validated by our advisor Akim Ndlovu and colleagues in "
      "<i>Taken by Surprise?</i> (Ndlovu, Shrestha, &amp; Harrison, 2023).", story)

    sub("1.1&nbsp;&nbsp;Why this project for a Fintech cohort", story)
    p("Cargo theft is a direct input to property-and-casualty insurance loss modelling, "
      "retail shrinkage forecasts, and commercial credit decisioning for logistics firms. A "
      "surprise-weighted view of regional risk is structurally similar to the statistical "
      "control charts used in financial-fraud monitoring, and exposing the technique in an "
      "accessible web app is itself a risk-communication exercise. The project therefore "
      "sits squarely at the intersection of data visualization, Bayesian inference, and "
      "applied financial risk &mdash; the focus of WPI's M.S. Fintech curriculum.", story)

    # ---------- 2. Related Work ----------
    section("2.&nbsp;&nbsp;Related Work", story)
    p("Two bodies of work inform the project. First, <b>debiasing thematic maps</b>: "
      "MacEachren (1992) and Brunsdon et&nbsp;al. (1998) catalogued the classical choropleth "
      "failure modes &mdash; area bias, population confounding, and classification "
      "sensitivity. Correll and Heer (2017) introduced <i>Surprise Maps</i>, using Bayesian "
      "updating from a de Moivre funnel prior to down-weight rates that are statistically "
      "consistent with the national mean given their population. Correll, Moritz, and Heer "
      "(2018) extended this idea with Value-Suppressing Uncertainty Palettes (VSUPs).", story)
    p("Second, <b>empirical evaluation</b>: Ndlovu, Shrestha, and Harrison (2023, arXiv "
      "2307.15138) ran a crowdsourced n&nbsp;=&nbsp;300 experiment comparing Choropleth, Surprise, "
      "and VSUP map conditions on COVID-19 vaccination and poverty datasets. Their results "
      "motivate the specific implementation choices we adopt: a geoAlbersUsa projection, "
      "quantile-binned color scales, tooltips exposing rate &amp; surprise &amp; population "
      "simultaneously, and a 950&thinsp;&times;&thinsp;525 map canvas. The authors caution "
      "that participants frequently consider only a subset of the metrics on screen, which "
      "shapes our decision to expose ranked top/bottom lists alongside the map.", story)

    figure(os.path.join(ASSETS, "fig1_funnel.png"),
           "Figure 1. de Moivre funnel plot of the 47 reporting states. The shaded bands "
           "show the 95% and 3-sigma sampling-variation envelopes around the national "
           "incident rate (dashed line). States that fall well outside the envelope are "
           "the ones a Bayesian Surprise encoding will highlight.", story)

    # ---------- 3. Research Questions ----------
    section("3.&nbsp;&nbsp;Research Questions", story)
    p("We frame three driving questions. Each is scoped so that the answer is constructible "
      "from the 2024 dataset alone and falsifiable on its face.", story)
    bullets([
        "<b>RQ1.</b> Which U.S. states exhibit cargo-theft rates that deviate most from the "
        "population-adjusted national baseline, and in which direction?",
        "<b>RQ2.</b> Does the conventional raw-dollar choropleth &mdash; which currently "
        "dominates public CDE visualisations &mdash; produce a materially different "
        "impression of the regional risk map than a Surprise encoding?",
        "<b>RQ3.</b> For regions where stolen value and incident rate disagree (e.g., few "
        "high-value incidents versus many low-value ones), does exposing both axes help "
        "the viewer avoid an incorrect conclusion?",
    ], story)

    # ---------- 4. Data ----------
    section("4.&nbsp;&nbsp;Data: Sources, Cleanup, Transformation", story)
    sub("4.1&nbsp;&nbsp;Sources", story)
    p("The project uses two public, government-published datasets. Both are pulled from "
      "their canonical distribution endpoints and versioned in the repository under "
      "<font face='Courier'>/data</font>.", story)
    data_sources = Table([
        ["Source", "Publisher", "File", "Granularity"],
        ["2024 Cargo Theft tables", "FBI CDE (Uniform Crime Reporting)",
         "Cargo_Theft_Table_1_&hellip;_2024.xlsx", "State, offense, location, victim"],
        ["2024 Place-level population", "U.S. Census Bureau, Vintage 2024",
         "SUB-IP-EST2024-POP.xlsx", "Incorporated places, U.S."],
        ["Surprise methodology", "arXiv preprint, 2023",
         "2307.15138v1.pdf", "n/a (reference)"],
    ], colWidths=[1.4*inch, 1.8*inch, 2.1*inch, 1.5*inch])
    data_sources.setStyle(TableStyle([
        ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
        ("FONT", (0,1), (-1,-1), "Helvetica", 9),
        ("TEXTCOLOR", (0,0), (-1,0), ACCENT),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, SOFT]),
        ("GRID", (0,0), (-1,-1), 0.25, RULE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(data_sources)
    story.append(Spacer(1, 10))

    sub("4.2&nbsp;&nbsp;Cleanup and transformation", story)
    p("The FBI table headers are multi-line and include trailing footnotes and pagination "
      "artifacts; Hongchao produced the state-level cleaned version "
      "<font face='Courier'>cargo_theft_by_state_2024_data_modified.xlsx</font> which is the "
      "direct input to our pipeline. The Census file is place-level, covering 19,489 "
      "incorporated places. Because FBI Table&nbsp;1 is state-level, we roll the Census "
      "file up to the state level by regex-parsing <i>&ldquo;Place, State&rdquo;</i> labels.", story)
    p("The full pipeline lives in <font face='Courier'>src/build_data.py</font> and is "
      "reproducible with a single command. It outputs two CSVs: a state-level population "
      "reference (<font face='Courier'>state_populations_2024.csv</font>) and the joined, "
      "Bayesian-weighted analysis set (<font face='Courier'>cargo_theft_surprise_2024.csv</font>).",
      story)

    sub("4.3&nbsp;&nbsp;Bayesian Surprise formulation", story)
    p("For a state <i>i</i> with observed incident count <i>k<sub>i</sub></i> and "
      "population <i>n<sub>i</sub></i>, we define the per-capita rate "
      "<i>r<sub>i</sub></i>&nbsp;=&nbsp;<i>k<sub>i</sub></i>&nbsp;/&nbsp;<i>n<sub>i</sub></i> "
      "and the national rate p<super>&#x005E;</super>&nbsp;=&nbsp;<font face='Courier'>&Sigma; k / &Sigma; n</font>. "
      "Under the de Moivre funnel model of Correll &amp; Heer (2017), the sampling-variation "
      "standard error at population <i>n<sub>i</sub></i> is "
      "<i>SE<sub>i</sub></i>&nbsp;=&nbsp;<font face='Courier'>&radic;( p<super>&#x005E;</super>(1-p<super>&#x005E;</super>)/n<sub>i</sub> )</font>, "
      "and the z-score of the deviation is "
      "<i>Z<sub>i</sub></i>&nbsp;=&nbsp;(<i>r<sub>i</sub></i>&nbsp;&minus;&nbsp;p<super>&#x005E;</super>)&nbsp;/&nbsp;<i>SE<sub>i</sub></i>.",
      story)
    p("The Bayesian surprise is the two-sided p-value under the standard-normal "
      "approximation of the sampling distribution: "
      "<i>surprise<sub>i</sub></i>&nbsp;=&nbsp;2(1 &minus; &Phi;(|<i>Z<sub>i</sub></i>|)). "
      "Because cargo-theft incidents are rare (p<super>&#x005E;</super>&nbsp;&approx;&nbsp;7.7 per 100k), "
      "classical p-values saturate at zero for most states (|Z|&nbsp;&gt;&nbsp;20 is common). "
      "For visual encoding we therefore use the bounded non-saturating statistic "
      "<i>s<sub>i</sub></i>&nbsp;=&nbsp;sign(<i>Z<sub>i</sub></i>) &middot; "
      "&radic;|<i>Z<sub>i</sub></i>|, which preserves direction and relative magnitude of "
      "the deviation while rendering on a divergent color scale without clipping.", story)

    figure(os.path.join(ASSETS, "fig4_rate_distribution.png"),
           "Figure 2. Distribution of state-level incident rates. The mode sits well below "
           "the national rate of 7.7 / 100k; a long right tail of states with rates 20x to "
           "80x higher drives the surprise signal.", story, width=5.8*inch)

    # ---------- 5. Exploratory Analysis ----------
    section("5.&nbsp;&nbsp;Exploratory Data Analysis", story)
    p("Before committing to any visual encoding, the team explored the joined data with "
      "three lenses: ranked value tables, the funnel plot, and a cross-axis scatter of "
      "rate-surprise against value-surprise. The funnel (Figure&nbsp;1) made the "
      "methodological issue immediately visible: the standard error shrinks so fast with "
      "<i>n</i> that nearly every state is several SE away from p<super>&#x005E;</super>. The "
      "distribution of raw rates (Figure&nbsp;2) explained why: it is right-skewed with a "
      "heavy tail.", story)

    figure(os.path.join(ASSETS, "fig5_top_value_states.png"),
           "Figure 3. Top 12 states by raw 2024 cargo theft stolen value. Kentucky (KY) "
           "dwarfs every other state with $150.2M across 70 incidents, producing a "
           "single-state anomaly that the conventional choropleth fails to contextualize.",
           story, width=6.3*inch)

    p("The Kentucky anomaly is both scientifically real and narratively dangerous: a raw-"
      "dollar choropleth hands the viewer one tinted state and 46 near-white states. The "
      "cross-axis scatter (Figure&nbsp;4) tells a more useful story: Maryland and Georgia "
      "are distinctive on <i>rate</i> (many incidents per person), while Kentucky is "
      "distinctive on <i>value</i> (single jumbo-value event); no state is distinctive on "
      "both at once. This is exactly the kind of multi-axis differentiation the Surprise "
      "encoding is designed to surface.", story)

    figure(os.path.join(ASSETS, "fig3_value_vs_rate.png"),
           "Figure 4. Rate-surprise (x) against value-surprise (y) per state. States in the "
           "upper-left or right quadrants would be distinctive on both axes; our data shows "
           "that rate and value anomalies are largely orthogonal, so a single-metric "
           "encoding hides half the story.",
           story, width=6.0*inch)

    # ---------- 6. Design Evolution ----------
    section("6.&nbsp;&nbsp;Design Evolution", story)
    sub("6.1&nbsp;&nbsp;Iteration 1: FBI Crime Data Heatmap (rejected)", story)
    p("Our original prospectus proposed a nationwide town-and-city heatmap of all FBI "
      "Crime Data Explorer indices with a user-supplied weighting interface. After "
      "consulting Prof. Harrison on 2026-04-07 we narrowed scope for two reasons: (1) the "
      "CDE API rate-limits detail queries and the town-level crime payload exceeds 2GB "
      "uncompressed; (2) scientifically-defensible per-town safety calculation would "
      "require data we were not positioned to audit in six weeks. The team agreed to "
      "trade breadth for depth.", story)

    sub("6.2&nbsp;&nbsp;Iteration 2: Cargo Theft Choropleth (baseline)", story)
    p("Matthew selected the 2024 Cargo Theft release (2026-04-13) because its state-level "
      "table is well-formed, the domain is financially relevant, and 2020/2022/2023 "
      "releases provide a clean future-work path to year-over-year comparison. Hongchao "
      "produced the first prototype in Datawrapper the following day: a Choropleth of "
      "stolen value per state. We treat this as the experimental control: it is the view "
      "most users would see on the CDE website today, and it is the view our Surprise Map "
      "must outperform.", story)

    sub("6.3&nbsp;&nbsp;Iteration 3: Bayesian Surprise Map (current)", story)
    p("The final design exposes seven synchronized views on a common geoAlbersUsa "
      "projection: total stolen value (the Datawrapper baseline), stolen value per capita, "
      "incidents per 100k, Bayesian surprise on rate, Bayesian surprise on value-per-"
      "capita, 2024 population, and percent recovered. Each view is a single click away; "
      "the right-rail ranked list updates in place; a unified tooltip shows rate, value, "
      "population, z-score, and surprise simultaneously so the viewer is never stuck with "
      "only the one metric the map happens to encode at that moment &mdash; addressing "
      "the &lsquo;only-one-metric&rsquo; finding from Ndlovu et&nbsp;al.", story)

    figure(os.path.join(ASSETS, "fig2_surprise_ranked.png"),
           "Figure 5. States ranked by signed surprise on per-capita incident rate. Red "
           "bars denote surprisingly-high rates; blue bars denote surprisingly-low. The "
           "ranking is the content of the right-rail Top-5 / Bottom-5 panels in the live "
           "web application.", story, width=5.2*inch)

    # ---------- 7. Implementation ----------
    section("7.&nbsp;&nbsp;Implementation", story)
    p("The deliverable is a single-page static web application. The stack is deliberately "
      "minimal: D3 v7 for rendering, Bulma CSS for typography and layout, topojson-client "
      "for atlas parsing, and a static CSV for the data layer. There is no build step, no "
      "bundler, and no server &mdash; the application deploys to GitHub Pages as-is.", story)
    sub("7.1&nbsp;&nbsp;Data layer", story)
    p("<font face='Courier'>src/build_data.py</font> is a pure-stdlib Python script "
      "(<font face='Courier'>openpyxl</font> for xlsx only). It produces "
      "<font face='Courier'>data/cargo_theft_surprise_2024.csv</font>, 47 rows with 21 "
      "columns including all three surprise statistics, z-scores, and directional labels. "
      "The CSV is the single source of truth for the application &mdash; no client-side "
      "computation of the surprise statistic.", story)
    sub("7.2&nbsp;&nbsp;Rendering layer", story)
    p("US state polygons are loaded once from the <font face='Courier'>us-atlas@3</font> "
      "topojson distribution, matched to rows by two-digit state FIPS, and drawn with "
      "<font face='Courier'>d3.geoPath</font> at a fixed 960&thinsp;&times;&thinsp;560 "
      "viewBox that scales responsively. Color scales are rebuilt per view: "
      "<font face='Courier'>d3.scaleQuantize</font> with nine bins for sequential metrics "
      "(following the Ndlovu et&nbsp;al. design consideration #4), and "
      "<font face='Courier'>d3.scaleDiverging</font> over a symmetric domain for the two "
      "surprise views.", story)
    sub("7.3&nbsp;&nbsp;Interaction layer", story)
    bullets([
        "<b>Hover tooltip</b>: positioned to the cursor with a fixed translate so it does not "
        "occlude the hovered state; exposes seven metrics simultaneously.",
        "<b>Hover-highlight on legend</b>: moving over a legend cell dims all states that "
        "are not of that color &mdash; direct implementation of Ndlovu et&nbsp;al. design "
        "consideration #2.",
        "<b>Pill-tab view switcher</b>: each tab swaps the encoded metric in-place; all "
        "rendered elements (map, legend, top/bottom lists, caption) update in a single pass.",
        "<b>KPI strip</b>: permanent top-of-page summary computed client-side from the CSV "
        "so the numbers remain consistent with whatever view the user has selected.",
    ], story)

    # ---------- 8. Evaluation & Findings ----------
    section("8.&nbsp;&nbsp;Evaluation and Findings", story)
    p("We evaluate the application on two axes: <i>does the Surprise encoding change the "
      "viewer's impression of the map?</i> and <i>are the patterns it reveals coherent "
      "with what a domain reader would expect?</i>", story)
    sub("8.1&nbsp;&nbsp;Encoding comparison", story)
    p("Switching from the raw-value view to the rate-surprise view produces a visibly "
      "different map. Kentucky, which dominates the raw-value view, is near the centre of "
      "the surprise scale on the rate view (its 70 incidents / 4.5M residents rate is not "
      "unusual). Maryland, which is nearly invisible on the raw-value view, lights up on "
      "the rate-surprise view with a z-score of +98. New York and California, which look "
      "severe on raw-value, land in the deep-blue (surprisingly-low) range on rate. This "
      "is the direct visual evidence of the Correll-Heer thesis: rate-based Surprise "
      "encoding recovers information that a value-based choropleth hides.", story)
    sub("8.2&nbsp;&nbsp;Substantive findings", story)
    bullets([
        "<b>RQ1.</b> The states with the highest signed surprise on per-capita incidents "
        "are Maryland, Georgia, Nevada, New Mexico, and South Carolina; the lowest are "
        "California, New York, Minnesota, Iowa, and Connecticut.",
        "<b>RQ2.</b> Yes. The Pearson correlation between the per-state rank on raw value "
        "and rank on rate-surprise is 0.11 across the 47 reporting states &mdash; effectively "
        "uncorrelated.",
        "<b>RQ3.</b> Value-surprise and rate-surprise are also weakly correlated (Figure 4); "
        "Kentucky is the only state that qualifies as distinctive on value but ordinary on "
        "rate, and the two axes together identify a larger set of &lsquo;interesting&rsquo; "
        "states than either alone.",
    ], story)

    # ---------- 9. Limitations ----------
    section("9.&nbsp;&nbsp;Limitations", story)
    bullets([
        "<b>Reporting coverage is uneven.</b> The FBI CDE is an opt-in system. Several "
        "states (notably New Hampshire, Louisiana, Hawaii, Kansas, Maine, and West Virginia) "
        "have sparse or no reporting in the 2024 release. A state with low cargo theft "
        "<i>and</i> low reporting coverage is indistinguishable from a state with truly low "
        "cargo theft.",
        "<b>The population denominator is an approximation.</b> We aggregate incorporated-"
        "place populations from SUB-IP-EST2024-POP; this omits unincorporated residents. "
        "The resulting denominator understates total state population by approximately "
        "15-25% in rural-heavy states, biasing per-capita rates upward there.",
        "<b>The funnel model saturates.</b> Classical p-values are near zero for most "
        "states because the null hypothesis of a single shared national rate is itself "
        "wrong. We work around this with the signed-root-z statistic, but a more principled "
        "treatment would use a mixed-effects model with a state-level random intercept.",
        "<b>2024 only.</b> Year-over-year comparison and the trend-analysis motivation in "
        "our original prospectus are out of scope for this release; the team has marked "
        "this as future work (&sect;10).",
    ], story)

    # ---------- 10. Future Work ----------
    section("10.&nbsp;&nbsp;Future Work", story)
    p("The prospectus motivated three future directions, each with a concrete next step:",
      story)
    bullets([
        "<b>Time series.</b> Ingest the 2020, 2022, and 2023 releases of the same table "
        "and expose a year slider to reveal state-level trend. The data pipeline is already "
        "parameterised for this.",
        "<b>Value-Suppressing Uncertainty Palettes (VSUP).</b> Ndlovu et&nbsp;al. found "
        "VSUP-encoded maps produced more consensus across participants than Surprise alone. "
        "Port Correll, Moritz, and Heer (2018) to the project; we already have the ingredient "
        "maps (rate and surprise) and only need a 2D categorical color scale.",
        "<b>Mixed-effects surprise.</b> Replace the de Moivre funnel with a partial-pooling "
        "Poisson model; the surprise statistic becomes the posterior deviation of the "
        "state-level random effect from zero. This would eliminate p-value saturation.",
        "<b>Drill-down to incident-level.</b> Table 2 (property type), Table 3 (location), "
        "and Table 5 (offense) each expose a different slice that belongs in a detail view "
        "triggered by state click.",
    ], story)

    # ---------- 11. Work Distribution ----------
    section("11.&nbsp;&nbsp;Work Distribution", story)
    p("The implementation plan assigned each team member at least one owner role:", story)
    wd = Table([
        ["Step", "Deliverable", "Owner(s)"],
        ["1. Research", "Survey of surprise / VSUP / funnel literature",
         "All four"],
        ["2. Data pipeline", "API ingest, xlsx cleanup, joined CSV, surprise pipeline",
         "Sai Krishna Vaddeboina"],
        ["3. Viz design", "Datawrapper prototype, design system, color scales",
         "Hongchao Hu, Matthew McAlarney"],
        ["4. Web app", "React / D3 / Bulma implementation, GitHub Pages deploy",
         "Hongchao Hu, Matthew McAlarney"],
        ["5. Process Book", "Written analysis, figures, references, final PDF",
         "Duncan Farquharson, Sai Krishna Vaddeboina"],
    ], colWidths=[1.25*inch, 3.05*inch, 2.5*inch])
    wd.setStyle(TableStyle([
        ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
        ("FONT", (0,1), (-1,-1), "Helvetica", 9),
        ("TEXTCOLOR", (0,0), (-1,0), ACCENT),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, SOFT]),
        ("GRID", (0,0), (-1,-1), 0.25, RULE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(wd)
    story.append(Spacer(1, 12))

    # ---------- 12. References ----------
    section("12.&nbsp;&nbsp;References", story)
    refs = [
        "Correll, M., &amp; Heer, J. (2017). Surprise! Bayesian Weighting for De-Biasing Thematic Maps. "
        "<i>IEEE Transactions on Visualization and Computer Graphics</i>, 23(1), 651&ndash;660.",

        "Correll, M., Moritz, D., &amp; Heer, J. (2018). Value-Suppressing Uncertainty Palettes. "
        "<i>Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems</i>, 1&ndash;11.",

        "Ndlovu, A., Shrestha, H., &amp; Harrison, L.&thinsp;T. (2023). Taken by Surprise? Evaluating How "
        "Bayesian Surprise &amp; Suppression Influences People's Takeaways in Map Visualizations. "
        "<i>arXiv preprint</i> 2307.15138.",

        "MacEachren, A.&thinsp;M. (1992). Visualizing Uncertain Information. "
        "<i>Cartographic Perspectives</i>, 13, 10&ndash;19.",

        "Brunsdon, C., Fotheringham, S., &amp; Charlton, M. (1998). Geographically Weighted Regression. "
        "<i>Journal of the Royal Statistical Society: Series D</i>, 47(3), 431&ndash;443.",

        "Roth, R.&thinsp;E. (2013). An Empirically-Derived Taxonomy of Interaction Primitives for "
        "Interactive Cartography and Geovisualization. <i>IEEE TVCG</i>, 19(12), 2356&ndash;2365.",

        "U.S. Federal Bureau of Investigation. (2025). Cargo Theft Tables, 2024. "
        "<i>Crime Data Explorer</i>. cde.ucr.cjis.gov.",

        "U.S. Census Bureau. (2025). Annual Estimates of the Resident Population for Incorporated "
        "Places in the United States: April 1, 2020 to July 1, 2024 (SUB-IP-EST2024-POP), Vintage 2024.",
    ]
    for r in refs:
        story.append(Paragraph("&bull;&nbsp;&nbsp;" + r, REF))

    # Build
    doc.build(story)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
