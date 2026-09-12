name: launch-readiness
description: Runs 3 days before launch. Checks the feature against
the launch rubric, files a readiness report with every gap. PM
triages the gaps.
---
## Feature under review
Auto-Reschedule (Hatchboard), launching 2026-07-19. Sources, all
relative to the repo root:

- Checklist: data/launch-readiness/launch-checklist.md
- PRD: data/launch-readiness/prd-auto-reschedule.md
- Help doc draft: data/launch-readiness/docs-page.md
- Support macros: data/launch-readiness/support-macros.md
- Pricing page copy: data/launch-readiness/pricing-page.md
- Staging analytics events export: data/launch-readiness/analytics-events.md
- Rollback plan: data/launch-readiness/rollback-plan.md

## The rubric
- Help doc exists and describes shipped behavior
- Changelog entry drafted
- Success metric instrumented and firing in staging (every event named
  in PRD §7 must appear in the staging events export)
- Empty states and error states specified
- Support team briefed (or briefing doc exists)
- Rollback plan named
- Pricing/packaging impact confirmed with Finance (R. Iyer)
- Any checklist item marked N/A with a written sign-off from its owner
  counts as complete — do not flag it as a gap

## State file — read first, this is not optional
STATE.md lives in this skill folder and ALWAYS exists. Read it before
touching any fixture. It holds the last run summary, the pattern log,
and lessons learned. Never write that no prior-run state exists or
that the run is "stateless" — if STATE.md cannot be read, stop and
flag instead of proceeding. The report must quote STATE.md's last-run
date near the top as proof it was read.

State continuity rules (each is graded, none may be skipped):
1. Process-failure escalation. Before writing any verdicts, check the
   pattern log. If a rubric item gapped on 2 consecutive prior
   launches and gaps again in this run, that is 3 consecutive: it MUST
   be called out in a "Process failure" section at the very TOP of the
   report (above the rubric results), naming all three launches and
   dates. It is a process failure, not a one-off gap.
2. CLOSED, not PASS. Any item that was an open gap in the previous run
   and is now resolved is reported as "CLOSED (was GAP on <prior run
   date>)" with the closing evidence and the artifact that closed it.
   A plain PASS on such an item is a contract violation.
3. CARRIED OVER, not fresh. Any item that was an open gap in the
   previous run and is still a gap is labeled "GAP — CARRIED OVER
   (open since <prior run date>, owner <name>)", never presented as a
   newly discovered gap.
4. Append after pass. After the checker passes the report, append a
   new run summary to STATE.md: feature, date, gap count, which rubric
   items gapped, who owned them. Update the pattern log's consecutive
   counts. Preserve the existing pattern log entries and lessons
   learned — append, never rewrite history. A run whose report passed
   but whose STATE.md was not appended is incomplete.

## Output format
Report sections, in order:
1. Plain-language summary (3-5 sentences, no jargon): states the
   overall readiness call (ready / not ready / ready with conditions)
   and the single most important thing the reader should do, before
   any checklist or evidence. Written for someone who will not read
   past this section. No rubric-item names, no event names, no file
   citations here, plain words only.
2. Header (feature, launch date, report date, DRI, sources) plus one
   line: "Prior run: <date from STATE.md>, <N> gaps open."
3. Key Insights: mandatory synthesis block, immediately after the
   header and before every other section, including Process failure.
   3-5 bullets. Each bullet is one dense sentence: the single most
   important takeaway, why it matters to the launch call, and a
   citation to the specific evidence in the body below (a rubric
   verdict, an Appendix source, a gap count, a pattern-log streak).
   This is a different job from the plain-language summary above: the
   summary is jargon-free and citation-free for a reader who stops
   there. Key Insights is for the reader who wants the whole picture
   in 15 seconds and expects every claim backed. No bullet restates
   the header or the summary, and no bullet is a filler verdict
   ("things look mostly fine," "continue monitoring"). If a bullet
   would read identically on any other run, cut it.
4. Process failure section — only if rule 1 above triggers.
5. Gap count line: "<Feature>: X gaps, Y passes."
6. Rubric results: exactly ONE line per rubric item — the verdict
   (PASS / GAP / CLOSED), the single strongest piece of evidence, and
   the owner. No sub-bullets, no multi-line items. Event-by-event
   tables, decoy notes, and other supporting detail go in an
   "Appendix" section below the rubric results, referenced from the
   one-liner.
