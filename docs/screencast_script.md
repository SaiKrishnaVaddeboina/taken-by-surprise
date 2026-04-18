# Screencast Script — *Taken by Surprise*

**Target runtime:** 4 minutes (±15 seconds).
**Platform:** QuickTime screen recording at 1280×800, voice-over via AirPods or USB mic.
**Delivery tempo:** ~150 wpm, unhurried.
**Visual rhythm:** one tab change per ~20 seconds.

---

## 0:00 — 0:20  Open on the landing page

> "This is *Taken by Surprise*, a CS 573 final project from Worcester Polytechnic
> Institute. I'm Sai Krishna Vaddeboina, speaking for the team of four: myself,
> Matthew McAlarney, Hongchao Hu, and Duncan Farquharson. For the next four minutes
> I'm going to walk you through what the project is, why we built it, and the one
> finding that surprised us the most."

**On screen:** full page visible, page loaded, "Stolen value ($)" tab active.

## 0:20 — 0:50  The problem we're solving

> "Our dataset is the FBI Crime Data Explorer's 2024 Cargo Theft release —
> 16,183 incidents, $483 million stolen, 9.7% recovered. This is the view you
> get on the FBI's own website: a choropleth of raw stolen dollars by state.
> Notice how Kentucky dominates the map. That one state accounts for $150
> million of the total from only seventy incidents. Every other state fades
> toward white. That's the storytelling problem we set out to fix."

**On screen:** hover Kentucky to show tooltip with $150.2M / 70 incidents / $58.42
per capita.

## 0:50 — 1:20  Per-capita normalization doesn't save us

> "The obvious first fix is to divide by population. Here's stolen value per
> capita — Kentucky is still the outlier, and now most states are pinned near
> zero. We've scaled the problem, not solved it. The map still encodes one
> dimension — value — and still hides the states where cargo theft is unusual
> *given* their population."

**On screen:** click "Stolen value per capita" tab, pause on the updated map.

## 1:20 — 2:10  The Surprise encoding

> "This is where we adopt a technique from Correll and Heer's 2017 paper and
> Akim Ndlovu's 2023 follow-up study — both out of the WPI visualization group.
> It's called a Bayesian Surprise Map. For every state we compute the expected
> cargo theft rate given its population, and ask: how many standard errors
> away from the national rate is the observed rate? Red means surprisingly
> higher than expected. Blue means surprisingly lower."

> "Look what changes. Maryland — nearly invisible on the raw-dollar map —
> lights up red. Its rate is 76.9 incidents per 100,000, against a national
> baseline of 7.7. Georgia, Nevada, and New Mexico all light up. And the
> states that dominated the first map — California, New York — are now dark
> blue: surprisingly *low* cargo theft given their population."

**On screen:** click "Surprise — rate" tab. Hover Maryland, then California, to
show the diverging surprise values in the tooltip.

## 2:10 — 2:40  Why two surprise axes

> "One more insight. Here's the surprise encoding on value per capita instead
> of incidents. Kentucky re-appears as the only extreme outlier. That's the
> cross-check we wanted: Maryland is extreme on *rate*, Kentucky is extreme on
> *value*, and no state is extreme on both. If you only ever look at one
> metric, you miss half the story. Our tooltip exposes both, every time."

**On screen:** click "Surprise — value" tab. Open tooltip on Kentucky and then on
Maryland to contrast.

## 2:40 — 3:10  Population companion map

> "The Ndlovu paper specifically warns that Surprise maps can draw the viewer
> toward populous regions — participants in their study systematically picked
> high-population counties when asked to identify extremes. Our companion
> population map is here as the reader's sanity check: Maryland has 6 million
> residents; Kentucky has 4.5 million; California has 40 million. If a state
> is lit up on Surprise and quiet on Population, that's not a population
> artifact — it's a real regional pattern."

**On screen:** click "Population (2024)" tab.

## 3:10 — 3:40  Methodology and reproducibility

> "Everything behind this map is reproducible with three Python commands.
> `build_data.py` ingests the FBI xlsx and the Census population file, computes
> the de Moivre funnel surprise score, and writes the joined CSV. The same
> pipeline regenerates the Process Book PDF and every figure in it. No API
> keys, no secrets, 47 rows and 21 columns of fully-audited data."

**On screen:** scroll down to the Methodology section of the page, showing the
formula block.

## 3:40 — 4:00  Close

> "The full Process Book, the data pipeline, and the live app are on our
> GitHub. If you take one thing from this walkthrough, let it be this: the
> default choropleth is not neutral. It amplifies population and dominant
> outliers and hides the patterns that matter. Surprise maps are one
> deliberate, statistically grounded fix. Thanks for watching."

**On screen:** scroll to the References section, fade to the repository URL
`github.com/MacCode7110/grad-final`.

---

## Cut-list (if runtime is tight)

Trim first, in order:
1. Section *1:20 — 2:10* pre-amble ("This is where we adopt…") — cut 10 sec.
2. Kentucky value-per-capita re-mention at 0:50–1:20 — 8 sec.
3. Close can shorten to *"The full Process Book and data pipeline are on our GitHub. Thanks for watching."* — saves 10 sec.

## Producer notes

- Open `index.html` at 120% zoom so the map and the right-rail Top-5 list both
  fit at 1280×800.
- Pre-populate the tooltip on the first hover by mousing over Kentucky before
  hitting record, then snap the cursor back to the frame edge.
- Record the audio in a single take against the pre-timed on-screen actions;
  cross-fade the two tracks in post rather than retaking.
- Export: 1080p ProRes, upload to YouTube as *unlisted*, embed the link under
  the site header as a `<video>` tag fallback so it works on the GitHub Pages
  deployment even if YouTube is blocked.
