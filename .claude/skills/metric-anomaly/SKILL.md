name: metric-anomaly
description: Runs daily. Checks key metrics against thresholds,
flags anything that moved, drafts a first-cause hypothesis that
names the most recent change as candidate.
---
## Metrics watched

Daily exports live at data/metric-anomaly/metrics-[YYYY-MM-DD].csv
(relative to the repo root). Columns: metric,value,unit.

- signups (count/day)
- activation_rate (pct)
- checkout_conversion (pct)
- api_error_rate (pct)
- dau (count)
- p95_latency (ms)

Recent-changes log (deploys, campaigns, pricing):
data/metric-anomaly/changes.md

## Thresholds (flag if crossed)

- Any metric: moves more than 10% vs its 7-day rolling average
  (the 7 days immediately preceding the day being evaluated).
- activation_rate (the metric we care most about): moves more
  than 5% vs its 7-day rolling average.
- A metric under its threshold is NEVER flagged, no matter how
  suggestive. It may go on a short "Watch (not flagged)" list with
  its computed delta, but the flag count must not include it.

## State file (this loop is NOT stateless)

STATE.md lives in this skill folder and ALWAYS exists. Read it
before computing anything. The output must never claim there is no
state file or no prior flags without quoting STATE.md to prove it —
"no state file in this loop" is an automatic fail.

State rules, in order:

1. Quote every open flag from STATE.md (metric, opened date, day
   count, baseline-exclusion rule) at the top of the output, before
   any table.
2. Baseline exclusion: every day covered by an open flag is removed
   from that metric's 7-day rolling-average window. The excluded-day
   ("clean") average is THE baseline — the only number allowed in
   the table, the Signal line, and any headline. A with-contamination
   figure may appear only as a clearly labeled aside, never as the
   primary number.
3. Continuation, not news: a crossing on a metric with an open flag
   is a CONTINUATION. Write it under a heading like
   "## Flag (continued, day N): metric" with an explicit day count
   carried from STATE.md (state day count + 1), status "OPEN, day N,
   not yet sustained" until day 3.
4. Sustained at 3: a metric flagged 3 consecutive days is escalated
   as a sustained shift, not re-announced. Before day 3 it is
   explicitly "not yet sustained."
5. No silent drops: every open flag in STATE.md is carried forward,
   escalated, or closed with a stated reason — never omitted.
