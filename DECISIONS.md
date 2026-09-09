# Decision log

Why each analytical choice was made, in the order I made it. I kept this so that when
someone asks "why did you do it that way?", the answer is written down rather than
reconstructed afterwards.

One note on method. I wrote the hypothesis, the primary metric and my own prediction down
*before* computing any result. That is a lightweight form of pre-registration, and it is what
stops you quietly rewriting the question once you have seen the answer.

## The experiment

| | |
|---|---|
| Question | Does moving a progression gate from level 30 to level 40 change player retention? |
| Data | Cookie Cats mobile game A/B test, 90,189 players |
| Design | Players randomly assigned at install to `gate_30` (control) or `gate_40` (variant) |
| Primary metric | 7-day retention, fixed in advance |
| Analyst | Andrej Gajić |

## What I predicted before looking

- **H0:** 7-day retention is the same in both groups; any gap is noise.
- **H1:** the two groups differ.
- **My prediction:** `gate_40` would retain better.

I backed **Theory A**: a player who reaches level 40 before hitting the wall has invested
more and formed more of a habit, so a later gate should retain better. The rival was
**Theory B**: a gate is an enforced pause, so hitting it earlier stops players while they
still want more and brings them back.

The data supported Theory B. Being wrong is the most useful thing in the project, because it
shows the result was not obvious and had to be measured rather than argued about.

## Decisions

### 1. Sample ratio mismatch: proceed, and write down the caveat
The split came out 44,700 / 45,489, or 49.56% / 50.44%. A binomial test against a perfect
50/50 gives p = 0.0087, so it is statistically detectable. It is detectable only because the
sample is huge: one standard deviation of random wobble is about ±0.17 percentage points, so
a 0.44-point deviation sits roughly 2.6 SD out.

Two things settled it. The magnitude is trivial, and the gate cannot have caused it, because
assignment happens at install, long before any player reaches level 30 or 40. So I proceeded
and recorded the caveat instead of either ignoring it or discarding a usable experiment.

### 2. The outlier player: drop it
One row logs 49,854 rounds in 14 days, about 3,561 a day. That is not a human; it is a bot or
a logging error. The next-highest player managed 2,961.

I dropped it because it distorts engagement statistics and any model using round counts. It
turned out to make no difference to the retention result (checked below), but it is still not
a valid observation.

### 3. Primary metric: `retention_7`, with `retention_1` as a secondary check
Nearly every game has decent day-1 retention, because day one is novelty and it is noisy.
Day-7 retention is the first honest sign that a habit formed, which is what a game's health
actually depends on. I fixed this before seeing any result, so that I could not later choose
whichever metric happened to be significant.

### 4. Significance test: chi-square, with a z-test as a cross-check
Retention is a yes/no outcome per player, so this compares two proportions. The chi-square
test of independence asks directly whether returning is linked to the group. I ran a
two-proportion z-test alongside it. For a 2×2 table the two are the same mathematics
(z² ≈ chi²), so their agreement is a sanity check on my setup, not extra evidence.

### 5. Bootstrap: 1,000 resamples
A p-value answers "is it real" and nothing else. Resampling the players with replacement and
recomputing the gap 1,000 times gives a range and a confidence, which is what someone
deciding the game's design actually needs. The seed is fixed at 42 so the figures reproduce.

### 6. Include a prediction model
A logistic regression predicting `retention_7`: binary target, readable coefficients, the
simplest thing that could work. I chose ROC-AUC over accuracy because 81% of players never
return, so a model that always predicts "won't return" already scores 81% accuracy while
being useless.

It scored 0.881, which was too good for three crude features. `sum_gamerounds` counts 14 days
of play while the target is retention at day 7, so the feature covers a window running past
the event it predicts. That is data leakage. Removing it drops AUC to 0.716, and 0.716 is the
number I would report.

### 7. Recommendation: keep the gate at level 30
Do not ship the move to 40. Confident in the direction, modest about the size, and explicit
that revenue is an unmeasured trade-off, since the gate is also where players pay to skip.

## Findings

**Primary, 7-day retention** (outlier removed)

- `gate_30` 19.02%, `gate_40` 18.20%, a gap of 0.82 percentage points, or 4.3% of the control's retention
- chi-square p = 0.0016, z-test agrees: statistically significant
- bootstrap: the control was ahead in 1,000 of 1,000 resamples; 95% interval +0.32 to +1.34 pp, never crossing zero

**Secondary, 1-day retention**

- `gate_30` 44.82%, `gate_40` 44.23%, a gap of 0.59 pp, p = 0.075, not significant
- Same direction as day 7 but a weaker signal, which is consistent with day 1 being noisier
  and supports having fixed day 7 as primary in advance.

**Effect size:** small, with a direction that is not in doubt.

## Robustness checks

I predicted the outcome of each before running it.

| Change | What I expected | What happened | What it taught me |
|---|---|---|---|
| Drop vs. keep the outlier player | that it could distort the analysis | gap 0.820 → 0.818 pp; p 0.00160 → 0.00164 | An outlier's danger depends on the metric. It would wreck an average, but one row in 90,000 cannot move a rate. |
| Remove the leaking `sum_gamerounds` from the model | that AUC would fall | AUC 0.881 → 0.716 | That 0.165 was leakage: a 14-day feature peeking past a 7-day target. |

## What I would check next

- Segment casual against heavy players, since an average can hide two opposite effects.
- A longer window, to see whether the effect fades or compounds by day 30 or 90.
- Revenue alongside retention, which this dataset cannot show.
- A formal power analysis, stating the smallest effect this design could reliably detect.