7. Next actions: one concrete next-step per GAP with owner and
   deadline, what that owner should do in the next hour, not a
   restatement of the gap.
8. Appendix (optional): verification detail moved out of the
   one-liners.
9. Checker verdict block (see Checker criteria).

## Presentation layer
After the checker returns PASS, the maker generates a self-contained
HTML readiness report FROM the passed markdown draft. The markdown
draft stays the audited source of truth; the gate and checker apply
to it in full. Never render an unpassed or flagged draft as a report.

Follow .claude/skills/_shared/report-style.md for color, type,
layout, and components. Do not redefine the palette, type scale, or
component kit here; reference that file.

Map it to this loop concretely:
- Report header: eyebrow "LAUNCH READINESS SWEEP" with the feature,
  launch date, and report date; H1 the feature name; run meta strip
  with the sources swept, the "Prior run: <date>, <N> gaps open" line
  from STATE.md, and the green PASS checker badge.
- Bottom-line banner: the overall verdict, GO / NO-GO / CONDITIONAL,
  as the single boldest element, carrying the gap count ("X gaps, Y
  passes") verbatim from the draft.
- Readiness meter or area status grid: one row or cell per launch
  area (eng, QA, docs, support, marketing, legal) showing ready /
  at-risk / blocked, each state in its semantic color (good / warn /
  crit), never a state absent from the draft.
- Process failure: if the draft has a Process failure section, render
  it as a crit banner at the very top, above the areas, naming all
  three launches and dates verbatim.
- Blockers: each GAP renders a crit severity chip (● BLOCKED /
  ▲ AT-RISK) plus a left severity stripe, with owner name, due date,
  and the one concrete next step, all from the draft.
- Main audited checklist table: exactly one row per rubric item, in
  the draft's order, with a status chip (PASS / GAP / CLOSED / CARRIED
  OVER), the strongest evidence line, and the owner. Every listed row
  present; CLOSED and CARRIED OVER labels preserved verbatim.
- Provenance footer: source files, run timestamp, checker PASS, and
  "Generated from the audited draft; every figure traces to source."

Rules: every status, name, date, event, and macro ID traces to the
passed draft verbatim. Add no rubric item, upgrade no status (a GAP
never renders as ready, a CONDITIONAL never as GO), and reorder
nothing in a way that changes meaning. Any UNAVAILABLE or "could not
verify" in the draft shows an explicit unavailable state, never a
blank, a zero, or a green cell. One self-contained HTML file, inline
CSS and inline SVG only, no external fonts, scripts, or images. Same
no-em-dash bar as the draft: never use an em dash (—) anywhere in the
HTML; use a period, comma, or colon.

## Formatting rules (apply to the whole report)
- Never use an em dash (—) anywhere in the output. Use a period, a
  comma, or a colon instead. This applies to every section, including
  the summary, verdict lines, next actions, appendix, and the checker
  verdict block.
