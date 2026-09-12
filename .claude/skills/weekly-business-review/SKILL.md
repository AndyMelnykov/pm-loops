name: weekly-business-review
description: Runs every Monday. Reads the weekly metrics export,
reports every metric on the fixed list with deltas vs last week
and vs the 4-week average, flags threshold breaches, drafts the
weekly business review.
---
## Bottom Line (mandatory, first section in every draft)

The first thing in the draft, before the metric list, before
anything else, before even the "## State carried in" section. 3-5
bullets. Each bullet is one dense sentence: the single most
important takeaway, why it matters this week, and a citation back
to the specific evidence in the body below (a metric's value from
the table, a flag and its owner, a callout, a North Star/OKR figure,
a Jira epic status — name the number or section). Written so a VP
gets the whole picture in 15 seconds without reading further. Never
a restatement of the header or a section title. Never vague
("things look mostly fine," "continue monitoring," "no major
changes") — every bullet must be falsifiable against a number or
fact that actually appears later in this exact draft. A bullet
generic enough to paste unchanged into any other week's review is
filler; rewrite it or cut it.

## Metric list (fixed — the loop never adds or drops a metric)

Definitions, sources, and owners: data/weekly-business-review/
metric-definitions.md (relative to the repo root). The warehouse
export is data/weekly-business-review/metrics-history.csv
(columns: week_start,metric,value,unit); NPS comes from the
vendor's separate file data/weekly-business-review/nps-export.csv.
(These are bundled fixtures — swap the paths for your real
analytics or warehouse MCP source when you adopt this loop.)

The nine metrics, exactly:

- new_trials (count)
- trial_to_paid_conversion (pct)
- weekly_active_accounts (count)
- ai_assist_adoption (pct)
- net_new_arr (usd_k)
- churned_arr (usd_k)
- support_ticket_volume (count)
- api_uptime (pct)
- nps (score)

The list is the contract. Every metric on it appears in every WBR,
as a number or as an explicit UNAVAILABLE flag. Nothing else
appears — a metric not on this list is never reported, however
interesting the export makes it look.

## Reporting rule

For every metric: current value, delta vs last week, delta vs the
4-week average (the 4 weeks immediately preceding the week under
review). Flag anything past its threshold. A metric whose source
is unreachable gets an "UNAVAILABLE" row naming the source and the
failure — never a silent omission, never a carried-forward value,
never an estimate.

## Thresholds (flag if crossed)

- Any metric: moves more than 10% vs last week, or more than 15%
  vs its 4-week average.
- trial_to_paid_conversion (the metric we care most about): moves
  more than 5% vs last week or vs its 4-week average.
- api_uptime: any week below 99.9%.
- A metric inside its thresholds is never flagged, no matter how
  suggestive the narrative.

## Writing style

Never use an em dash (—) anywhere in the draft, including headers,
table cells, and footnotes. Use a period, comma, colon, or
parentheses instead. This is a hard formatting rule, checked by the
checker like any other.

Voice: write like a VP of Product, not a status page. High
information density, no filler, no throat-clearing. Every claim
carries a specific citation. State the call rather than hedging it.
Zero unsupported adjectives ("significant," "robust," "healthy") —
a number sits next to the claim or the adjective is cut. MAKER.md's
voice bar has the full drafting standard.

## Delivery

After a PASS, ask the user whether they want this WBR delivered
automatically each week (e.g. posted to a Slack channel, emailed, or
another channel) instead of only landing as a markdown file under
runs/weekly-business-review/. Record their answer as a line in
STATE.md under "## Delivery preference" so future runs don't ask
again once it's set.

## North Star & OKR progress

Source: data/weekly-business-review/okrs.md (North Star metric,
target, and the current-quarter OKRs with their KRs). This section
never invents a target or KR — every number in it must match
okrs.md verbatim, and every progress figure must be computed only
from metrics already on the fixed list above (no new metrics are
introduced by this section).

Report: the North Star metric's current value (from the metric
table), its quarter-start baseline (okrs.md) and quarter-end target
(okrs.md), and % of the target range closed
(`(current - baseline) / (target - baseline)`). Then each OKR's KRs,
each tied explicitly to the metric on the fixed list that tracks it,
with current value vs target and on-track / at-risk / off-track
called only from the metric's own flag/threshold state — a KR whose
tracking metric is flagged this week is at-risk or off-track, never
called on-track without saying why the flag doesn't apply.

## Dev progress (Jira)

