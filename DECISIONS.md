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
| **Working mode** | Coached loop: **I decide each step and say why → generate the code → break it to check understanding** |
| **Started** | 2026-09-08 |

---

## Predictions locked in *before* seeing any results

- **Hypothesis under test (H1):** moving the gate from level 30 to level 40
  changes 7-day retention.
- **Null (H0):** retention is the same in both groups; any gap is noise.
- **My prediction (Andrej, before data):** moving the gate 30 → 40 **lowered**
  retention.
- **My reasoning for that prediction:** _[Andrej to fill — one line: why would a
  later gate lower retention?]_

---

## Decisions

### D0 — Project choice
**Decision:** Build a clean A/B analysis of the Cookie Cats retention experiment.
**Why:** Nordeus's posting names *"a main focus on AB testing"* and *"modelling
user behaviour from real data."* This is exactly that, on real mobile-game data —
not a generic Titanic/Iris demo. It's small enough to understand every line.
**Alternatives considered:** generic ML demo (rejected: doesn't match the role).

### D1 — Working mode
**Decision:** Coached loop (decide → generate → break), not "AI writes it, I read it."
**Why:** The value of this project is that I can *defend* it in an interview.
Reading an explanation of code produces a weak, borrowed understanding that
collapses under one follow-up question. Deciding first and breaking things after
is what builds understanding I can defend.

### D2 — Where we build vs. where I run
**Decision:** Build & verify the canonical notebook in the repo; use Google Colab
as the hands-on surface to re-run and break it.
**Why:** Building where the code is actually executed means no broken cells reach
the repo. Re-running it myself in Colab is where I take ownership.

---

## Open decisions (queued — to be made as we reach them)

- [ ] **Primary metric:** `retention_7` vs `retention_1` — which is primary, and why decide *before* seeing results?
- [ ] **The outlier player** (famously huge `sum_gamerounds`): keep or drop, and why?
- [ ] **SRM check:** is the group split clean enough to trust the experiment?
- [ ] **Significance test:** chi-square vs two-proportion z-test — which, and why?
- [ ] **Bootstrap:** how many iterations, and what does it add over the p-value?
- [ ] **Stretch model (optional):** logistic regression to predict `retention_7` — worth including?

---

## Break-it experiments (predict first, then run)

_Logged as we do them: what we changed, what I predicted, what actually happened,
and what it taught me._

| # | What we broke | My prediction | What actually happened | Lesson |
|---|---|---|---|---|
| | | | | |