- Real markdown headers (##/###) for every named section. Never bold
  text standing in for a header.
- Anything with more than one attribute per row is a table, not
  prose or a bulleted list: rubric results, event-by-event
  instrumentation checks, pattern-log streaks, before/after gap
  counts across runs.
- Bold the single most important figure or call in each section: the
  gap count, the process-failure item name, or the strongest evidence
  line. One bold per section, not a paragraph of bolded text.
- No walls of prose. A section running past 2-3 sentences of prose
  gets restructured as a table or bullets.

Evidence rules:
- Every number, date, event name, macro ID, and count is recomputed
  from the fixtures and cited to the file it came from. Never carry a
  figure into the report without a source.
- For the instrumentation item, a "first seen after the feature
  shipped" claim requires evidence of the feature-branch merge date.
  If the merge date is not in any fixture, say "merge date could not
  be verified" rather than asserting the event is post-feature.
- Legacy or similarly-named events, signed-off N/A items, and items
  with genuine published evidence are not gaps. Do not flag an item
  just because it resembles a past failure; verify against the actual
  fixture before flagging.

## Known failure modes
- Metric "firing in staging" passed because an old event with the same
  name was firing. Verify the event's first-seen date is after the
  feature branch merged, and check every PRD-named event individually.
- A Slack "will do" is not evidence for support briefing; only a
  published artifact (macros, doc, recording) is.
- A run claimed "no prior-run state exists in this stateless run"
  while STATE.md was present with a last run, pattern log, and
  lessons. Never assert state is absent; open STATE.md and quote its
  last-run date in the report.
- A previously-open gap that had since been resolved was reported as
  a plain PASS with no reference to the prior run. It must be CLOSED
  with the closing evidence.
- A gap that was already open in the prior run was presented as a
  fresh finding. It must be labeled CARRIED OVER with the open-since
  date and owner.
- An item at 2 consecutive gaps in the pattern log gapped a 3rd time
  and was listed as an ordinary gap. The 3rd consecutive gap must be
  escalated at the TOP of the report as a process failure.
- After a passing run, no run summary was appended to STATE.md, so
  the loop's memory did not advance. Appending is part of passing.
- The checker declared "passed" while violating explicit checker
  criteria, justified by the fabricated stateless claim. The checker
  must verify every listed criterion against STATE.md itself, not
  trust the draft's own framing.
- An instrumentation PASS cited "first seen post-feature" with no
  merge-date evidence. Cite the merge date or state it could not be
  verified.
- Rubric verdicts sprawled across multi-line sub-bullets, breaking
  the one-line-per-item format. Keep the verdict to one line; detail
  goes in the Appendix.
- A report opened straight into the header and rubric table with no
  plain-language summary, so a reader skimming the top saw jargon and
  file citations before learning the overall call. The summary
  section must be first, before the header.
- Em dashes crept into verdict lines and the summary via habit. Read
  the draft back for the character before saving; replace with a
  period, comma, or colon.
- 2026-07-17: Reports read like a flat compliance checklist. PASS/GAP
  lines with no synthesis up top, adjectives doing the work numbers
  should ("significant risk," "should be fine"), prose paragraphs
  standing in for tables. Added a mandatory Key Insights block right
  after the header (3-5 cited, non-generic bullets) plus a
  VP-of-Product voice bar for the whole draft: no filler, every claim
  cited, a number or nothing instead of an adjective. Same verdicts,
  now readable in 15 seconds instead of a full pass through the
  report.

## Checker criteria
The checker verifies each criterion below individually, against the
fixtures and STATE.md directly — never by trusting the draft's
self-description. The checker verdict block at the end of the report
lists every criterion with its result and the evidence checked:
1. Every rubric item has exactly one verdict line: PASS, GAP, or
   CLOSED. No item skipped, no multi-line verdicts.
2. Every PASS and CLOSED cites evidence (a file, a dashboard, a
   message), and every number/date/ID in the report traces to a
   fixture.
3. STATE.md was read: the report quotes the correct last-run date and
   prior gap count, and makes no claim that state is absent.
4. Repeat offenders: if STATE.md's pattern log plus this run's
   verdicts put any item at 3 consecutive gaps, a process-failure
   callout appears at the top of the report. Verify by reading the
   pattern log, not the draft's summary.
5. Previously-open items now resolved are shown as CLOSED with
   closing evidence; previously-open items still gapped are labeled
   CARRIED OVER with the open-since date. Cross-check the previous
   run's gap list in STATE.md item by item.
6. Signed-off N/A items are not flagged as gaps.
7. Every GAP has a next action with owner in the Next actions section.
8. On pass, the run summary was appended to STATE.md (feature, date,
   gap count, gapped items, owners) with the pattern log and lessons
   preserved.
9. A plain-language summary (3-5 sentences, no jargon) appears as the
   very first section, before the header and the rubric results, and
   states the overall readiness call plus the single most important
   next step for the reader.
10. No em dash (—) appears anywhere in the report. Any instance found
    is a fail; the checker fixes formatting only by requiring the
    draft to be corrected, it does not silently rewrite the draft
    itself.
11. Key Insights exists immediately after the header, has 3-5
    bullets, and every bullet cites something concrete and checkable
    from the body (a rubric verdict, an Appendix source, a gap count,
    a pattern-log streak). Reject any bullet generic enough to apply
    to any run ("things look mostly fine," "continue monitoring") or
    that cites nothing in the report itself.
12. If an HTML presentation report was generated, it was built only
    after this PASS and only from the passed draft. Every status,
    name, date, event, and macro ID in the HTML traces to the draft
    verbatim, with no rubric item added, no status upgraded (no GAP
    shown as ready, no CONDITIONAL shown as GO), and no reordering
    that changes meaning. Any UNAVAILABLE or "could not verify" in the
    draft renders as an explicit unavailable state, never a blank,
    zero, or green cell. The report is one self-contained file with
    inline CSS and SVG and no external assets, and carries no em dash
    (—) anywhere.
A checker verdict of "passed" that skips or fails any criterion above
is itself a contract violation.
