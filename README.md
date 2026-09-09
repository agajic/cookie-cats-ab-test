# Cookie Cats A/B test: does moving the progression gate change player retention?

**[Read the case study →](https://cookie-cats-ab-test-andrej.vercel.app/)**

An end-to-end analysis of a real mobile-game A/B test. *Cookie Cats* moved its first
progression gate from level 30 to level 40, and this project tests whether that change
affected how many players came back.

> **Moving the gate to level 40 reduced 7-day retention, from 19.0% to 18.2%
> (p = 0.0016). Recommendation: keep the gate at level 30.**

| | |
|---|---|
| Case study | [cookie-cats-ab-test-andrej.vercel.app](https://cookie-cats-ab-test-andrej.vercel.app/) |
| Notebook | [`cookie_cats_ab_test.ipynb`](cookie_cats_ab_test.ipynb) |

## The question

A gate forces players to wait, or pay, to continue past a level. It paces the game and it
sells at the same time. The team moved that gate from level 30 to level 40, giving players
ten more levels of free play before hitting the wall. Did more of them come back?

## The data

90,189 players ([Kaggle: Mobile Games A/B Testing, Cookie Cats](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats)),
randomly assigned at install to `gate_30` (control) or `gate_40` (variant). The fields that
matter are `retention_1` and `retention_7` (did the player come back 1 or 7 days after
installing) and `sum_gamerounds` (rounds played in the first 14 days).

## Approach

- **Data checks before any comparison:** group balance (sample ratio mismatch), a single implausible player logging 49,854 rounds in 14 days, and the engagement distribution.
- **Primary metric fixed in advance:** `retention_7`. Day-1 retention is novelty and it is noisy; day 7 is a stronger sign of a lasting habit. Choosing before looking is what prevents cherry-picking.
- **Significance:** a chi-square test of two proportions, with a two-proportion z-test as a cross-check.
- **Uncertainty:** a 1,000-resample bootstrap of the retention gap, giving a range and a confidence rather than a yes/no.
- **Secondary check:** `retention_1`, to see whether the shorter horizon agrees.

## Findings

- `gate_30` retained 19.02% at day 7 against 18.20% for `gate_40`: a gap of **0.82 percentage points**, or 4.3% of the control's retention.
- The gap is real. Chi-square gives **p = 0.0016**, and the control came out ahead in **1,000 of 1,000** bootstrap resamples, with a 95% interval of +0.32 to +1.34 points that never crosses zero.
- `retention_1` points the same way (+0.59 points) but does not reach significance (p = 0.075), which is consistent with day 1 being a noisier signal and supports having fixed day 7 as primary in advance.
- The effect is small, and its direction is not in doubt. The most plausible explanation is a forced-break effect: an earlier gate makes players pause while they still want more, so they come back.

## Recommendation

**Keep the gate at level 30; do not ship the move to 40.** I am confident in the direction,
the size is modest, and a full decision would also need to weigh revenue, which this dataset
cannot show.

## A prediction model, and a lesson in leakage

A logistic-regression baseline predicting `retention_7` scored **AUC 0.881**, which is too
good for three crude features. `sum_gamerounds` counts 14 days of play while the target is
retention at day 7, so the feature covers a window that runs past the event it predicts and
partly contains the answer. That is data leakage. Removing it drops AUC to **0.716**, and
0.716 is the number I would report. The lesson outlives the score: always ask whether a
feature would really be available, and would not already encode the answer, at the moment
you would have to make the prediction.

## What I would check next

- **Segment** casual against heavy players, since an average can hide two opposite effects.
- **A longer window** (day 30 or 90), to see whether the effect fades or compounds.
- **Revenue, not just retention.** The gate is also where players pay to skip, so `gate_40` could earn more per player even while retaining fewer. This dataset has no revenue column, so the trade-off is unmeasured here.
- **A formal power analysis**, stating the smallest effect this design could reliably detect.

## Repo contents

| Path | What it is |
|---|---|
| `cookie_cats_ab_test.ipynb` | The full analysis, top to bottom |
| `site/` | Source of the case-study site |
| `DESIGN.md` | How the site was designed and built |
| `cookie_cats.csv` | The dataset |
| `requirements.txt` | Dependencies |

## Running it

```bash
pip install -r requirements.txt
jupyter notebook cookie_cats_ab_test.ipynb
```

The notebook also opens directly in Google Colab. Every figure on the case-study site is
drawn at runtime from `site/data.js`, which `site/generate_data.py` regenerates from the
dataset, so the page cannot drift from the analysis.

## Contact

Andrej Gajić · [andrejgajic777@gmail.com](mailto:andrejgajic777@gmail.com) · Novi Sad, Serbia
