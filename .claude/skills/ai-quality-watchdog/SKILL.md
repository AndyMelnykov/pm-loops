name: ai-quality-watchdog
description: Runs nightly. Scores the eval set against the live
feature, compares pass rate to the 7-day average, alerts on drops
with the failing examples attached.
---
## Sources
- Eval set: data/ai-quality-watchdog/eval-set.json (30 real anonymized
  inputs, each with pass criteria: what a correct output must contain,
  must not contain, or must match)
- Tonight's live-feature outputs: data/ai-quality-watchdog/tonight-outputs.json
  (captured by the 2am harness; treat as the live feature's responses)
- History: data/ai-quality-watchdog/history.csv

## Threshold
Pass rate drops more than 5 points below the 7-day rolling
average.

## Escalation rule
Any example failing 3+ consecutive nights gets its own line in
the alert.

## State file
Read STATE.md in this skill folder
(.claude/skills/ai-quality-watchdog/STATE.md) before starting — it
always exists; if a read fails, list the folder and flag the run
rather than asserting it is absent. It holds the last run summary,
the pattern log of open flags, and lessons learned. After a passing
run the state MUST advance: append date, pass rate, which examples
failed and why, and EVERY flag that cleared (any example that failed
last night or holds an open pattern-log flag and passed tonight —
enumerate them all, not just one). In eval rounds, write the append
to a round copy (copy STATE.md to the round folder and append there);
never edit the fixture. A passing run with no state append is an
incomplete run. An example failing 3+ consecutive nights per STATE.md
gets escalated in the alert as a confirmed regression, not a new
failure. "New failure" means: no failure recorded for that example in
STATE.md's pattern log or in the last 7 nights of history.csv.
Intermittent counts (e.g., "failed 4 of last 7 nights") come from the
pattern log and must be cited in the alert — they are a stronger
signal than a raw streak count.

## Output quality rules
- Never use an em dash (—) anywhere in the report, alert, or state
  append. Use a period or comma instead.
- Every nightly report opens with a **Plain-Language Summary** section,
  above and separate from the Bottom Line block: 3-5 sentences, no
  jargon (no "pass rate," "regression," "pattern log," example IDs, or
  percentages beyond one plain number), stating the overall
  AI-quality verdict and the single most important thing the reader
  should do next.

## Report format
Every nightly report (runs/ai-quality-watchdog/nightly-YYYY-MM-DD.md)
opens with a Plain-Language Summary (see Output quality rules above),
then a **Bottom Line** block — the first thing after the title,
before any other section, including before the alert groupings. 3-5
bullets. Each bullet is one dense sentence: the single most important
takeaway, why it matters, and a citation to the specific evidence in
the body below (an example ID, a STATE.md pattern-log count, an
unrounded number, a section heading). No bullet may restate the
header or be generic enough to fit any night's run ("things look
mostly fine," "continue monitoring," and equivalents are banned). A VP
reading only Bottom Line should have the whole picture in 15 seconds.

Below Bottom Line: real markdown headers for every section — no
unlabeled walls of prose. Use a table wherever the content is
naturally tabular: the failing-examples list under each alert heading
(columns: ID, reason, signal/streak), the cleared-tonight list,
before/after pass-rate comparisons. Bold the single most important
figure or call in each section (the pass rate, the delta, the
escalation verdict).

## Presentation layer

After the checker returns PASS, the maker generates a self-contained
HTML report FROM the passed markdown draft. The draft stays the
audited source of truth; the gate and checker apply to it in full.
Never render an unpassed or flagged draft as a polished report.

Follow .claude/skills/_shared/report-style.md for color, type,
layout, and components. Reference it; do not redefine the palette,
type scale, or component kit here.

Map this loop concretely:

- Bottom-line banner: the quality metric that breached and by how
  much (tonight's pass rate vs the 7-day rolling average, the point
  drop bolded), or an explicit all-clear state ("All metrics in-band,
  no regression") when nothing crossed threshold.
- Stat tiles: pass rate (with the 7-day baseline delta), refusal
  rate, and latency, each vs its threshold with a direction-colored
  delta line; where a series exists, an inline-SVG sparkline of the
  metric's recent nights with the current point emphasized.
- Severity chips + left stripe on each breach (● BREACH for a
  confirmed regression, ▲ AT-RISK for known-intermittent, ✓ ON-TRACK
  / all-clear), colored by the draft's flag, with the "failed N of
  last 7 nights" or consecutive-night count where the draft carries
  one.
- Failing-examples section: the sampled failing examples rendered as
  mono cards showing the input then the output (input -> output),
  quoted from the draft exactly, never paraphrased or invented.
- Audited table: metric -> value -> threshold -> flag -> owner ->
  next step, every listed row present, no re-ranking.
- Owner + next-step line: the owner or team to page (eval-set.json
  owner field) and the one concrete first-look action, verbatim from
  the draft.
- Provenance footer: source files, run date, checker PASS.

Every metric, value, threshold, example, name, and count traces to
the passed draft verbatim; sampled examples are quoted exactly, never
paraphrased or invented. Add no figure and do no reordering that
changes meaning. Where the draft says UNAVAILABLE, show an explicit
unavailable state, never a blank or a zero. One self-contained file
(inline CSS and SVG, no external assets). Same no-em-dash bar as the
draft: one em dash in the report is a fail.

## Alert rules
- Group failing examples under exactly these headings, in order:
  "Confirmed regression (3+ consecutive nights)", "New failures
  tonight" (only genuinely new per the definition above),
  "Ongoing / known-intermittent" (anything with prior failures in the
  pattern log or last-7-night history, with its STATE.md count
  quoted), "Cleared tonight" (exhaustive). Render each heading's list
  as a table per Report format above — no bare bullet lists.
- Every "suggested first look" action names an owner or team — use
  the owner field in eval-set.json when no better owner is known.
- Link only paths a #product reader can open: the nightly report
  (runs/ai-quality-watchdog/nightly-YYYY-MM-DD.md), never harness/eval output
  paths.
- Numbers: recompute pass rate and the 7-day average from raw data,
  state the unrounded value once, then use one consistent precision
  (one decimal). Compute deltas from unrounded values before
  rounding.

## Known failure modes
(Write every mistake here the day it happens. This becomes the
most valuable part of the skill file.)
- 2026-07-02: Live feature timed out on 4 examples and they were
  scored FAIL. Timeouts are "no result," not failures — retry
  once, then flag the run as incomplete.
- 2026-07-10: Partial credit is not a thing. If criteria say
  AES-256 and the answer says "industry-standard encryption,"
  that is a FAIL.
- 2026-07-16: Checker marked "counts match STATE.md's pattern log" ✓
  while claiming STATE.md was absent. It exists at
  .claude/skills/ai-quality-watchdog/STATE.md. Never mark a check ✓
  that was not actually performed; never claim a file is absent
  without listing its directory. Each pattern-log check must quote
  the STATE.md line it verified against.
- 2026-07-16: Run passed but no state append was written anywhere.
  The state advance is part of the pass action, not optional — the
  next night's run loses tonight's streak data without it.
- 2026-07-16: Alert filed an intermittent example (failed 4 of last
  7 nights per STATE.md) and a known flake under "New failures
  tonight," contradicting its own bullet text. Prior failures never
  go under "New" — use the Ongoing / known-intermittent heading and
  quote the pattern-log count.
- 2026-07-16: Cleared flags reported selectively (one cleared example
  named, another omitted). Cross-check every failed_id from last
  night and every open flag against tonight's passes; list all that
  cleared.
- 2026-07-16: Alert linked an internal eval-harness path and named no
  owner. Link the nightly report path and name an owner (eval-set.json
  owner field) for each suggested action.
- 2026-07-17: Reports read like a scored spreadsheet — 30 lines of
  PASS/FAIL with no synthesis, forcing a VP to read the whole thing to
  find the one regression that mattered, and prose paragraphs where a
  table belonged. Reports now open with a mandatory Bottom Line block
  (3-5 bullets, each citing a specific example ID, pattern-log count,
  or number from the body) and use tables/bold throughout. A report
  missing Bottom Line, or with a generic/uncited bullet in it, is not
  a pass — same bar as a missing state append.

## Checker criteria
No em dash (—) appears anywhere in the draft (report, alert, or
proposed state append); flag and reject if one is found. The report
opens with a Plain-Language Summary (3-5 sentences, no jargon, states
the overall verdict and the single most important next action) before
the Bottom Line block. Every example ran. Every score has a one-line reason. STATE.md was
actually read and each consecutive-night or intermittent count in the
draft matches its pattern log, with the matching pattern-log line
quoted as evidence. Alert compares against the 7-day rolling average,
not last night alone, with numbers recomputed independently from raw
data. Alert grouping follows the Alert rules: nothing previously
failing sits under "New failures tonight"; intermittent items carry
their STATE.md counts; the cleared list is exhaustive; every
suggested action has a named owner; links point to the nightly report,
not harness paths. On pass, the state append exists in the round copy
of STATE.md. No check may be marked ✓ without the evidence in hand.

The report opens with a Bottom Line block — the first thing after the
header, before any other section — with 3-5 bullets. For each bullet,
find its cited evidence (example ID, pattern-log count, unrounded
number, section heading) in the body and confirm it actually appears
there; a bullet whose citation doesn't check out, or that merely
restates the header, is a fail. Reject the whole Bottom Line if any
bullet is generic enough to apply to any night's run ("things look
mostly fine," "continue monitoring," and equivalents). Confirm real
markdown headers exist for every section, tabular content (failing
examples, cleared flags) is rendered as a table rather than bare
bullets, and each section bolds its single most important figure or
call — flag any wall of unformatted prose.

Presentation layer (only when an HTML report is generated): build it
only after PASS. Every metric name, value, threshold, flag, pass-rate
delta, consecutive-night or intermittent count, owner, and next step
in the report must trace to the passed draft verbatim, with nothing
added, dropped, or re-ranked; sampled failing examples must be quoted
exactly as the draft has them, never paraphrased or invented. The
all-clear state and any UNAVAILABLE source must be shown explicitly,
never as a blank or a zero. The report must be one self-contained file
(inline CSS and SVG, no external assets) and carry zero em dashes;
even one is a fail.