Source: data/weekly-business-review/jira-dev-progress.md. List every
epic tagged to a Q3 OKR: status, story points done/total, target
ship date, and the OKR/KR it's linked to (must match okrs.md's KR
labels exactly). Never editorialize a status beyond what the export
says (an epic marked "In progress" is never reported as "on track"
unless the export's notes say so). Include the sprint burndown table
and its stated pace-vs-velocity read verbatim from the source — do
not recompute a different velocity number than the export states.

## Output format

Order: Bottom Line first, then the "## State carried in" section,
then the callouts below, then the metric table, then everything
else. Nothing that belongs in the detailed body is ever promoted
above the Bottom Line, and the Bottom Line is never pushed below it.

Formatting bar: real markdown headers for every section (no bare
bold text standing in for a heading). A table wherever the content
is naturally tabular (comparisons, multi-attribute lists,
before/after values) — never a prose paragraph doing a table's job.
Bold the single most important figure or call in each section (one
bold span, not a wall of bolded text). No walls of prose: dense
bullets or a table beat a paragraph every time.

Headline: 2-4 narrative callouts, each citing the exact numbers it
rests on — a callout claim with no number from the source behind
it is a gate violation. A claim about a streak or trend duration
("Nth straight increase," "N weeks running") is a numeric claim
like any other: it is a gate violation unless verified by walking
every consecutive week in the raw export from the earliest
available row for that metric and citing the exact week range that
backs the count — a specific-sounding number is still a vibe if
nobody walked the series to get it. If the series wasn't walked,
state only the WoW and 4-week-avg deltas and drop the duration
claim.

Full metric table below (metric, current, Δ vs last week, Δ vs
4-week avg, flag). State each 4-week average's component values
once — in the table or a single footnote — never in a separate
section that re-lists values already shown elsewhere in the draft.

Unavailable metrics listed with source and reason.

Every flagged metric, new or continuing, names its owner (from
metric-definitions.md) and one concrete next step inline — a flag
that reports only a number with no name to act on it is incomplete.

Watch items from STATE.md carried forward with their week counts,
written as content directly under a single "## Watch items"
heading (one bullet or H3 per item) — no heading is ever
immediately followed by another heading with nothing between them.

North Star & OKR progress and Dev progress (Jira) sections come
after the metric table, per the sections above, so every number in
those two sections must trace back to okrs.md, jira-dev-progress.md,
or the metric table with no invented figures. See "## Presentation
layer" below for how the passed draft becomes the HTML report.

## Presentation layer

The markdown draft is the audited source of truth: the gate and
checker apply to it in full. The HTML report is generated FROM the
passed draft only, never authored independently, never built for a
flagged or unpassed draft. If the checker returns anything but PASS,
no report exists. It follows .claude/skills/_shared/report-style.md
for all color, type, layout, and components: never restate the
palette here.

Map WBR content onto the shared kit:

- Report header: loop name eyebrow, week covered, and a green PASS
  badge from the checker verdict.
- Bottom Line banner at the very top of the body, most important
  figure bolded.
- Stat-tile row for the nine fixed metrics: current value, WoW
  delta, 4-week-avg delta, flag color, with an inline sparkline per
  metric where the series exists. An UNAVAILABLE metric renders as
  an explicit unavailable tile naming its source, never a number,
  never a dropped tile.
- Full audited metric table below the tiles, every listed row
  present. Flagged metrics show owner and next step inline.
- North Star meter (baseline to target, current marked) and OKR
  progress bars, each KR colored by its tracking metric's real flag
  state this week.
- Jira epics and sprint burndown as a table, statuses verbatim.
- Watch items as counter chips with their week counts.
- Provenance footer: sources, run timestamp, checker PASS.

The report carries the same bars the draft does: no em dash anywhere,
and no figure that is not reproduced verbatim from the passed draft.

## State file

Read STATE.md in this skill folder before starting. It holds last
week's values, the watch list, and lessons learned. A metric
flagged 2+ consecutive weeks is a watch item: write it as a
continuing trend with an explicit week count (STATE.md's count
+ 1), not fresh news. After a passing run, the checker appends:
date, week covered, all values, flags raised, unavailable sources,
updated watch-item week counts.

## Known failure modes

(Write every mistake here the day it happens. This becomes the most
valuable part of the skill file.)
- 2026-06-22: the NPS vendor export was missing and the draft
  silently dropped the row; the review shipped eight metrics
  instead of nine and nobody noticed for two weeks. Rule: the
  table has exactly one row per listed metric — a missing source
  is an UNAVAILABLE row, never an absent one.
- 2026-07-06: a callout said trial conversion was "down roughly a
  fifth since early June" — a vibe, not a citation; the real
  numbers (18.4% → 14.8%) appeared nowhere in the sentence. Rule:
  every callout claim carries the exact source values (and the
  delta computed from them) inline.
- 2026-07-17: a callout claimed ai_assist_adoption was on "a fifth
  straight weekly increase" — sounds cited but the maker never
  walked the series; the real streak was 7+ consecutive increases
  (2026-06-01 through 07-13). Rule: any streak/duration claim must
  be verified by walking every consecutive week in the raw export
  from the earliest available row and citing the exact week range,
  or the claim is dropped — a specific-sounding count is still a
  vibe if it isn't reproduced.
- 2026-07-17: the draft had an empty "## Watch items" heading
  immediately followed by another heading, with no body text
  between them. Rule: no heading is ever immediately followed by
  another heading — write watch items as content directly under
  one "## Watch items" heading (bullets or one H3 per item), never
  as an empty parent header.
- 2026-07-17: a "Raw values used" prose block re-listed each
  metric's current and prior-week values that were already in the
  metric table above it — filler, against the writing-style "no
  filler" rule. Rule: state each 4-week window's component values
  once, in the table or one footnote per metric — never restate
  values already shown in the table.
- 2026-07-17: a FAIL flags file cited full evidence for each
  failing check but never told the maker what to change. Rule:
  every failing check in the flags file ends with one directive
  sentence naming the specific fix needed for resubmission — this
  is an instruction, not a caveat, and does not soften the fail
  verdict.
- 2026-07-17: checker PASS checks asserted numbers "reproduce
  exactly" without showing the recomputed figures, asking to be
  trusted on everything except the one check that failed. Rule:
  every checklist item, pass or fail, shows the actual recomputed
  figures or matched items inline — naming the source file checked
  is not evidence by itself.
- 2026-07-17: a brand-new flag (support_ticket_volume) reported the
  number and threshold breach but never named who owns it or what
  to do next. Rule: every flagged metric, new or continuing, names
  its owner from metric-definitions.md and one concrete next step
  inline.
- 2026-07-17: voice/format upgrade. Before, the draft read like a
  status report: accurate callouts buried in prose, no section led
  with the number that mattered, and "significant"/"robust" stood
  in for figures nobody cited; a VP had to read the whole document
  to find the one thing worth acting on. Now, every draft opens
  with a "## Bottom Line" (3-5 dense, cited bullets, first section
  after the header, before even "## State carried in"), every
  section leads with its most important figure or call in bold,
  tables replace prose wherever the content has multiple
  attributes, and no unsupported adjective survives without a
  number next to it. Rule: this is a permanent contract change, not
  a one-off polish pass, enforced by the checker like any other
  format rule.

## Checker criteria

Bottom Line is the first section in the draft, before "## State
carried in" and before the callouts, with 3-5 bullets, and every
bullet cites a number, flag, or section that actually appears later
in the same draft — a bullet generic enough to apply to any week
unchanged fails this check.

Every metric on the list covered exactly once — as a recomputed
number or an UNAVAILABLE flag — and no metric beyond the list.
Every value, weekly delta, and 4-week-average delta reproduces
from the raw export; the checker recomputes them itself and does
not trust the draft's arithmetic. Every narrative callout cites a
number present in the source (or a delta of two such numbers). No
metric inside its thresholds is flagged. Watch items match
STATE.md's week counts, incremented by one, and no watch item is
silently dropped. North Star progress math
(`(current - baseline) / (target - baseline)`) recomputes exactly
from okrs.md's baseline/target and the metric table's current value.
Every KR's on-track/at-risk/off-track call matches its tracking
metric's actual flag state this week. Every Jira epic's OKR/KR link
and status matches jira-dev-progress.md verbatim — no status
upgraded beyond what the export says.

Every streak or duration claim ("Nth straight...") is verified by
walking the full consecutive series in the raw export, not taken
on faith — an uncounted or undercounted streak fails this check
even if every other figure in the callout is correct. Every
flagged metric names its owner and a concrete next step. No
heading in the draft is immediately followed by another heading.
The checker's own report shows the actual recomputed figures or
matched items for every checklist item, pass or fail — naming the
file checked against is not evidence by itself. A fail lists, for
each failing check, one directive sentence on what the resubmission
must change.

The HTML report, if built, is generated only after a PASS. Every
metric value, WoW delta, 4-week-avg delta, flag, streak, OKR figure,
and Jira status in it reproduces from the passed draft verbatim,
with nothing added, dropped, or re-ranked. Every UNAVAILABLE metric
renders as an explicit unavailable tile naming its source, never a
fabricated number and never a missing tile. The file is
self-contained (inline CSS and SVG, no external assets) and honors
the no-em-dash bar.

A pass verdict is valid only if the draft is moved out of drafts/
and the run summary is appended to STATE.md in the same run.
