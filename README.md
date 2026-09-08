# Cookie Cats A/B Test — does moving the progression gate change player retention?

A clean, end-to-end analysis of a real mobile-game A/B test. *Cookie Cats* moved its first
progression **gate** from **level 30** to **level 40**, and this project tests whether that
change affected how many players came back.

> **TL;DR — moving the gate to level 40 *reduced* 7-day retention (19.0% → 18.2%, p = 0.0016).
> Recommendation: keep the gate at level 30.**

Full analysis: [`cookie_cats_ab_test.ipynb`](cookie_cats_ab_test.ipynb).
The reasoning behind every decision is logged step-by-step in [`DECISIONS.md`](DECISIONS.md).

**There is also an interactive write-up of this analysis** — the same findings as a visual,
scrollable case study, with every chart drawn at runtime from the analysis output. Source in
[`site/`](site/); see [`DESIGN.md`](DESIGN.md) for how it was built.

## The question
A "gate" forces players to wait (or pay) to continue past a level. The team moved that gate
from level 30 to level 40. Did more players come back as a result?

## The data
~90,000 players ([Kaggle: Mobile Games A/B Testing — Cookie Cats](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats)),
randomly assigned to `gate_30` (control) or `gate_40` (variant). Key fields: `retention_1`
and `retention_7` (came back 1 / 7 days after install), and `sum_gamerounds` (rounds played
in the first 14 days).

## Approach
- **Data checks first** — group balance (Sample Ratio Mismatch), the famous outlier player, and the engagement distribution.
- **Primary metric chosen up front** — `retention_7`. Day-1 retention is noisy (novelty); day-7 is a stronger signal of a *lasting habit*. Deciding before looking avoids cherry-picking.
- **Significance** — chi-square test of two proportions, with a two-proportion z-test as a cross-check.
- **Uncertainty** — a 1,000-iteration bootstrap of the retention difference (range + confidence, not just a yes/no).
- **Secondary check** — `retention_1`.

## Findings
- gate_30 retained **19.0%** at day 7 vs **18.2%** for gate_40 — a **0.82pp (~4% relative)** drop from moving the gate.
- **Statistically real:** chi-square **p = 0.0016**; the control was ahead in **1,000 / 1,000** bootstrap resamples (95% CI **+0.32 to +1.34pp**, never crossing zero).
- `retention_1` agrees in direction but is **not** significant (p = 0.075) — consistent with day-1 being a noisier signal, which is exactly why day-7 was the primary metric.
- **Small effect, rock-solid direction.** The most plausible explanation is a *forced-break / anti-burnout* effect: an earlier gate makes players pause while they still want more, so they come back.

## Recommendation
**Keep the gate at level 30 — do not ship the move to 40.** I'm confident in the direction;
the size is modest; and a full decision should also weigh revenue (see below).

## Bonus — a prediction model, and a lesson in leakage
A logistic-regression baseline predicting `retention_7` scored **AUC 0.88** — but
`sum_gamerounds` counts 14 days of play, which runs *past* the day-7 target, so it leaks the
outcome. Dropping it (keeping only genuinely-early signals) drops AUC to **0.72** — the
honest, deployable number. That 0.16 gap *was* the leakage. The lesson matters more than the
score: always ask whether a feature would really be available, and wouldn't already encode
the answer, at the moment you'd make the prediction.

## Limitations & what I'd do next
- **Segment** casual vs heavy players — an average can hide opposite effects.
- **Longer window** (day 30/90) to check for novelty effects fading or growing.
- **Revenue, not just retention** — the gate is also a monetisation lever (players pay to skip); gate_40 could earn more per player even if slightly fewer return. This dataset has no revenue column, so that trade-off is unmeasured here.
- A formal **power analysis**.

## Repo contents
| File | What it is |
|---|---|
| `cookie_cats_ab_test.ipynb` | The full analysis, top to bottom |
| `DECISIONS.md` | Decision journal — why each choice was made |
| `cookie_cats.csv` | The dataset (~90k players) |
| `requirements.txt` | Dependencies |
| `site/` | Interactive case-study site (static, deployed on Vercel) |
| `DESIGN.md` | Design documentation for the site |

## How to run
```bash
pip install -r requirements.txt
jupyter notebook cookie_cats_ab_test.ipynb
```
Or open the notebook directly in Google Colab.
