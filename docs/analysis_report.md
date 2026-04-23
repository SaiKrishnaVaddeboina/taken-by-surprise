# Analysis Report

*Final Project — Taken by Surprise: Mapping U.S. Cargo Theft in 2024*
*CS 573 Data Visualization · WPI · Spring 2026*

---

## 1. Overview

This section of the process book answers the three research questions we
posed at the start of the project by working directly with the visualizations
we built. All figures and interaction behaviors referenced below live in the
web application (`index.html`), and the numerical results come from the
cleaned dataset `data/cargo_theft_surprise_2024.csv`.

The three research questions were:

1. Which U.S. states have unusual cargo-theft behavior in 2024 once the
   effect of population is held constant?
2. Does a Bayesian-Surprise encoding actually surface those states better
   than the FBI Crime Data Explorer's default raw-dollar choropleth?
3. Are the rate outliers and the dollar outliers the same states, or does
   each encoding tell a different story?

## 2. Which states are unusual?

The de Moivre funnel plot is the clearest place to answer this. Each state
is positioned on a log-scaled population axis and a rate axis, and the 95%
and 99% confidence envelopes are drawn under the national incident rate.
A state outside the 99% band is statistically unusual, not just noticeable.

Under the 2024 data, the states that fall outside the 99% confidence band on
the high side are:

- **Maryland** — 76.9 incidents per 100k residents, 14× the national
  baseline of 7.7, z ≈ +98.
- **Georgia** — z ≈ +51.
- **Nevada** — z ≈ +50.
- **New Mexico** — z ≈ +39.
- **Alabama**, **Kentucky**, and **Tennessee** also sit above the 99% band
  by smaller margins.

On the low side, with rates materially below what sampling would predict for
their populations:

- **California**, **New York**, **Minnesota** — all populous states where
  the raw counts are moderate but the per-capita rate is well below the
  national baseline.

These are the states the Surprise encoding is built to surface, and the
funnel plot confirms that the signal is not a visualization artifact.

## 3. Does Surprise beat the raw choropleth?

Yes, and the Compare tab is the direct evidence. When we put
`Population (2024)` on the left panel and `Surprise — rate` on the right, the
two maps share almost no structure: the bright states on the population map
(California, Texas, Florida, New York) are not the bright states on the
surprise map. By contrast, if we put `Population` next to `Incidents` or even
`Incidents per 100k`, the two maps are visually correlated — the raw-count
map is still partially reading the population signal.

This is the central claim of Ndlovu et al. (2023) reproduced on 2024 data:
raw-count and even per-capita encodings leak the population distribution
into the thematic variable, and the Bayesian Surprise encoding is the one
that suppresses it.

The auto-tour on the Overview tab makes the same point in a narrative form.
Cycling through the three encodings, Kentucky dominates the raw-value view,
recedes on the rate view, and Maryland emerges as the dominant outlier.
Georgia and Nevada only become legible once the surprise encoding is active.

## 4. Are rate outliers and dollar outliers the same states?

No. This was the most surprising finding of the project for us.

- **Kentucky** is the extreme dollar outlier: $150.2M in stolen value, which
  is 31% of the entire national total, from only 70 incidents. Per-capita
  stolen value is $33.62 — almost an order of magnitude above any other
  state. But Kentucky's incident rate is 3.7 per 100k, which is *below* the
  national baseline of 7.7. Kentucky's story is "a small number of very
  high-value thefts," and that story is only visible on the value-surprise
  map and the tooltip, not on the raw-dollar choropleth.
- **Maryland** is the extreme rate outlier but a modest dollar outlier — the
  opposite of Kentucky. High volume of incidents, lower average value per
  incident.
- **Georgia, Nevada, New Mexico** are rate outliers with modest dollar
  totals. They only become visible on the rate surprise map.

In other words, each encoding tells a genuinely different story. The raw
choropleth we see on the FBI Crime Data Explorer answers the question "which
states had the most dollar loss," and that question has a clean answer
(Kentucky). The Surprise map answers the question "which states are unusual
given their population," which has a different and more useful answer for
policy-minded readers.

## 5. What the recovery-rate view shows

The recovery rate is a secondary variable we did not model with Surprise,
but the visualization is informative. Tennessee recovers 34.9% of stolen
value, Alabama 23.4%, and Kentucky 0.8%. The national aggregate is 9.7%.
This is a state-policy story — states differ wildly in how much of what is
stolen is eventually recovered — and we chose to expose it as a separate
view rather than blend it into the surprise encoding, because recovery is
conceptually a different kind of outcome.

## 6. How the dashboard helped answer the questions

Three features of the dashboard did the real analytical work.

1. **The funnel plot** gave the statistical ground truth. Without it, the
   surprise map is a colorful assertion; with it, the claim "Maryland is
   significantly above the 99% confidence band" is directly visible.
2. **The cross-linked selection** between map, ranked bar chart, and data
   table meant that whenever an interesting state surfaced on one view, we
   could confirm the numbers on the other two. This cut the time to
   validate a finding from minutes to seconds.
3. **The auto-tour on the Overview tab** made the Kentucky-to-Maryland
   handoff legible to a viewer who hasn't read the paper. This was the
   single feature that non-technical reviewers responded to most strongly in
   our informal walkthroughs.

## 7. Limitations and next steps

The analysis is state-level because the FBI does not publish cargo theft at
county level. 47 data points is the lower bound at which the Surprise
technique is demonstrable, and a natural next step is to move to a dataset
that is published at county or incorporated-place level so the per-capita
pathology has more cells to operate on. A population map at the town level,
which the team explored mid-project, is the most promising candidate.

The choropleth does not currently show per-state uncertainty; the funnel
plot carries that information instead. A follow-up version of the dashboard
would likely use a Value-Suppressing Uncertainty Palette (Correll, Moritz &
Heer, 2018) to show confidence and magnitude on the main map simultaneously.

Finally, the dataset covers 2024 only. A longitudinal view across
2020/2022/2023/2024 would let a viewer distinguish persistent state-level
patterns from one-year anomalies, which is particularly relevant for a
release where Kentucky's numbers are dramatic enough to raise questions
about reporting practices as much as actual theft.

## 8. Takeaway

The raw-dollar choropleth that the FBI currently publishes is an honest
summary of dollar loss, but it is an incomplete one. It lets a single state
with a small number of very-high-value incidents define the visual story
for the entire country, and it systematically hides states whose rate of
cargo theft is unusual given their population. Re-encoding the same data as
Bayesian Surprise under a de Moivre model is a small change in method and a
large change in what the viewer walks away believing.