6. State advance on pass: after a passing run, append to STATE.md a
   dated run summary (what crossed, hypothesis, flag status with new
   day count, and the updated list of days excluded from future
   baselines — including today's flagged data day). A "pass" that
   leaves STATE.md untouched is not a pass.

## Hypothesis format

Signal: what moved, by how much (clean baseline only), over what
window, and — if continuing an open flag — "day N of open flag."
Recent changes: last deploy, last campaign, last pricing change.
Candidate cause: one sentence, or "no recent change found."
First step: one action to verify or rule out in the next hour —
time-bound, specific (what data, which breakdown), with the owner
to page and the fallback (e.g. rollback) named.

Every number cited must be recomputed from the raw CSVs, with the
exact baseline window (dates included, dates excluded and why)
stated next to it.

## Output format

Every draft opens, in this order, before any table or other detailed
section:

1. "## Plain-language summary": 3-5 sentences, no jargon (no bare
   metric-code names, no unexplained "rolling average"/"clean
   baseline"). States whether an anomaly was found today (naming it
   if so) and the single most important thing the reader should do
   next. If nothing crossed, say so plainly and name what to do
   instead. Written for a reader with zero context on this loop.
2. "## Bottom Line" block: 3-5 bullets, each one dense sentence: the
   single most important takeaway, why it matters, and a citation to
   specific evidence found later in the draft (a metric + delta, a
   STATE.md day count, a section heading). Write it last, after
   every number is computed, but place it here (right after the
   plain-language summary). No bullet may restate the header or read
   as generic filler ("things look mostly fine," "continue
   monitoring"); if a bullet would apply verbatim to any other day's
   run, rewrite it or cut it.

No em dashes anywhere in the draft, in any section, including the
plain-language summary. Use a period, comma, or colon instead. One
em dash anywhere in the draft is an automatic fail.

Formatting for the rest of the draft: real markdown headers for
every section, a table wherever content is naturally tabular (the
metrics-vs-threshold check, before/after baseline values, multi-day
flag status — these belong in a table, not prose), and bold on the
single most important figure or call per section (the flagged delta,
the day count, the candidate cause). No walls of prose — if a
paragraph runs past ~3 sentences, break it into a table or bullets.

Voice: high information density, no filler or throat-clearing ("it
is important to note," "as we can see"), every claim backed by a
specific citation, confident and precise — state the call, not a
hedge. Zero unsupported adjectives ("significant," "robust") — a
number, or nothing.

## Presentation layer

After the checker returns PASS, the maker generates a self-contained
HTML report FROM the passed markdown draft. The draft stays the
audited source of truth; the gate and checker apply to it in full.
Never render an unpassed or flagged draft as a polished report.

Follow .claude/skills/_shared/report-style.md for color, type,
layout, and components. Reference it; do not redefine the palette,
type scale, or component kit here.

Map this loop concretely:

- Bottom-line banner: the flagged metric and its breach magnitude
  (clean-baseline delta vs threshold), or an explicit all-clear
  state ("No flags today") if nothing crossed this run.
- Hero chart: an inline-SVG sparkline/area chart of the metric's
  series with the anomaly point emphasized (endpoint dot) and the
  expected band (threshold around the clean 7-day baseline) shaded.
- Stat tiles: current value, clean baseline, and threshold for the
  flagged metric, each with a direction-colored delta line.
- Severity chip + left stripe on the breach card (● BREACH,
  ▲ AT-RISK for a Watch item, ✓ ON-TRACK / all-clear), colored by
  the draft's flag, plus the "OPEN, day N" continuation count where
  the draft carries one.
- Audited table of contributing segments only if the passed draft
  lists them, every listed row present, no re-ranking.
- Owner + next-step line: the owner to page and the one time-bound
  first step, verbatim from the draft.
- Provenance footer: source CSVs, run date, checker PASS.

Every value, threshold, metric name, day count, and owner traces to
the passed draft verbatim. Invent no cause, add no figure, and do no
reordering that changes meaning. Where the draft says UNAVAILABLE,
show an explicit unavailable state, never a blank or a zero. One
self-contained file (inline CSS and SVG, no external assets). Same
no-em-dash bar as the draft: one em dash in the report is a fail.

## Known failure modes

(Write every mistake here the day it happens. This becomes the most
valuable part of the skill file.)
- 2026-05-19: signup spike from a bot wave crossed the threshold two
  days straight, then got absorbed into the 7-day average and masked
  a real dip the following week. Rule: days covered by an open flag
  are excluded from the rolling-average baseline until the flag is
  closed.
- 2026-07-16: a run declared the loop "stateless: no state file, no
  prior open flags" without checking; STATE.md existed and held an
  open flag. Rule: STATE.md always exists; read it first and quote
  its open flags verbatim. Any "no state" claim is an automatic fail.
- 2026-07-16: the contaminated 7-day average (spike day included) was
  reported as the headline baseline, with the clean figure demoted to
  a parenthetical. Rule: the flagged-days-excluded average is the
  only reportable baseline; the contaminated figure never leads.
- 2026-07-16: an open flag's second day was announced as a fresh
  anomaly with no day count. Rule: continuations carry an explicit
  "OPEN, day N, not yet sustained" line taken from STATE.md, never a
  new "Flag:" heading.
- 2026-07-16: the self-review passed checks "vacuously" on the false
  no-state premise and printed "checker: passed" without moving the
  draft or appending to STATE.md. Rule: every check must cite the
  evidence it verified (file read, numbers recomputed); vacuous
  passes are fails, and a pass without both on-pass side effects
  (file move + STATE.md append) is a gate violation.
- 2026-07-17: the draft read like a status log — flat bullet lists,
  no synthesis up top, key numbers buried mid-paragraph, hedged
  language ("seems to have," "may be related"). A VP had to read the
  whole thing to find the one number that mattered. Rule: every
  draft now opens with a "Bottom Line" synthesis block (3-5 dense,
  cited takeaways) before any detailed section, uses tables for
  comparisons, bolds the one figure that matters per section, and
  drops hedges and unsupported adjectives for stated calls backed by
  numbers.

## Checker criteria

Hypothesis cites specific recomputed data. "Something changed" is not
a hypothesis. The checker must itself open STATE.md and the raw CSVs:
a check justified by the draft's own claims (or by "no state file
exists") is invalid; each check must name the evidence checked. Open
flags in STATE.md are carried forward or closed, never silently
dropped; continuations carry the day count. A 3-day-running flag is
marked sustained, not repeated as news; under 3 days it is marked
"not yet sustained." Days covered by an open flag are excluded from
the baseline; any table, Signal line, or headline that leads with a
contaminated baseline fails even if a clean figure appears elsewhere.
No metric under its threshold is flagged. A pass verdict is valid
only if the draft is moved to the round root and the STATE.md run
summary is appended in the same run.

Plain-language summary: the draft must open with a "## Plain-language
summary" (3-5 sentences, no jargon) before the Bottom Line block,
"State carried in," or any table. It must state whether an anomaly
was found and the single most important action to take next, in
language a reader with no context on this loop could follow. Missing,
misplaced, jargon-heavy, or silent on the "what do I do" question is
a fail.

Em dashes: the draft must contain zero em dashes, anywhere, in any
section. Even one is a fail.

Bottom Line block: right after the plain-language summary, the draft
must open with a "## Bottom Line"
section before any other detailed section (before "State carried
in," before any table). It must have 3-5 bullets. Each bullet must
cite something concrete found later in the draft or the raw sources
— a metric name + delta, a STATE.md day count, a specific section
reference — not a restatement of the header. Reject any bullet that
is generic filler and could apply to any day's run ("things look
mostly fine," "continue monitoring," "no major issues") with no
number or reference attached. Missing block, wrong position, fewer
than 3 or more than 5 bullets, or any uncited/generic bullet is an
automatic fail.

Presentation layer (only when an HTML report is generated): build it
only after PASS. Every metric name, value, clean baseline, breach
magnitude, threshold, day count, and owner in the report must trace
to the passed draft verbatim, with nothing added, dropped, or
re-ranked (contributing-segment rows appear in full and in draft
order). The all-clear state and any UNAVAILABLE source must be shown
explicitly, never as a blank or a zero. The report must be one
self-contained file (inline CSS and SVG, no external assets) and
carry zero em dashes; even one is a fail.
