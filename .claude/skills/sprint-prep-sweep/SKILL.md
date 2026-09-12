name: sprint-prep-sweep
description: Runs the day before sprint planning. Sweeps every ticket
in the sprint candidate list against a fixed readiness checklist and
drafts a prep report ranked by severity. Findings only — it never
edits tickets.
---
## Sources
- Backlog export: data/sprint-prep-sweep/backlog-export.json
  (fixture — swap for your real Jira/Linear MCP next-sprint filter)
- Sprint goal: data/sprint-prep-sweep/sprint-goal.md

## Step 0 — state (MANDATORY, before anything else)
Read .claude/skills/sprint-prep-sweep/STATE.md. This is not optional
and is never "not applicable": if the file exists, the run is
stateful. The report MUST open with a "State consulted" line naming
STATE.md's last-run date and the number of tickets in the
repeat-offender log. A report that lacks this line, or that claims
the loop is stateless, is an automatic checker FAIL.

For every entry in STATE.md's repeat-offender log, classify it in
this run (match by ticket ID + failed check):
- RESOLVED — the ticket now passes that check. Report it in a
  "Resolved since last sweep" section. Never silently drop it or
  fold it into the ready list without the note.
- REPEAT OFFENDER — still failing the same check, 2+ consecutive
  sweeps counting this one. Label it with the sweep count,
  first-failed date, and owner in a dedicated "Repeat offenders"
  section — not as a fresh finding.

### Counting sweep counts (arithmetic, not archaeology)
STATE.md's recorded sweep count is always "as of the last time the
file was updated" — it is never this run's count. If a ticket fails
the same check again this run, this run's count is STATE.md's
recorded number **plus one**. Never read STATE.md's number and
restate it unchanged, and never try to re-derive the count by
counting dates in the file — STATE.md is not guaranteed to log every
historical date, only the most recent one. Write the recorded number
and the new number side by side before drafting, so the +1 is
auditable, not asserted.

## Readiness checklist (fixed — every ticket, every item)
1. Acceptance criteria present (an empty field, "TBD", or a bare
   pointer like "see spec" all fail — criteria must actually exist).
2. Sized (estimate field populated; null fails).
3. No unresolved blocking dependency (a blocker that will land
   before the ticket is reachable mid-sprint is noted, not waved
   through — quote the blocker status).
4. Linked spec/design exists and is current (dead link or archived
   page fails; "n/a" is acceptable only for bugs and spikes where
   the ticket itself carries the context).
5. No open questions in comments (an unanswered question that gates
   the build fails; answered or informational comments pass).

These five items are the entire readiness bar. Whether a ticket is
named in the sprint goal's prose, or looks like a scope surprise, is
not a checklist item and must never be raised as a reason to doubt a
ticket that passes all five — see "Planning risks" below.

## Severity ranking
- BLOCKS PLANNING: the ticket cannot be committed in the meeting as
  is (no acceptance criteria, unresolved blocking dependency, open
  question gating the build).
- FIX BEFORE PLANNING: quick pre-meeting fix (unsized, dead spec
  link with the content recoverable elsewhere).
Rank findings BLOCKS PLANNING first, then FIX BEFORE PLANNING.

## Quotes and citations
- Every finding cites the ticket ID and quotes the missing or
  failing element verbatim from the export (the empty field, the
  blocker status line, the open comment, the dead link status). If
  you shorten or reword, drop the quotation marks and label it
  "(paraphrase)". The checker diffs quotes against the export.
- Never carry a finding from memory or a prior report — re-check
  every ticket against every item at run time.

## Read-only rule
This loop never edits tickets. Findings only; a human fixes. Any
draft that describes changing a ticket field is an automatic FAIL.

## Output style rules (apply to every section)
- Never use an em dash (—) anywhere in the report. Use a period or a
  comma instead, or restructure the sentence. This applies to every
  section, including quoted paraphrases and the plain-language
  summary below. A single em dash anywhere in the draft is an
  automatic checker FAIL.
- Plain-language summary is mandatory and goes first, before the
  header. See "Plain-language summary" below for its contents and
  the checker bar it must meet.

