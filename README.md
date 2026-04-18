# Taken by Surprise — Mapping U.S. Cargo Theft in 2024

[![D3 v7](https://img.shields.io/badge/D3-v7-orange)](https://d3js.org/)
[![Bulma 1.x](https://img.shields.io/badge/Bulma-1.x-blueviolet)](https://bulma.io/)
[![CS 573](https://img.shields.io/badge/CS%20573-WPI%20Spring%202026-3b2e7e)](https://wp.wpi.edu/vis/)

An interactive Bayesian-Surprise dashboard for the FBI 2024 Cargo Theft release.
Final project for **CS 573 Data Visualization**, Worcester Polytechnic Institute,
Spring 2026.

| | |
| --- | --- |
| **🔗 Live site** | <https://saikrishnavaddeboina.github.io/taken-by-surprise/> |
| **🎬 Screencast** | _to be recorded — see `docs/screencast_script.md` for narration_ |
| **📖 Process book** | [`docs/process_book.pdf`](docs/process_book.pdf) |
| **📄 Prospectus** | [`docs/prospectus.pdf`](docs/prospectus.pdf) |
| **👥 Team** | Matthew McAlarney · Hongchao Hu · Duncan Farquharson · Sai Krishna Vaddeboina |
| **👨‍🏫 Instructor** | Prof. Lane T. Harrison |
| **🎓 Advisor** | Akim Ndlovu (PhD researcher, Taken-By-Surprise paper) |

---

## 1. Project summary

A raw-dollar choropleth of the 2024 FBI Cargo Theft release looks like one
bright Kentucky and 46 near-white states. A per-capita version looks almost
identical. Neither tells the viewer what we actually want to know: *which
states are unusual given their population?*

We replaced that single-metric map with an interactive dashboard that encodes
each state's **Bayesian Surprise** under a de Moivre sampling model, following
Correll & Heer (2017) and Ndlovu, Shrestha & Harrison (2023). The dashboard
presents seven synchronized views of the same dataset, a de Moivre funnel
plot so the methodology is visible, and a cross-linked data table so the raw
numbers are never hidden.

## 2. Research questions

1. Which U.S. states have *unusual* cargo-theft behavior in 2024 once the
   effect of population is held constant?
2. Does a Bayesian-Surprise encoding actually surface those states better than
   the FBI Crime Data Explorer's default raw-dollar choropleth, and if so, how
   much better?
3. Are the rate outliers and the dollar outliers the same states, or does
   each encoding tell a different story?

## 3. Key findings

- **Kentucky** reports $150.2M in stolen cargo value (31% of the national
  total) from only 70 incidents — a value outlier, but *not* a rate outlier
  (only 3.7 incidents per 100k, below the national baseline).
- **Maryland** posts 76.9 incidents per 100k — roughly **14× the 7.7 per 100k
  national baseline** and the single largest *z*-score in the dataset.
- **Georgia, Nevada, and New Mexico** emerge as outliers *only* under the
  Surprise encoding, with *z* of +51, +50, and +39 — moderate populations,
  unusually high rates.
- **California, New York, and Minnesota** look unremarkable on every
  population-weighted map but come up as surprisingly *low* under the de
  Moivre model — a story the raw map completely hides.
- **Recovery rates** vary wildly: Tennessee 34.9%, Alabama 23.4%, Kentucky 0.8%,
  national aggregate 9.7%.

## 4. The dashboard at a glance

The site is organized as six tabs, each with a distinct purpose. The same
underlying dataset is used throughout; only the encoding changes.

| Tab | Purpose |
| --- | --- |
| **Overview** | Narrative entry point. Three-view toggle (raw value / rate / surprise) with auto-annotated outliers and a "play tour" auto-cycle. |
| **Explorer** | Full seven-metric workbench: choropleth + linked ranked bar chart + histogram + state detail panel. Click-to-select propagates across all three. |
| **Funnel Plot** | The methodology made visual. Rate vs. log-population with 95% and 99% de Moivre confidence bands. The dots outside the 99% band are where the Surprise map earns its keep. |
| **Compare** | Two independent maps side-by-side. Put "Population" on the left and "Surprise — rate" on the right to watch the correlation collapse — the central lesson of the Ndlovu paper. |
| **Data Table** | Sortable, searchable, CSV-exportable — the escape hatch for a skeptical reader. |
| **Methodology** | Formulas, design rationale, references. |

### 4.1 Non-obvious UI features (per rubric)

These are features a grader might miss on first pass, so I'm calling them out
explicitly:

- **Shared selection.** Clicking a state on the map, a bar in the ranked
  chart, or a row in the data table highlights it across all three views. A
  second click deselects.
- **Legend-as-filter.** Hover any legend cell: all states *not* painted that
  color dim on the map. For diverging scales, this doubles as a way to pick
  out states inside a specific *z*-range.
- **Auto-tour.** The ▶ button on the Overview tab cycles through raw / rate /
  surprise on a 3.2-second timer so the viewer doesn't have to find the
  controls.
- **Dark / light theme.** Top-right 🌓 button toggles theme; choice is
  remembered in `localStorage`.
- **Rich tooltip.** Exposes seven numbers (population, incidents, rate,
  stolen value, $/capita, recovery %, *z*-score, surprise) simultaneously with
  a mini-bar for rate — so the viewer is never locked into the single metric
  the map happens to encode right then.
- **CSV export** on the Data Table tab saves the exact filtered view.
- **Print-friendly CSS.** The layout strips the interactive chrome when sent
  to a printer.

## 5. Data sources

| Dataset | Provider | Used for |
| --- | --- | --- |
| 2024 Cargo Theft Table 1 (per-state incidents + stolen / recovered value) | FBI Crime Data Explorer (CDE) | incidents, value, recovery |
| 2024 incorporated-place population estimates | U.S. Census Bureau, Vintage 2024 (SUB-IP-EST2024-POP) | per-capita normalization |

Both are public-domain U.S. Federal data.

The pipeline in `src/build_data.py` joins the two sources on 2-digit FIPS
codes, drops three territories with incomplete reporting, computes
*z*-scores / Bayesian Surprise, and emits a single CSV
(`data/cargo_theft_surprise_2024.csv`, **47 states × 21 columns**) that the
frontend loads at runtime.

### Files present in the working folder but intentionally not used

- `data.csv` (831 MB NIBRS master file) — out of scope; Table 1 has what we need.
- `demographic_data.csv` — reserved for a future per-demographic drill-down.
- Cargo Theft Tables 2–5 (by location, victim, property type, offense) — candidates for follow-up views.

## 6. Methodology

For each state *i*:

```
p̂  = Σ incidents / Σ population                      national baseline rate
Z_i = (rate_i − p̂) / √( p̂ · (1 − p̂) / pop_i )         de Moivre z-score
surprise_i = 2 · ( 1 − Φ(|Z_i|) )                     two-sided p-value
encoded on map: sign(Z_i) · √|Z_i|                    signed square-root
```

Because cargo theft is rare (p̂ ≈ 7.7 per 100k), Φ(|Z|) saturates for most
states and the two-sided *p*-value collapses to 0. We therefore encode
`sign(Z) · √|Z|` on the map, which preserves both the *magnitude* and the
*direction* of the deviation. Value-per-capita surprise uses a plain Gaussian
*z*-score across states.

Both design decisions (de Moivre rather than Poisson-Gamma; signed
square-root rather than log *p*) are taken from Correll & Heer (2017) and the
Ndlovu et al. (2023) paper. We follow the paper's visual recommendations
deliberately rather than innovate on the statistics.

## 7. How to run locally

The site is fully static. Any file server works:

```bash
# from the project/ directory
python3 -m http.server 8765
# open http://localhost:8765 in a browser
```

Re-running the data pipeline:

```bash
cd src
python3 build_data.py          # → data/cargo_theft_surprise_2024.csv
python3 make_figures.py        # → assets/*.png (process-book figures)
python3 make_process_book.py   # → docs/process_book.pdf
python3 make_prospectus.py     # → docs/prospectus.pdf
```

Python dependencies: `openpyxl`, `reportlab`, `matplotlib`. No API keys, no
secrets, no network access required.

## 8. Code vs. libraries

Per the rubric, here is the split between what we wrote and what is
third-party.

### What we wrote

- `index.html` — the entire dashboard (HTML, CSS, JavaScript), ~1,200 lines.
- `src/build_data.py` — data pipeline that joins FBI Table 1 with Census
  population and computes the Bayesian Surprise columns.
- `src/make_figures.py` — generates the process-book figures with matplotlib.
- `src/make_process_book.py` — builds the process book PDF using reportlab.
- `src/make_prospectus.py` — builds the prospectus PDF using reportlab.
- `docs/screencast_script.md` — narration written for the screencast.

### Third-party libraries (loaded from CDN, not vendored)

- **D3 v7** — rendering. <https://d3js.org/>
- **topojson-client v3** — TopoJSON decoding. <https://github.com/topojson/topojson-client>
- **us-atlas v3 (states-10m)** — base geography. <https://github.com/topojson/us-atlas>
- **Bulma 1.x** — CSS layout primitives only. <https://bulma.io/>
- **Google Fonts** — Inter, Source Serif 4, JetBrains Mono.

### Third-party libraries (Python pipeline)

- **openpyxl** — Excel I/O.
- **matplotlib** — static figures.
- **reportlab** — PDF generation.

No D3 wrappers (the rubric asks for this explicitly): we use D3 directly, not
nvd3, Plotly, Vega-Lite, or similar.

## 9. Repository layout

```
project/
├── index.html                            single-file web app (≈1,200 lines)
├── data/
│   ├── cargo_theft_surprise_2024.csv     joined + surprise-weighted dataset (47 × 21)
│   └── state_populations_2024.csv        aggregated state populations
├── src/
│   ├── build_data.py                     data pipeline (xlsx → CSV + surprise)
│   ├── make_figures.py                   process-book figures (matplotlib)
│   ├── make_process_book.py              process-book PDF builder (reportlab)
│   └── make_prospectus.py                prospectus PDF builder (reportlab)
├── docs/
│   ├── process_book.pdf                  main written deliverable (§ Process Book in rubric)
│   ├── prospectus.pdf                    final one-page prospectus
│   └── screencast_script.md              screencast narration
├── assets/                               generated figure PNGs (referenced from process book)
└── README.md                             this file
```

## 10. Design decisions worth justifying

A few choices that were not obvious and that are defended at greater length in
the process book:

1. **Signed square root of *z* instead of log *p*.** The *p*-value saturates
   at 0 for almost every state at this incidence rate; log *p* pushes
   everything to −∞. The signed square root preserves direction and magnitude.
2. **Funnel plot in its own tab rather than embedded in Explorer.** The plot
   is information-dense and needed the room. It is also the single clearest
   explanation of what the Surprise technique is doing.
3. **State-level granularity** (47 × 21). County or place-level data would
   make the Surprise effect more dramatic, but the FBI does not publish cargo
   theft at county level, so the join is not available. See §11.
4. **Vanilla JS rather than React.** The prospectus committed to React + D3.
   We dropped React because the deliverable is a single page with no routing;
   the React mental model is preserved (a single `state` object, explicit
   `render*()` calls) without the build tooling.
5. **No VSUP palette.** Correll, Moritz & Heer (2018) introduce a
   value-suppressing uncertainty palette for exactly this case. Implementing
   it was out of scope for this pass and is flagged as future work.

## 11. Evaluation and limitations

**What the dashboard does well.**

- Answers the research question from three angles (narrative tour, funnel
  plot, direct comparison).
- Never hides the raw numbers — the Data Table + CSV export mean claims can
  always be cross-checked.
- The cross-linked selection between map, bar chart, and table is used every
  time and does real work.

**Where it falls short.**

- 47 state-level data points is the lower bound at which the Surprise
  technique is demonstrable. County-level or place-level data would make the
  per-capita pathology much more visible. (This is the direction Matthew is
  taking in a parallel Population Map build — see *Team contributions*.)
- No uncertainty is shown on the choropleth itself. The funnel plot carries
  the uncertainty story, but a VSUP-style bivariate encoding on the main map
  is the obvious next step.
- The dataset is 2024 only. A year slider across 2020, 2022, 2023, 2024 would
  let viewers distinguish persistent patterns from one-year anomalies.

## 12. Team contributions

- **Matthew McAlarney** — dataset selection (US Cargo Theft 2024), initial
  DataWrapper prototype, implementation plan, Zoom coordination with
  Prof. Harrison and Akim Ndlovu.
- **Hongchao Hu** — visualization-design review, related-dataset sourcing
  (Kaggle UK real-estate + county-level demographic data), accessibility
  references (GeoVisAlly / CHI '26).
- **Duncan Farquharson** — prospectus authoring, deliverables coordination,
  weekly sync scheduling.
- **Sai Krishna Vaddeboina** — interactive web dashboard (`index.html`),
  data pipeline (`src/build_data.py`), process book and prospectus PDF
  builders, repository setup and GitHub Pages deployment.

## 13. References

1. Ndlovu, A., Shrestha, H., & Harrison, L. T. (2023). *Taken By Surprise?
   Evaluating How Bayesian Surprise & Suppression Influences People's
   Takeaways in Map Visualizations.* arXiv:[2307.15138](https://arxiv.org/abs/2307.15138).
2. Correll, M., & Heer, J. (2017). *Surprise! Bayesian Weighting for De-Biasing
   Thematic Maps.* IEEE TVCG 23(1), 651–660. DOI
   [10.1109/TVCG.2016.2598618](https://doi.org/10.1109/TVCG.2016.2598618).
3. Correll, M., Moritz, D., & Heer, J. (2018). *Value-Suppressing Uncertainty
   Palettes.* Proc. CHI 2018.
4. FBI Crime Data Explorer, *Cargo Theft Tables — 2024*.
   <https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi>.
5. U.S. Census Bureau, *Annual Estimates of the Resident Population for
   Incorporated Places, Vintage 2024 (SUB-IP-EST2024-POP)*.
   <https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html>.

## 14. License

Code: MIT. Data: U.S. public domain. Academic references are cited in full in
the process book (§12).

```bibtex
@article{correll2017surprise,
  title   = {Surprise! Bayesian Weighting for De-Biasing Thematic Maps},
  author  = {Correll, Michael and Heer, Jeffrey},
  journal = {IEEE Transactions on Visualization and Computer Graphics},
  volume  = {23}, number = {1}, pages = {651--660}, year = {2017}
}

@article{ndlovu2023taken,
  title   = {Taken By Surprise? Evaluating How {B}ayesian Surprise and
             Suppression Influences People's Takeaways in Map Visualizations},
  author  = {Ndlovu, Akim and Shrestha, Hilson and Harrison, Lane T.},
  journal = {arXiv preprint arXiv:2307.15138},
  year    = {2023}
}
```
