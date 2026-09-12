# PM Loop Pack — shared report design system

> The one visual language every loop's presentation layer uses, so all 12
> outputs read as one product: a PM's operating surface, not twelve
> unrelated documents. This file is the source of truth for look and feel.
> A loop's SKILL.md references it; it never redefines colors, type, or
> components locally.

## What the presentation layer is (and is not)

Every loop already produces an **audited markdown draft** — that stays the
source of truth, and the gate/checker apply to it in full. The presentation
layer is a **self-contained HTML report generated from the already-passed
draft**, never authored independently of it. Rules:

- Build it only after the checker returns PASS. Never render an unpassed or
  flagged draft as a polished report; a FAIL never ships a pretty page.
- Every number, flag, name, and citation in the HTML traces back to the
  passed markdown draft verbatim. The HTML adds layout and visual encoding,
  never a new figure, claim, adjective, or reordering that changes meaning.
- If the draft says UNAVAILABLE, the report shows an explicit unavailable
  state (see components) — never a blank, a zero, or an omission.
- One HTML file, fully self-contained (inline CSS, inline SVG for any
  chart, no external fonts/scripts/images). It must open offline and be
  publishable as an Artifact.
- The report is a presentation of the draft, so it carries the same
  no-em-dash and no-unsupported-adjective bars the draft does.

## Design plan

**Subject.** A PM's weekly operating surface — scanned and operated, not
read top to bottom. So this is information design first: summary before
detail, state encoded in form (chip, stripe, meter) as well as number.

**Color — chosen slate neutrals, one confident accent, semantic set kept
separate from the accent.**

```
--ink:      #16181d;   /* near-black text, slight blue bias         */
--paper:    #f7f8fa;   /* page ground, cool off-white               */
--surface:  #ffffff;   /* card ground                               */
--line:     #e4e7ec;   /* hairline borders, grid lines              */
--muted:    #5b6472;   /* secondary text, labels                    */
--accent:   #3b4ce2;   /* single brand accent: indigo               */
--accent-2: #eef0fe;   /* accent wash for fills, active states       */
/* semantic — status only, NEVER used as the accent */
--good:     #1a7f5a;   /* on-track, healthy, passed                 */
--warn:     #b3701a;   /* at-risk, watch, degrading                 */
--crit:     #c0392b;   /* off-track, breach, blocker                */
```

Dark theme (redefine the same tokens, do not invert naively):

```
--ink:#eef0f4; --paper:#0f1115; --surface:#171a21; --line:#282d38;
--muted:#9aa4b2; --accent:#8b96ff; --accent-2:#1c2140;
--good:#4ecb93; --warn:#e0a355; --crit:#f0736a;
```

Wire both `@media (prefers-color-scheme: dark)` AND
`:root[data-theme="dark"]` / `:root[data-theme="light"]` at the token
level so the viewer's toggle wins in both directions.

**Type — inline every face as a @font-face data URI (CSP blocks CDNs); if
a face can't be embedded, fall back to the system stacks below, never to a
silent default.**

- Display / headings: a confident grotesk or humanist sans, tight leading,
  `text-wrap: balance`. Fallback: `"Inter", system-ui, sans-serif` is fine
  only as fallback, not the intended identity — reach for something with
  more character (e.g. a face like Space Grotesk / Söhne / General Sans) as
  the embedded display face.
- Body: a readable sans at ~15–16px, running measure near 65ch.
- Data / mono: a monospace with `font-variant-numeric: tabular-nums` for
  every column of digits, deltas, and IDs.

One type scale, used everywhere: 32 / 24 / 19 / 16 / 14 / 12.5. Uppercase
eyebrow labels get ~0.08em letter-spacing.

**Layout.** Max content width ~in the 1080–1200px band, centered, generous
gutters. Lay out with grid/flex + `gap`, never per-element margins. Any
wide table/chart lives in its own `overflow-x:auto` container so the body
never scrolls sideways. Give focusable elements a visible focus ring and
respect `prefers-reduced-motion`.

## Component kit (use these, don't reinvent per loop)

- **Report header** — eyebrow with loop name + run date/period, an H1
  title, and a one-line run meta strip (source(s), checker verdict badge:
  green PASS). Keep it a header, not a giant hero.
- **Bottom line / TL;DR banner** — the draft's lead call, set larger, at
  the very top of the body. One block, the single most important figure
  bolded.
- **Stat tiles** — a responsive row of KPI cards: big tabular number, an
  uppercase label, and a delta line colored by direction (good/warn/crit),
  with an arrow glyph. A tile whose source is UNAVAILABLE shows a muted
  "UNAVAILABLE" state naming the source, never a fake number.
- **Delta / trend** — deltas always show sign and are colored semantically
  (improvement = good even when the number falls, e.g. churn down). Where a
  series exists, draw a small inline SVG sparkline with a faint grid, an
  area fill in `--accent-2`, and an emphasized endpoint dot.
- **Flag / severity chip** — a pill in the semantic color: `● BREACH`,
  `▲ AT-RISK`, `✓ ON-TRACK`. Rows or cards that carry a flag also get a
  left severity stripe in the same hue.
- **Data table** — hairline `--line` borders, zebra-free, tabular-nums,
  right-aligned numeric columns, sticky header if long. This is the audited
  table; it appears in full, every listed row present.
- **Owner + next-step line** — every flagged item renders its owner name
  and the one concrete next step from the draft, inline under the flag.
- **Watch items / carried-forward** — each with its week/run count as a
  small counter chip.
- **Provenance footer** — source files, run timestamp, checker PASS, and
  "Generated from the audited draft; every figure traces to source." No
  invented figures live below this line either.

## Anti-patterns (this is internal PM tooling, keep it sharp)

- No purple→blue gradient hero, no giant centered splash, no emoji as
  section markers, no `rounded-lg`-on-everything card soup.
- No decorative number badges (01/02/03) unless the content is a real
  ordered sequence.
- Color means status. Don't tint things for decoration; a chip's color is
  a claim about state and must match the draft's flag.
- Density over drama: this beats a status page by being scannable, not by
  being loud. Spend boldness in one place (the bottom line), keep the rest
  quiet.
