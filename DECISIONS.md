# Cookie Cats A/B Test — Decision Log

This file records **every decision we make and why**, in order. It is a working
journal, not a polished document. The point is that when someone asks "why did
you do this?", the answer is written down here in plain words — and it's *mine*.

> A note on method: writing the hypothesis, primary metric, and my prediction
> *before* touching the data is a lightweight form of **pre-registration**. It's
> what stops you from quietly rewriting the question once you've seen the answer
> (p-hacking). So the "Predictions" section below is locked in before analysis.

---

## Meta

| | |
|---|---|
| **Project** | Does moving a progression gate (level 30 → level 40) change player retention? |
| **Dataset** | Cookie Cats mobile game A/B test (~90,000 players), Kaggle: `mursideyarkin/mobile-games-ab-testing-cookie-cats` |
| **Role it targets** | Junior Data Scientist @ Nordeus — *"Causal data inference, with a main focus on AB testing"* |
| **Analyst** | Andrej Gajić |
| **Working mode** | Coached loop: **decide each step and say why → generate the code → break it to check understanding** |
| **Started** | 2026-09-08 |

---

## Predictions locked in *before* seeing any results

- **Hypothesis (H1):** moving the gate 30 → 40 changes 7-day retention. **Null (H0):** no difference; any gap is noise.
- **My prediction (Andrej, before data):** moving the gate 30 → 40 **raised** retention — `gate_40` retains *better*.
  *(Honesty note: my first phrasing said "lowered" — a wording slip; my actual reasoning was Theory A, which predicts gate_40 better.)*
- **Theory A (mine — momentum/sunk-cost):** reaching level 40 before the wall = more invested, habit formed → later gate retains better.
- **Theory B (the rival):** a gate is a forced pause; hitting it *earlier* (30) makes players stop while they still want more → earlier gate retains better.

---

## Decisions

### D0 — Project choice
Build a clean A/B analysis of the Cookie Cats retention experiment. **Why:** matches Nordeus's *"main focus on AB testing"* on real mobile-game data; small enough to understand every line.

### D1 — Working mode
Coached loop (decide → generate → break), not "AI writes it, I read it". **Why:** the project's value is that I can *defend* it; reading an explanation gives borrowed understanding that collapses under a follow-up.

### D2 — Where we build vs. run
Build & verify the canonical notebook in the repo; use Google Colab as the hands-on surface. **Why:** no broken cells reach the repo; re-running it myself is where I take ownership.

### D3 — Sample Ratio Mismatch (SRM): proceed and document
Split 44,700 / 45,489 (49.56% / 50.44%); binomial vs 50/50 gives p = 0.0087. Statistically flagged, but only because n is huge (1 SD ≈ ±0.17pp; ~2.6 SD out). Deviation is 0.44pp and the gate **cannot** cause it (assignment at install, before any gate). **→ proceed, document the caveat.**

### D4 — The outlier player: drop it
Remove `userid 6390605` (49,854 rounds in 14 days ≈ 3,560/day — bot or logging error). Distorts engagement stats and any round-count model. Break-it #1 confirmed it does **not** affect the retention result.

### D5 — Primary metric: `retention_7` (secondary: `retention_1`)
Day-1 retention is easy and noisy (novelty); day-7 signals a *lasting habit*. Chosen before seeing results. `retention_1` kept as a secondary consistency check.

### D6 — Significance test: chi-square (z-test as confirmation)
Chi-square test of independence on the 2×2 table (interview-friendly, tests dependence directly). Two-proportion z-test run alongside as a cross-check. **Why two:** they're the same math for a 2×2 (z² ≈ chi²), so agreement is a sanity check, not new evidence.

### D7 — Bootstrap: 1,000 iterations
Resample players with replacement 1,000×, recompute the gap each time. **Why:** turns the yes/no p-value into a *range* + a *confidence* ("how big, how sure"), which is what a product manager actually needs. Seed fixed (42) for reproducibility.

### D8 — Include the optional prediction model (Phase 4)
Logistic regression predicting `retention_7`. **Why include:** the Nordeus posting lists *"Applied Machine Learning"*, so a small, fully-understood model strengthens the fit. **Key result & the real lesson:** AUC = 0.88 looked strong, but `sum_gamerounds` (14-day window) leaks information from *past* the day-7 target. Dropping it → AUC 0.72, the honest number. Reported both, with the leakage called out.

### D9 — Recommendation
**Keep the gate at level 30; do not ship the move to 40.** Confident in the direction, modest in size, with revenue flagged as an unmeasured trade-off.

---

## Findings (Phase 2)

**Primary — 7-day retention** *(outlier dropped)*
- gate_30 = **19.02%**, gate_40 = **18.20%** → gap **+0.82 pp** (gate_30 better; −4.3% relative for gate_40)
- chi-square **p = 0.0016** (z-test agrees) → **statistically significant**
- bootstrap: gate_30 ahead in **1000/1000** resamples; 95% CI **[+0.32, +1.34] pp** (never crosses 0)

**Secondary — 1-day retention**
- gate_30 = 44.82%, gate_40 = 44.23% → gap **+0.59 pp**, **p = 0.075 → not significant**
- **same direction** as day-7, weaker signal — consistent with day-1 being noisier (vindicates the primary-metric choice)

**Verdict on the theories:** the data supports **Theory B** (earlier gate retains better), contradicting my Theory A prediction. Effect is **small in size but rock-solid in direction.**

---

## Open decisions (queued)

- [x] SRM → proceed & document (D3)
- [x] Outlier → drop (D4)
- [x] Primary metric → `retention_7` (D5)
- [x] Significance test → chi-square + z-test (D6)
- [x] Bootstrap → 1,000 iterations (D7)
- [x] Stretch model → included (D8)
- [x] Recommendation → keep gate at 30 (D9)

All core decisions locked. Deliverable: `cookie_cats_ab_test.ipynb` + `README.md`.

---

## Break-it experiments (predict first, then run)

| # | What we broke | My prediction | What actually happened | Lesson |
|---|---|---|---|---|
| 1 | Drop vs keep the outlier player | could mess up the analysis | gap +0.820 → +0.818 pp, p 0.00160 → 0.00164 — **no change** | An outlier's danger depends on the metric: it wrecks an *average* but is invisible to a *rate* (1 row in 90k). |
| 2 | Remove the leaky `sum_gamerounds` from the model | it drops | AUC 0.88 → 0.72 | That 0.16 was leakage — a 14-day feature peeking past the 7-day target. 0.72 is the honest number. |
