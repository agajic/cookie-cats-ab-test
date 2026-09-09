# DESIGN.md — case-study site (`site/`)

Documents the visual world as built. Written from the finished build, not before it.

**Surface:** `site/index.html`, a single long-form case study.
**Visitor mode:** Read — the visitor must understand an analysis; comprehension *is* the
persuasion. Structure serves reading first, expression second.
**Approach:** built directly in code rather than from a static mockup, with the ambition
carried by the first viewport and by one signature interaction.

## The world

A **match-statistics report**. An A/B test is a fixture between two versions: two named
sides, one metric, a decisive verdict. That grammar is native to a football-management
studio's audience, and it maps onto the mechanism exactly. Executed with instrument
precision, never broadcast cartoon.

Consequences that show up everywhere in the build:

- **Rules, not boxes.** Hairlines and generous space group content. Nothing is put in a card.
- **Numbers are the display element.** Set in Archivo at expanded width, tabular figures throughout.
- **One tonal inversion**, reserved for the bootstrap section, to pace the scroll and give the focal moment its own ground.

## Tokens

```
--paper      oklch(97.4% 0.005 250)   cool ground (deliberately not cream)
--paper-2    oklch(94.6% 0.009 250)   closing band
--ink        oklch(24%   0.032 262)   primary text
--ink-2      oklch(44%   0.030 262)   secondary text (AA on paper)
--ink-3      oklch(56%   0.022 262)   chart ticks, supplementary only
--rule       oklch(88%   0.012 258)   hairline
--rule-firm  oklch(74%   0.020 258)   structural rule

--cobalt      oklch(50% 0.170 256)    gate 30 / control
--cobalt-text oklch(44% 0.160 256)    links and cobalt text (AA)
--rust        oklch(56% 0.150 34)     gate 40 / variant
--rust-text   oklch(48% 0.145 34)

--d-ground   oklch(22%   0.035 262)   inverted section
--d-ink      oklch(95.5% 0.010 258)
--d-ink-2    oklch(78%   0.030 258)   tinted from the hue, never gray
--d-cobalt   oklch(72%   0.140 256)   bootstrap marks
```

**Colour strategy:** restrained. Neutrals carry the page; the two data hues are reserved for
the two sides of the experiment and never spent on decoration. Group identity is always
double-coded (colour *and* position *and* label), so colour is never the only channel.

## Type

One family: **Archivo variable**, self-hosted (latin + latin-ext; latin-ext is required for
`ć`). Width and weight axes carry the hierarchy, so no second family is needed.

| Role | Setting |
|---|---|
| Display (h1) | `wdth 112 / wght 700`, clamp 2.3–4.35rem, tracking −0.04em |
| Scoreline | `wdth 118 / wght 720`, clamp 2.6–4.9rem, tabular figures |
| Section head (h2) | `wdth 108 / wght 650`, max 20ch, balanced |
| Body | `wdth 100 / wght 400`, 1.0625rem, 1.62 leading, 36rem measure |
| Label / tick | `wdth 92–96 / wght 620–700`, uppercase, tracked |

On the inverted section, light-on-dark is compensated on all three axes: more leading,
slightly more tracking, one step more weight.

## Motion

**One authored focal moment:** the bootstrap. 1,000 resampled worlds arrive as individual
marks that stack into the distribution while the zero rule stands unbroken. The motion
explains the statistic rather than decorating it.

Everything else is quiet: a scroll-reveal for content below the fold and count-ups on the
headline figures. Easing is `cubic-bezier(0.16, 1, 0.3, 1)` (exponential ease-out, never
bounce). Content is visible by default, so a failed script cannot hide the page.
`prefers-reduced-motion` draws every final state immediately, including the settled
distribution.

## Charts

All charts are inline SVG drawn at runtime from `site/data.js`, which
`site/generate_data.py` regenerates from the dataset. No figure is hand-typed, and the
generator reproduces the shipped file byte-for-byte.

Honesty rules applied: retention comparisons are **dot plots with 95% intervals**, not bars,
because the interesting range does not include zero and a truncated bar axis would mislead.
The AUC chart starts at 0.5 and says so, because 0.5 is chance, not zero.

## Browser surfaces

Text selection, focus rings, caret and scrollbar are themed from the palette rather than
left at browser defaults.

## Known lint warnings

A static CSS scan reports five warnings. Each was checked against the rendered page and
judged a false positive rather than worked around:

- **Four on the verdict and stat dividers.** The scanner flattens `@media` blocks, so it
  applies the narrow-viewport `padding-left:0` unconditionally. Confirmed by flipping which
  side the mobile override zeroes, since the warning moved with it. At every real viewport
  the padding is 1.6rem.
- **One on display type**, where leading below 1.3 is the intended setting.