## Plain-language summary (goes first, before the Header)
3-5 sentences, no jargon (no ticket IDs, no checklist-item names like
"acceptance criteria", no severity labels like "BLOCKS PLANNING" as
raw labels without explaining them in plain words). It must state, in
words a non-PM stakeholder would understand:
1. Whether the sprint looks ready to plan or not, in plain terms
   (e.g., "most of the backlog is ready, but a few tickets need work
   before the meeting").
2. Roughly how many tickets are in good shape versus need attention.
3. The single most important thing the reader should do before
   planning starts (one concrete action; name the owner and describe
   the ticket in plain words rather than citing its raw ID).
This section is a summary for someone skimming, not a restatement of
every finding. It comes before the detailed backlog breakdown
(Header onward), not after it.

## Bottom Line — mandatory synthesis block
Distinct from the plain-language summary above: this is the VP-dense
version, not the jargon-free one. It is the first section after the
Header, before "State consulted" or any other detail. 3-5 bullets,
each one dense sentence: the single most important takeaway, why it
matters to planning, and a citation back to the specific evidence in
the body below, a ticket ID, a section name (e.g. "Repeat
offenders"), a sweep count, a number. A VP should read these bullets
in 15 seconds and have the whole picture without opening the body.

No bullet restates the Header (date, sprint name, ticket count,
already ran once above it) or the plain-language summary. No bullet
is filler that could describe any sweep. "A few tickets need
attention," "things look mostly fine," "continue monitoring" are all
automatic FAILs. Draft this section last, after the sweep and
findings exist, so every citation resolves to something actually in
the draft. Written in the voice bar from MAKER.md: dense, cited,
confident, no unsupported adjectives.

- GOOD: "TICKET-142 is now a 3rd-consecutive-sweep repeat offender
  for missing acceptance criteria (Repeat offenders); [owner] hasn't
  fixed it across two prior sweeps and it will eat meeting time again
  unless written before Thursday."
- BAD: "Several tickets have issues that should be resolved before
  planning." (no ticket ID, no section reference, no number, could
  be copy-pasted into any week's report.)

## Output format
Report sections, in order:
1. Plain-language summary (see above).
2. Header: run date, sprint, tickets swept count, sources used.
3. Bottom Line: the mandatory synthesis block (see above), 3-5
   dense, cited bullets. Always third, always right after the Header.
4. State consulted: STATE.md last-run date + repeat-offender count.
5. Resolved since last sweep (if any).
6. Repeat offenders (if any): ticket ID, failed check, Nth
   consecutive sweep, first-failed date, owner.
7. Findings — BLOCKS PLANNING: per finding — ticket ID, checklist
   item failed, quoted failing element, owner, one-line fix.
8. Findings — FIX BEFORE PLANNING: same fields.
9. Ready: every ticket with zero findings, listed by ID with a
   one-line reason it passed. Omission is not readiness.
10. Planning risks: 3-5 lines tying the *findings* (BLOCKS PLANNING,
    FIX BEFORE PLANNING, repeat offenders) to the sprint goal, what
    the goal loses if those tickets slip. Never introduce doubt about
    a ticket that passed all five checklist items and sits in the
    Ready list, e.g., a ticket absent from the goal's stated scope
    is not a risk; it already cleared the only bar that matters. This
    section discusses findings, not Ready tickets.
11. Checker verification (filled by checker, every criterion PASS or
    FAIL, "not applicable" is forbidden).

Formatting bar (every section, not just Bottom Line):
- Real markdown headers (##) per section, no unlabeled paragraph
  break doing the work of a header.
- Any list with more than one attribute per item (Repeat offenders,
  Findings, Ready) renders as a markdown table, columns for ticket
  ID, checklist item, quoted evidence, owner, etc., not a prose
  paragraph per ticket.
- Bold the single most important figure or call in each section (the
  blocking-ticket count, a repeat offender's sweep count, the ready
  count), one bolded anchor per section, not a bolded sentence.
- No walls of prose. If a section runs past 3 sentences of running
  text, it should be a table or bullet list instead.

## Presentation layer
After the checker returns PASS, the maker generates one self-contained
HTML report from the passed markdown draft. The draft stays the
audited source of truth; the gate and checker apply to it in full.
Never render an unpassed or flagged draft as a polished page.

Follow .claude/skills/_shared/report-style.md for color, type, layout,
and components. Do not redefine the palette, type scale, or component
kit here; reference that file.

Map this sweep concretely:
- Report header: eyebrow "SPRINT PREP SWEEP" + run date and sprint
  name, H1 title, run-meta strip naming the backlog export and sprint
  goal sources and the green PASS badge.
- Bottom-line banner: how many candidate tickets are planning-ready
  versus blocked, the blocked count bolded as the single loudest
  figure.
- Stat tiles: three KPI cards, Ready count, Fix-before-planning count,
  Blocks-planning count, each colored by severity (good / warn / crit).
  A count whose source is UNAVAILABLE shows the muted UNAVAILABLE state
  naming the source, never a fake zero.
- Per not-ready ticket: a severity chip (● BLOCKS PLANNING crit,
  ▲ FIX BEFORE PLANNING warn) plus a left stripe in the same hue,
  labeled by which checklist item is missing (acceptance criteria,
  estimate, blocking dependency, spec/design link, open question).
- Main audited table: every ticket to missing piece(s) to owner to the
  one-line next step, verbatim from the draft, every listed row
  present, quoted evidence intact.
- Repeat offenders and Resolved sections carry their sweep-count
  counter chip and disposition exactly as the draft states them.
- Provenance footer: source files, run timestamp, checker PASS, and
  "Generated from the audited draft; every figure traces to source."

Every ticket ID, checklist item, quoted element, owner, and count
traces to the passed draft verbatim. Invent no ticket, add no figure
or adjective, and never reorder findings in a way that changes
severity meaning. UNAVAILABLE stays explicit. Ship one self-contained
HTML file (inline CSS, inline SVG, no external assets). The same
no-em-dash bar applies: a single em dash anywhere in the HTML is a
FAIL.

## State file
STATE.md has exactly three sections, each appearing once: "## Last
run", "## Repeat offenders", "## Lessons learned". After the checker
passes, update it — do not blindly append text:
- "## Last run" — replace its content with this run's summary (date,
  tickets swept, findings by severity). The prior run's block does
  not stay behind, and a second "## Last run" heading never appears.
- "## Repeat offenders" — updated in place: each still-failing
  ticket's line gets the new sweep count (recorded count + 1, per
  Step 0); RESOLVED tickets' lines are removed; newly-qualifying
  tickets are added. No second "## Repeat offenders" heading below
  the old one.
- "## Lessons learned" — true append-only; add a new dated bullet,
  never remove or rewrite an existing one.
A run is not complete until this update happens; the checker owns it
and must not stamp a pass without it. If an edit would leave two
headings with the same name, that is the signal it was done wrong —
edit the existing section instead of appending a new block.

## Known failure modes
(Write every mistake here the day it happens. This becomes the most
valuable part of the skill file.)
- 2026-07-07: a ticket whose acceptance_criteria field read
  "AC: see spec" was passed as having criteria. Rule: a pointer is
  not criteria — the field must contain testable statements, or the
  linked spec must be opened and shown to contain them.
- 2026-07-07: a ticket missing from the report entirely was assumed
  ready by the team and pulled into the sprint unsized. Rule: every
  ticket in the export appears in the report by ID, as a finding or
  in the ready list — the checker reconciles the two lists against
  the export count.
- 2026-07-17: two repeat offenders already at "2 consecutive sweeps"
  in STATE.md failed the same check again, and both maker and
  checker restated "2nd consecutive sweep" instead of incrementing —
  STATE.md's number is as of the last run, not this one, and neither
  Step 0 nor checker criterion 6 spelled out the +1. Rule: this run's
  sweep count is always STATE.md's recorded count plus one; restating
  it unchanged is a FAIL (see "Counting sweep counts" under Step 0).
- 2026-07-17: Planning risks flagged two Ready tickets (both passing
  all five checklist items) as possible "scope creep" for not being
  named in the sprint goal's prose. Rule: goal/scope alignment is not
  one of the five checklist items — Planning risks discusses only
  tickets with findings or repeat-offender status; a Ready ticket is
  never re-litigated there.
- 2026-07-17: the state append duplicated "## Last run" and "##
  Repeat offenders" headers instead of replacing/updating the
  existing ones, leaving a stale block a future run could read by
  mistake. Rule: STATE.md keeps exactly one instance of each section
  — "Last run" is replaced wholesale, "Repeat offenders" entries are
  updated or removed in place, only "Lessons learned" is append-only.
- 2026-07-21: the new "no em dash anywhere" rule collided with two
  backlog-export fields whose source text contains an em dash inside
  the exact string that needed quoting (a blocked-by status and a
  dead spec-link status). Quoting them verbatim would violate the
  em-dash rule; silently swapping the em dash for a comma while
  keeping quotation marks would violate the verbatim-quote rule.
  Rule: when a quote would contain an em dash, drop the quotation
  marks, replace the em dash with a comma or period, and label it
  "(paraphrase)" instead of presenting an altered string as verbatim.
- 2026-07-17: reports were accurate but read like a raw checklist
  dump: no synthesis up top, prose paragraphs instead of tables,
  hedged filler ("a few tickets may need attention") instead of
  numbers. A VP skimming it for 15 seconds got nothing usable. Rule:
  every report now opens with a mandatory "Bottom Line" block (3-5
  dense, cited bullets) right after the Header, and the body uses
  tables, bold key figures, and real headers instead of prose, see
  "Bottom Line" and the formatting bar under "Output format."

## Checker criteria
Answer each with PASS or FAIL plus one line of evidence. "Not
applicable" is forbidden. Any FAIL fails the draft.
1. Report contains a "State consulted" line citing STATE.md's
   last-run date; STATE.md was actually read.
2. Every ticket ID in the backlog export appears exactly once in
   the report — as a finding or in the ready list. Reconcile the
   counts yourself against the export.
3. Every ticket was checked against all five checklist items; a
   ticket with multiple failures shows every failure, not just the
   worst one.
4. Every finding cites a ticket ID and quotes the missing or
   failing element; every quotation-marked string is verbatim in
   the export (spot-check by searching the file); paraphrases are
   labeled.
5. Severity ranking follows the SKILL.md definitions; BLOCKS
   PLANNING findings appear before FIX BEFORE PLANNING.
6. Every STATE.md repeat-offender entry has an explicit disposition:
   RESOLVED or REPEAT OFFENDER (Nth sweep, owner). Recompute sweep
   counts yourself as STATE.md's recorded number **plus one** for
   every ticket still failing the same check — STATE.md's number is
   as of the last run, not this one; restating it unchanged is a
   FAIL. Same check failing 2+ consecutive sweeps counting this run
   = repeat-offender section, not a fresh finding.
7. No ticket was edited and the draft proposes no ticket edits by
   the loop itself (suggested fixes are addressed to humans).
8. On pass, STATE.md is updated (not blindly appended to) before
   "checker: passed" is written: "## Last run" replaced (not
   duplicated), "## Repeat offenders" entries updated or removed in
   place (not appended as a second block), "## Lessons learned" gets
   a new bullet if applicable. Exactly one of each section heading
   exists afterward — two headings with the same name is a FAIL.
9. Planning risks discusses only findings (BLOCKS PLANNING, FIX
   BEFORE PLANNING, repeat offenders), it raises no scope or
   goal-alignment doubt about any ticket in the Ready list. A Ready
   ticket being unnamed in the sprint goal's prose is not a valid
   risk to raise.
10. No em dash (—) appears anywhere in the report. Search the full
    draft text yourself; a single instance is a FAIL.
11. The report opens with a plain-language summary (before the
    Header), 3-5 sentences, no jargon (no raw ticket IDs, checklist
    item names, or severity labels used without plain explanation),
    stating sprint readiness in plain terms, a rough count of
    tickets in good shape versus needing attention, and naming the
    single most important action the reader should take before
    planning. A summary that is missing, placed after the Header, is
    longer than 5 sentences, or is just a restatement of the
    findings list, is a FAIL.
12. Bottom Line is present as the third section (right after the
    Header, before State consulted), has 3-5 bullets, and every
    bullet cites something concrete that actually exists in the body
    or sources below, a ticket ID, a named section, a sweep count, or
    a number. Resolve each citation yourself against the rest of the
    draft. A bullet that merely restates the Header or the
    plain-language summary, or that is generic enough to paste into
    any run ("continue monitoring," "things look mostly fine"), is a
    FAIL.
13. If an HTML presentation-layer report was generated, it was built
    only after this PASS, and every ticket ID, checklist item, quoted
    element, owner, count, and next step in it traces verbatim to the
    passed draft. Nothing was added, dropped, or re-ranked in a way
    that changes severity meaning, and every UNAVAILABLE stays
    explicit, never rendered as a zero or blank. The report is one
    self-contained file (inline CSS and SVG, no external assets) and
    carries no em dash anywhere. Any divergence is a FAIL.
