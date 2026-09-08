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

- **Hypothesis under test (H1):** moving the gate from level 30 to level 40
  changes 7-day retention.
- **Null (H0):** retention is the same in both groups; any gap is noise.
- **My prediction (Andrej, before data):** moving the gate 30 → 40 **raised**
  retention — i.e. `gate_40` retains *better*.
  *(Honesty note: my first phrasing said "lowered"; that was a wording slip —
  my actual reasoning was Theory A below, which predicts gate_40 is better.)*
- **My mechanism — Theory A (momentum / sunk-cost):** letting players reach
  level 40 before the wall means they've invested more and formed a habit, so
  they're more likely to keep playing. A later gate → better retention.
- **The competing story I'm betting against — Theory B (forced-break /
  anti-burnout):** a gate is a forced pause; hitting it *earlier* (30) makes
  players stop while they still want more, so they come back. Earlier gate →
  better retention. The data decides between A and B.

---

## Decisions

### D0 — Project choice
**Decision:** Build a clean A/B analysis of the Cookie Cats retention experiment.
**Why:** Nordeus's posting names *"a main focus on AB testing"* and *"modelling
user behaviour from real data."* This is exactly that, on real mobile-game data —
not a generic Titanic/Iris demo. Small enough to understand every line.

### D1 — Working mode
**Decision:** Coached loop (decide → generate → break), not "AI writes it, I read it."
**Why:** The value of this project is that I can *defend* it in an interview.
Reading an explanation of code gives a weak, borrowed understanding that collapses
under one follow-up. Deciding first and breaking things after builds understanding
I can defend.

### D2 — Where we build vs. where I run
**Decision:** Build & verify the canonical notebook in the repo; use Google Colab
as the hands-on surface to re-run and break it.
**Why:** Building where the code actually executes means no broken cells reach the
repo. Re-running it myself in Colab is where I take ownership.

### D3 — Sample Ratio Mismatch (SRM): proceed and document
**Decision:** Note the SRM, but proceed with the analysis.
**Why:** Split is 44,700 / 45,489 (49.56% / 50.44%). A binomial test vs a perfect
50/50 gives p = 0.0087, so the deviation is *statistically* detectable — but only
because n is huge (1 SD of noise ≈ ±0.17pp; we're ~2.6 SD out). The deviation is
just 0.44pp, and the gate **cannot** have caused it: assignment happens at install,
long before a player ever reaches level 30 or 40. So: small + mechanistically
impossible to be a treatment effect → proceed, and write down the caveat.
Interview line: *"I check SRM first; here it was flagged but tiny and can't be
caused by the treatment, so I proceeded and documented it."*

### D4 — The outlier player: drop it
**Decision:** Remove `userid 6390605` (49,854 rounds in 14 days).
**Why:** ~3,560 rounds/day is not a real human (bot or logging error), and it
badly distorts engagement summaries and any round-count model. It's also
internally weird (retention_1=False but retention_7=True).
**Open prediction to test:** I expect it *could* mess up the analysis — but
retention is one True/False per player, so this is 1 row in ~44,700. **Break-it
experiment #1** will measure the actual effect on the retention gap.

### D5 — Primary metric: `retention_7` (secondary: `retention_1`)
**Decision:** 7-day retention is the primary outcome, chosen before seeing results.
**Why:** Almost every game has decent day-1 retention (novelty, curiosity); it's
easy and noisy. Day-7 retention is the signal that a *lasting habit* formed, which
is what actually matters for a game's long-term health. `retention_1` is kept as a
secondary check — agreement across both is more convincing; a conflict is worth
explaining.

---

## Open decisions (queued)

- [x] SRM → proceed & document (D3)
- [x] Outlier → drop (D4)
- [x] Primary metric → `retention_7` (D5)
- [ ] **Significance test:** chi-square vs two-proportion z-test — which, and why?
- [ ] **Bootstrap:** how many iterations, and what does it add over the p-value?
- [ ] **Stretch model (optional):** logistic regression to predict `retention_7`?

---

## Break-it experiments (predict first, then run)

_Logged as we do them: what we changed, what I predicted, what actually happened,
and what it taught me._

| # | What we broke | My prediction | What actually happened | Lesson |
|---|---|---|---|---|
| 1 | Drop vs keep the outlier player | _could mess up the analysis_ | _(pending)_ | _(pending)_ |
