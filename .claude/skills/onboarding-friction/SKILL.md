name: onboarding-friction
description: Runs weekly. Checks drop-off at every onboarding step
against baseline, cross-references onboarding-tagged tickets,
flags the step that's degrading.
---
## Sources
- Funnel: data/onboarding-friction/funnel-[week].csv (step, entries,
  completions). Current weeks on disk: funnel-2026-06-29.csv,
  funnel-2026-07-06.csv.
- Baselines: data/onboarding-friction/baseline-8week.csv (8-week
  rolling drop-off baseline per step)
- Support: data/onboarding-friction/support-onboarding-[week].csv
  (support-onboarding-2026-06-29.csv, support-onboarding-2026-07-06.csv)
- Qualitative: data/onboarding-friction/session-notes.md

## Run date
The run date is TODAY'S ACTUAL DATE from the environment (system
date / context). Never self-declare or back-date a run. The report
header, the draft filename, and all staleness arithmetic use this
date. Wrong run date = failed run.

## Freshness gate
Check each source's own dated header/"last updated" line. Staleness =
(today's actual date) minus (source's dated header), computed
explicitly — show the subtraction (e.g., "2026-06-03 → 43 days old as
of 2026-07-16"). Any source older than 30 days is stale: do not use it
as current-state evidence — flag it as stale in the output instead.

## Counting and arithmetic rules (mandatory)
- Ticket counts come from counting DATA ROWS ONLY: exclude `#` comment
  lines and the column-header row. Verify with a command (e.g.,
  `grep -vc '^#' file.csv` minus 1 for the header) before writing any
  count. Never eyeball a count.
- Every subcount (tag intersections like connect-data + confusing-setup)
  is recomputed from the raw rows with a command (e.g.,
  `grep 'connect-data' file.csv | grep -c 'confusing-setup'`), never
  estimated from memory of the rows.
- Ratios use the recomputed counts and are stated to 2 decimals
  (e.g., 27/12 = 2.25x), not rounded to 1 decimal.
- ROUND ONCE, at final write, never twice. Compute every percentage at
  full precision (4+ decimals) from the raw numerator/denominator, then
  round directly to 2 decimals: 686/3572 = 19.2049% → 19.20%. Never
  round an intermediate value and round again (19.2049 → 19.205 →
  19.21 is WRONG). Deltas are subtracted at full precision, then
  rounded once: 19.2049 − 14.5 = 4.7049 → +4.70 (NOT round-then-
  subtract-then-round). Verify each displayed percentage/delta with a
  command (e.g., `python3 -c 'print(686/3572*100)'`) immediately
  before writing it.
- Every headline number must be identical at every occurrence (flag
  title, body lines, notes, STATE.md append). Grep the draft for each
  headline value and confirm no variant spelling of it exists.
- Raw source files are the ONLY authority for counts. If any prose
  summary, README, fixture description, or other document contradicts
  a command-recomputed count from the raw rows, keep the recomputed
  number, and add a one-line note that the prose is inconsistent with
  the raw file (for the data owner to fix). Never edit a
  command-verified count to match prose.
- Every number in the report must be reproducible from a named source
  file. If a number cannot be recomputed, it does not go in the report.
- When a raw recount contradicts any prose summary, the mandatory
  one-line discrepancy note goes IN the report's Notes section (e.g.,
  "Note for data owner: [doc] states 15/13; raw CSV recount gives
  18/14 — raw file is authoritative"). Keeping the raw numbers without
  printing this note is itself a failure.

## Citation provenance rules (mandatory)
- Before writing any "noted in X" / "per X" / "logged in X" phrase,
  grep the cited file and confirm it actually contains that claim. A
  citation to content the cited file does not contain is fabrication
  and fails the run — even when the fact itself is true.
- Cite the exact STATE.md section. The pattern log and the "Last run"
  entries are distinct: prior-week numbers and watch-item upticks live
  in a "Last run" entry; structural baselines live in the pattern log.
  "Noted in the pattern log" when the fact sits in a Last-run entry is
  a false citation.
- A fact whose only source is a stale (>30-day) file may appear ONLY
  as disclosed historical context naming that file (e.g., "per
  session-notes.md's header — stale, historical context"). Never
  re-attribute a stale-source fact to STATE.md or any fresh source;
  laundering a stale fact through a fresh attribution defeats the
  freshness gate and fails the run.
- Likely-cause lines cite current-run evidence directly (ticket_ids,
  fresh-source rows). A release date or ship window with no fresh
  source is optional context, properly attributed per the rule above,
  or dropped.

## Trend-language rule (mandatory)
Words implying a trend shape — "accelerating", "decelerating",
"compounding", "trend" — require 3+ consecutive data points. With only
two points, write magnitude-plus-direction language instead (e.g.,
"worsened sharply week-over-week, consistent with the watch-item
escalation"). Two points never establish acceleration.

## Thresholds (flag if crossed)
- Any step's drop-off rises more than 3 points above its 8-week
  baseline
- Onboarding ticket volume rises more than 2x the 4-week average
  (the 4-week average is stated in the support CSV headers)

## Output format rules (mandatory)
- Never use an em dash (—) anywhere in the output. Use periods or
  commas (or "to"/"vs"/parentheses) instead. Grep the draft for the
  em-dash character before finishing and rewrite any hit.
- Open the report with a "Plain-language summary" section (3-5
  sentences, no jargon, no unexplained acronyms) stating the single
  biggest friction point found this run and the one most important
  next action, BEFORE the header and BEFORE the Bottom Line / detailed
  breakdown. If nothing crossed threshold, say so plainly and name the
  closest watch item instead. This is a distinct, plain-English opener
  for a non-specialist reader; it does not replace the Bottom Line
  block specified under Output format below (the dense, citation-backed
  opener for the VP skim, placed right after the header). Both
  sections are mandatory and serve different readers — write both.

## Output format
Header: "week of [data week] (run [today's actual date])".

### Bottom Line (mandatory — first section after the header, before any per-flag detail)
3-5 bullets. Each bullet is ONE dense sentence that fuses three things:
the single most important takeaway, why it matters, and a citation to
the specific evidence in the body below or a source file (a step name
+ its delta, a ticket_id, a source-health age, a STATE.md
consecutive-week count, a recomputed ratio). A VP reads these bullets
in 15 seconds and has the whole run — the detailed sections below are
substantiation, not new information. Banned: restating the header,
generic filler ("things look mostly fine", "continue monitoring"), or
any bullet that would be equally true of any other week's run — if a
bullet could be copy-pasted into next week's report unchanged, rewrite
it. When there are no flags, the Bottom Line still leads with the
strongest specific fact the run turned up (nearest-miss step and its
margin to threshold, a source that just crossed 30 days stale, a watch
item that resolved) — never a bare "no flags this week" with nothing
under it.

### Formatting requirements (mandatory)
- Real markdown headers (`##`/`###`) for every named section: Bottom
  Line, each flag, Source health, Notes. Bold text is not a substitute
  for a header.
- Render the per-flag summary as a markdown table whenever 2+
  flags/metrics exist (columns: step/metric, now, baseline/average,
  delta, continuity) — comparisons and multi-attribute lists belong in
  a table, not prose. Render source health as a table (source, dated
  header, age, fresh/stale) rather than a run of paragraph lines.
- Bold the single most important figure or call in each section (the
  headline delta in a flag, the acting owner in its Next action, the
  stale source in source health). One bolded item per section — bold
  is a signal, not decoration.
- No walls of prose: restructure any paragraph running past ~3
  sentences into a table or bullet list.

Per flag, in order:
1. Step (or metric), drop-off now vs baseline (or count vs average),
   with the delta.
2. Continuity line sourced from STATE.md: new flag / escalated from
   watch item / Nth consecutive flagged week / sustained (3+ weeks).
   Never write "sustained" before 3 consecutive flagged weeks; never
   write "new" for a step STATE.md already tracks as a watch item —
   write "escalated from watch item, 1st consecutive flagged week".
3. Related ticket count (recomputed per the counting rules).
4. 2 verbatim ticket quotes if any exist, cited by ticket_id.
5. Likely cause: one line naming the most probable trigger, citing
   the evidence directly per the citation provenance rules — ticket
   quotes/ids first; any release or ship-date claim attributed to the
   file that actually contains it (grep-verified), never to STATE.md
   unless STATE.md literally says it.
6. Next action: one line with a concrete next-hour action, the ACTING
   owner (who performs it this hour), and — if routing — the receiving
   team (e.g., "On-call PM routes to the connect-wizard eng team this
   hour; prioritize surfacing the silent test-connection failure").
   "Route to team X" without who does the routing is incomplete.
Also include: a source-health section and a notes section for
near-threshold or structural steps. EVERY source-health line — all
sources, fresh or stale — uses the same explicit form:
"[source date] → [RUN-DATE] minus [source date] = N days old". Never
abbreviate any line to just "→ N days old"; the full subtraction
appears on every line. When citing a
structural baseline, the citation is STATE.md's pattern log (the
authoritative current source), NOT stale session notes — stale notes
may be mentioned only as historical context, never as the basis.
Do NOT include any checker section, self-review, or "checker: passed"
line in the maker's output. The checker is a separate pass with its
own artifacts.

## Presentation layer
After the checker returns PASS, the maker generates a self-contained
HTML report FROM the passed markdown draft. The draft stays the audited
source of truth; the gate and checker apply to it in full. Never render
an unpassed or flagged draft.
- Follow .claude/skills/_shared/report-style.md for color, type,
  layout, and components. Reference it; never redefine the palette or
  type scale locally.
- Hero is a funnel/step visualization: an inline SVG with one bar per
  activation-funnel step (entries into completions), the drop-off
  between consecutive steps drawn between the bars, and the breached
  step emphasized in --crit. Label each bar with its step name and
  conversion. If no step breached, no bar carries crit color.
- Bottom-line banner states the worst drop-off step this run and its
  magnitude (delta vs the 8-week baseline), the single figure bolded.
- Stat tiles for key step conversions vs baseline, delta colored by
  direction (a rising drop-off is --crit); a tile whose source is
  UNAVAILABLE shows the explicit unavailable state naming the source.
- Severity chips on breached steps (● BREACH), a left severity stripe
  in the same hue on each breached row.
- Audited table, every row from the draft present: step, conversion
  now, delta vs baseline, flag, owner, next step.
- Provenance footer: source files, run date, checker PASS.
- If nothing breached threshold, show an explicit all-clear state (no
  breach this week) and surface the nearest-miss step, never a blank.
- Every rate, step name, delta, ticket_id, and owner traces to the
  passed draft verbatim. Add no cause, adjective, or reordering that
  changes meaning. UNAVAILABLE is explicit, never a blank or zero.
- One self-contained HTML file (inline CSS, inline SVG, no external
  fonts/scripts/images). Same no-em-dash bar as the draft: grep the
  HTML for the em-dash character before finishing.

## State file (mandatory)
Read .claude/skills/onboarding-friction/STATE.md (this skill folder,
absolute path from repo root) BEFORE starting. It exists and it is the
single source of truth for: last-run numbers, watch items, consecutive
flagged-week counts, structural baselines (pattern log), and lessons
learned. If you cannot read it at that path, the run FAILS — stop and
report the missing state file; never proceed with a "no state file"
framing and never claim it doesn't exist without listing the directory
first.
Continuity rules:
- A pattern-log watch item that crosses threshold this week is
  reported as "escalated from watch item → 1st consecutive flagged
  week", not as an unanchored new flag.
- A step flagged 3 consecutive weeks is escalated as a sustained
  degradation, not a fresh flag.
- Steps STATE.md documents as structurally high (known baseline) are
  NOT news — do not re-flag them unless they cross threshold vs their
  own documented baseline, and attribute that rule to the pattern log.
After a passing run, the checker MUST append a new "Last run" entry to
STATE.md containing: run date, steps flagged with consecutive-week
counts, numbers vs baseline (deltas and ticket count vs 4-week avg),
and source health (including which sources are stale and their ages).
A run is not complete until this append exists; "checker: passed"
without the append is a failed run.
Append format: add ONE new dated bullet ("- [RUN-DATE] (data week
...): ...") under the existing "## Last run" section header. NEVER
create an additional "## Last run" header — STATE.md keeps exactly one
Last-run section with dated bullets, or it fragments over weeks.
Pattern-log updates (consecutive-week counters, new watch items) edit
or extend the existing pattern-log bullets in place.

## Artifact flow (mandatory)
- Maker writes ONLY to runs/onboarding-friction/drafts/[RUN-DATE].md. Nothing
  else in the round directory.
- Checker on PASS: move the draft to the round root, THEN append to
  STATE.md. Both, in that order — a promoted output without the
  STATE.md append, or an append without the promotion, is a failed run.
- Checker on FAIL: write the failing checks to
  runs/onboarding-friction/flags/[RUN-DATE].md — that exact path is the ONLY fail
  artifact; never a second copy anywhere else (no checker-flags.md, no
  duplicates). The draft STAYS in drafts/. Nothing is written to the
  round root and no STATE.md append happens. A checker FAIL means NO
  output file may exist at the round root for that date — promoting a
  failed draft (or leaving a byte-identical copy at the round root) is
  itself a failed run.
- After a FAIL: the maker fixes every failure listed in
  flags/[RUN-DATE].md in the draft, then the checker re-runs from
  scratch. Only a clean re-check promotes the draft and appends state.
  The loop is not done until the round root holds a checker-passed
  output AND STATE.md holds the matching "Last run" entry.
- The promoted [RUN-DATE].md is the ONLY report file the loop ever
  places at the round root. Never write a second copy under any other
  name (no output.md, no report.md) — a byte-identical duplicate at
  the round root is a failed completeness check. If a harness needs a
  differently-named copy, the harness makes it; the loop does not.
- Final completeness check (checker, after pass): confirm exactly one
  report file — [RUN-DATE].md — exists at the round root, drafts/ no
  longer holds an unpromoted copy of the final text (remove drafts/ if
  it is left empty), exactly zero or one flags file from earlier fails
  remains (never duplicates), and `tail` of STATE.md shows the new
  dated bullet under the single existing "## Last run" header (no
  second "## Last run" header was created).

## Known failure modes
(Write every mistake here the day it happens. This becomes the most
valuable part of the skill file.)
- 2026-04-14: Funnel export renamed "Step 5: Invite" to "Invite team."
  Baseline lookup missed it and the step vanished from the report.
  Match steps by position AND fuzzy name for 2 weeks after any rename.
- 2026-07-16: Run falsely claimed "No STATE.md exists" when
  .claude/skills/onboarding-friction/STATE.md was present, losing the
  watch-item escalation and pattern-log context. Rule: STATE.md is
  mandatory; list the skill directory before ever claiming a file is
  missing; a missing state file fails the run, it never downgrades it.
- 2026-07-16: Ticket count included the column-header/comment lines
  (reported 28; file had 27 data rows), which propagated into the
  ratio (2.3x instead of 2.25x) and a "18 of 28" subclaim. Rule:
  count data rows with a command, exclude comments and header, restate
  the ratio from the recomputed count.
- 2026-07-16: Tag intersection off by one (reported 13 connect-data +
  confusing-setup; raw grep shows 14). Rule: recompute every subcount
  with a command against the raw CSV.
- 2026-07-16: Staleness computed from a self-declared run date
  (claimed 40 days; actually 43 as of the real run date). Rule: run
  date comes from the environment's actual today; show the date
  subtraction in the source-health line.
- 2026-07-16: Structural invite-team baseline attributed to stale
  session notes instead of STATE.md's pattern log. Rule: pattern log
  is the authoritative citation for structural baselines; stale notes
  are historical context only.
- 2026-07-16: Maker embedded a "Checker self-review" in its own output
  and passed itself on a false premise; no drafts/ or flags/ artifacts
  existed. Rule: maker writes drafts/, checker is a separate pass that
  moves the draft on pass or writes flags/ on fail; a checker that
  cannot verify required state FAILS the run, never rationalizes it.
- 2026-07-16: Passing run never appended to STATE.md. Rule: the
  checker's pass action includes the STATE.md append; no append = no
  pass.
- 2026-07-16: Flags stopped at diagnosis with no owner or next step.
  Rule: every flag ends with a Likely cause line and a Next action
  line naming an owner.
- 2026-07-16 (later run): Headline percentage double-rounded —
  686/3572 = 19.2049% was written as 19.21% (via 19.205), and the
  delta as +4.71 instead of +4.70, in the flag title AND body. Rule:
  round ONCE from the full-precision value (19.2049 → 19.20); deltas
  subtract at full precision then round once (4.7049 → +4.70); verify
  every displayed percentage/delta with a command before writing, and
  grep the draft to confirm the same value at every occurrence.
- 2026-07-16 (later run): A draft the checker FAILED was promoted to
  the round root anyway — output was byte-identical to the failed
  draft. Rule: on FAIL the draft stays in drafts/ and nothing goes to
  the round root; fix the listed failures, re-run the checker, and
  promote only on a clean pass.
- 2026-07-16 (later run): Run ended with no "Last run" append to
  STATE.md, so the escalation (watch item → 1st consecutive flagged
  week) and deltas were unrecorded and the next week's consecutive
  counts were uncomputable. Rule: the pass is promote + append,
  atomically; verify the append with `tail` on STATE.md before
  declaring the run complete.
- 2026-07-16 (later run): Checker wrote its fail record twice —
  flags/[RUN-DATE].md plus a stray duplicate in the round root. Rule:
  flags/[RUN-DATE].md is the single fail artifact; never write a
  second copy.
- 2026-07-16 (later run): A prose summary elsewhere in the repo gave
  tag subcounts (15/13) contradicting the raw CSV (grep-verified
  18/14); the raw-verified numbers were correct. Rule: raw rows are
  the only authority — never "correct" a command-verified count to
  match prose; note the prose discrepancy for the data owner instead.
- 2026-07-16 (later run): Some source-health lines showed only
  "→ N days old" while others showed the full date subtraction. Rule:
  every source-health line, fresh or stale, shows the explicit
  "[RUN-DATE] minus [source date] = N days old" subtraction.
- 2026-07-16 (latest run): Fabricated citation — a likely-cause line
  claimed the connect-wizard ship date was "noted in STATE.md's
  pattern log alongside the first uptick." STATE.md's pattern log
  contained neither: the ship date's only source was stale
  session-notes.md's header NOTE, and the first uptick lived in
  STATE.md's "Last run" entry, not the pattern log. The checker passed
  it anyway. Rule: grep-verify every "noted in X" citation against the
  cited file before writing; name the exact STATE.md section; a
  stale-source fact appears only as disclosed historical context
  naming the stale file, never re-attributed to a fresh source. The
  checker must grep-verify every file attribution and FAIL any claim
  the cited file does not contain.
- 2026-07-16 (latest run): Wrote "the degradation is accelerating"
  from only two data points (+1.00 → +4.70). Rule: trend-shape words
  (accelerating, compounding, trend) require 3+ consecutive points;
  with two, write "worsened sharply week-over-week" or similar.
- 2026-07-16 (latest run): A Next action named the receiving team
  ("route to the connect-wizard eng team") but no acting owner. Rule:
  every Next action names the acting owner AND, when routing, the
  receiving team (e.g., "On-call PM routes to ... this hour").
- 2026-07-16 (latest run): Kept the raw-verified counts (18/14) over
  contradicting prose (15/13) but omitted the mandatory one-line
  prose-discrepancy note for the data owner. Rule: whenever raw
  recounts contradict prose, the note goes in the report's Notes
  section; the checker FAILs a draft that omits it.
- 2026-07-16 (latest run): Round root ended up with two byte-identical
  report copies ([RUN-DATE].md plus output.md) and a leftover empty
  drafts/ directory. Rule: the promoted [RUN-DATE].md is the only
  report file at the round root; never write a second copy under any
  name; remove drafts/ if promotion leaves it empty.
- 2026-07-16 (latest run): The pass append created a second
  "## Last run" header at the bottom of STATE.md instead of a dated
  bullet under the existing section. Rule: STATE.md keeps exactly one
  "## Last run" section; appends add one new dated bullet under it.
- 2026-07-17: Reports read like a compliance log, not a VP memo: six
  flags of dense paragraph prose with no synthesis at all, and per-flag
  data buried in prose paragraphs instead of scannable tables. A reader
  had to read the whole document to find the one figure that mattered.
  Rule: every report now opens with a mandatory "## Bottom Line" block
  immediately after the header (3-5 bullets, each fusing a takeaway +
  why it matters + a citation to a step delta/ticket_id/source
  age/STATE.md count) — distinct from, and in addition to, the
  Plain-language summary that opens before the header for a
  non-specialist reader. Per-flag and source-health data now render as
  tables with the headline figure bolded. See Output format's Bottom
  Line and Formatting requirements. The checker FAILs a draft whose
  Bottom Line is missing, misplaced, under/over 3-5 bullets, or
  contains an uncited/generic bullet.

## Checker criteria
The checker is a separate agent/pass; a self-review inside the maker's
draft does not count and is itself a fail. Verify ALL of:
- No em dash (—) appears anywhere in the draft. Grep for it; any hit
  is a FAIL.
- Plain-language summary: a "Plain-language summary" section (3-5
  sentences, no jargon, no unexplained acronyms) opens the draft,
  before the header and before the Bottom Line / detailed
  funnel-evidence breakdown, and names both the biggest friction point
  and the single most important next action. Missing, misplaced (after
  the header or Bottom Line), or jargon-heavy is a FAIL.
- Bottom Line block: a "## Bottom Line" section sits immediately after
  the header, before any per-flag detail, with 3-5 bullets. For EACH
  bullet, confirm it cites something concrete found later in the draft
  or in a named source file (a step name + its delta, a ticket_id, a
  source-health age, a STATE.md consecutive-week count, a recomputed
  ratio) — a bullet with no checkable citation is a FAIL. FAIL any
  bullet that is generic filler applicable to any week's run (e.g.,
  "continue monitoring", "things look mostly fine", a restatement of
  the header with no number). FAIL if the block is missing, sits before
  the header or after per-flag detail, or has fewer than 3 or more than
  5 bullets. The Plain-language summary and the Bottom Line are two
  distinct, both-mandatory sections serving different readers (a
  non-specialist opener vs. a dense VP-skim block) — do not FAIL a
  draft for having both; FAIL only if either is missing or misordered.
- STATE.md was actually read: the draft's continuity lines match
  STATE.md's watch items, consecutive-week counts, and pattern log.
  If the draft claims STATE.md (or any required file) is missing,
  check the path yourself; if the file exists, FAIL.
- Both funnel and support sources read; every flag shows the baseline
  comparison.
- Independently recount every ticket count, subcount, and ratio from
  the raw CSVs (data rows only, exclude comments/header). Any wrong
  number is a FAIL even if the threshold conclusion survives.
- Independently recompute every percentage and delta at full precision
  and round once to 2 decimals; a double-rounded value (e.g., 19.21
  for 19.2049) is a FAIL. Confirm each headline number is identical at
  every occurrence in the draft (title, body, notes).
- Recounts are checked against the RAW files only. A draft that
  matches the raw rows passes that check even if some prose document
  disagrees; a draft that matches prose but not the raw rows FAILS.
- Run date is today's actual date; staleness ages are recomputed from
  it; EVERY source-health line shows the explicit "[RUN-DATE] minus
  [source date] = N days old" subtraction; sources >30 days old are
  called out, not silently used.
- Watch items crossing threshold are framed as escalations with a
  1-week consecutive count; sustained only at 3+ consecutive weeks in
  STATE.md; new flags distinguished from repeats.
- Known-structural steps from the pattern log are not re-flagged as
  new, and the pattern log (not stale notes) is cited as the basis.
- Citation provenance: for EVERY "noted in / per / logged in [file]"
  claim in the draft, open the cited file and confirm it contains that
  content. A claim the cited file does not contain is a FAIL — even if
  the fact is true elsewhere. Citations to STATE.md must name the
  section that actually holds the content (pattern log vs "Last run"
  entry); the wrong section is a FAIL. Any fact whose only source is a
  stale file must be disclosed as such — a stale-source fact carrying
  a fresh-source attribution is a FAIL.
- Trend language: FAIL any trend-shape word (accelerating,
  compounding, trend) supported by fewer than 3 consecutive data
  points.
- Prose-discrepancy note: if the raw recounts contradict any prose
  summary the run touched, the draft's Notes section must carry the
  one-line data-owner note; its absence is a FAIL.
- Every flag carries a Likely cause line and a Next action line with
  an acting owner (and receiving team when routing) — a Next action
  that names only the destination team FAILs.
- On pass: promote the draft to the round root, then append the run
  summary to STATE.md (date, flags with consecutive-week counts,
  numbers vs baseline, source health) as ONE dated bullet under the
  existing "## Last run" header — never a new "## Last run" header.
  The pass is invalid without BOTH; verify the append with `tail` on
  STATE.md. Confirm exactly one report file ([RUN-DATE].md) sits at
  the round root — no duplicate under any other name — and remove
  drafts/ if promotion left it empty.
- On fail: write flags/[RUN-DATE].md (the only fail artifact — no
  duplicate copies), leave the draft in drafts/, write nothing to the
  round root, append nothing to STATE.md. If an output for this date
  already exists at the round root, that is an extra FAIL to record
  and the failed run must not leave it standing as the output.
- A failed run is not the end: the maker fixes every listed failure
  and the checker re-runs; the loop ends only on a clean pass with
  both artifacts in place.
- Presentation layer (only if an HTML report was generated, and only
  after PASS): confirm every step conversion, delta vs baseline, flag,
  owner, and threshold in the HTML traces to the passed draft verbatim,
  with nothing added, dropped, or re-ranked from the draft's ordering.
  The all-clear state (no breach) and any UNAVAILABLE source are
  explicit, never blank or zeroed. The report is one self-contained
  file (inline CSS/SVG, no external assets). Grep the HTML for the
  em-dash character; any hit is a FAIL.
