name: sales-deal-intelligence
description: Runs every Friday. Reads the CRM export of open-pipeline
deals and deals closed this week plus AE/SE notes, files a PM
takeaways brief: PM assists for open deals, roadmap learnings from
closed deals tagged against the five win/loss dimensions, and
repeating-pattern alerts computed against STATE.md.
---
## Sources
Paths are relative to the repo root (/Users/aakashgupta/Downloads/pm-loop-pack).
For the week ending 2026-07-17:
- Deals export: data/sales-deal-intelligence/deals-2026-07-17.csv
- AE notes: data/sales-deal-intelligence/ae-notes-rachel-kim-2026-07-17.md
- AE notes: data/sales-deal-intelligence/ae-notes-diego-fuentes-2026-07-17.md
- AE notes: data/sales-deal-intelligence/ae-notes-marcus-hale-2026-07-17.md
- AE notes: data/sales-deal-intelligence/ae-notes-priya-shah-2026-07-17.md
- SE call log: data/sales-deal-intelligence/se-call-log-2026-07-17.md

These are bundled fixtures. To run against your real pipeline, swap
this list for your Salesforce/HubSpot MCP source (export: deals in
open stages + deals with a close date in the last 7 days, plus the
activity/notes feed per deal) and keep everything below unchanged.

## Context
Product: Meridian Ops Analytics — B2B operations-analytics platform
for mid-market logistics (3PLs, carriers, shippers). Strengths:
best-in-class dashboarding and reporting, flexible REST API +
webhooks, Okta/SAML SSO. Known objections: no native TMS connectors
(McLeod, Trimble), ~90s webhook latency vs. competitors' sub-60s
streams. Primary competitors: Cortexa, FreightIQ, Dockwise.

## Win/loss dimensions (fixed taxonomy — absorbed from the retired win-loss tracker)
Price, features, competition, timing, champion strength.
- A closed deal CITES a dimension when the sources substantively
  discuss it for that deal — whether or not it decided the outcome.
  A factor the sources explicitly call non-deciding is still cited;
  it stays secondary in the narrative, but its streak advances.
- NOT cited = the dimension is absent from the sources, or the only
  mention is an affirmative statement that it was not a factor
  (e.g., "took list, no discount asked").
- Decoys: "budget" can mean amount (price) or fiscal calendar
  (timing) — verify before tagging. "Revisit in N months" /
  door-open comments are pipeline notes, not timing evidence.
  Prospect praise does not soften a loss — tag what decided it.

## Streak arithmetic (the repeating-pattern rule)
Closed deals are processed in close-date order (ties broken by deal
ID). Both wins and losses count. For each dimension: start from
STATE.md's pattern-log count; +1 per citing closed deal; reset to 0
on a closed deal where the dimension is not cited. A deal flagged
insufficient-data is EXCLUDED from streak arithmetic entirely — it
neither advances nor resets any streak. A dimension reaching 3+
consecutive closed deals is a repeating pattern: declare it with the
count and the deal IDs in the streak. If a streak crossed 3 earlier
in the week and then broke, declare both the hit and the break —
never hedge with "worth watching."

## The no-commitments rule (hard)
PM assists for open deals may only use what the product does today:
explanation, positioning, objection handling, pointing at existing
docs or gaps in docs. Never a feature promise, ship date, "coming
soon," "on the roadmap," or "planned" — even softened, even when
the AE's notes beg for one. If the only honest assist would be a
promise, write "no assist available — roadmap gap: [what's missing]"
and let it land in section (b) as a learning instead.

## Output format (exact — the checker verifies each element)
1. Header: "Deal Intelligence Brief — week ending YYYY-MM-DD" plus a
   sources-read line with the deal count from the export (header row
   excluded) split open/closed.
2. **Bottom Line (mandatory, first thing after the header, before
   any detailed section).** 3-5 bullets, each one dense sentence
   carrying three things: the single most important takeaway, why
   it matters, and a citation back to specific evidence in the body
   below (a deal ID, a dimension + streak count, a section
   reference). Draft this last — once (a), (b), and (c) exist — so
   every bullet points at something real already on the page. Never
   a restatement of the header, never vague ("things look mostly
   fine," "continue monitoring the pipeline") — a genuine synthesis
   a VP could read in 15 seconds and have the whole picture.
3. **(a) Open deals — where PM can help.** One block per open deal:
   "NW-xxxx Account (stage, $amount)", the live objection with its
   source file cited, and one "PM assist:" line — concrete and
   startable this week. Open deals with no substantive notes yet get
   an insufficient-data flag here instead of an invented objection.
4. **(b) Roadmap learnings — closed this week.** One block per
   closed deal in close-date order: "NW-xxxx Account — Won/Lost
   M/D, $amount", then one line per CITED dimension with evidence
   (non-deciding dimensions annotated "(non-deciding)"), then a
   "Not cited:" line naming the remaining dimensions. Closed deals
   with no usable sources get an explicit insufficient-data flag
   (deal ID + what's missing) instead of tags.
5. **(c) Repeating patterns.** All five dimensions with recomputed
   consecutive counts and the deal IDs in each active streak;
   threshold hits (3+) declared, broken streaks stated as broken.
6. Coverage is total: every deal_id in the export appears in exactly
   one of (a), (b), or an insufficient-data flag. Silent omissions
   are a coverage failure.

## Presentation layer
After the checker returns PASS, the maker generates a self-contained
HTML report FROM the passed markdown draft. The draft stays the
audited source of truth; the gate and checker apply to it in full. Never
render an unpassed or flagged draft as a report.
- Follow `.claude/skills/_shared/report-style.md` for color, type,
  layout, and components. Do not redefine the palette or type scale here.
- Report header: eyebrow "Deal Intelligence Brief" + week ending date,
  H1 title, run-meta strip naming the sources read (deals CSV, AE notes,
  SE call log) and a green PASS verdict badge.
- Bottom line banner: the draft's 3-5 Bottom Line bullets, verbatim, at
  the top of the body, the single most important figure bolded.
- Stat tiles (one responsive row): total ARR at stake across open deals,
  open deal count, closed deal count (won/lost split), and count of
  dimensions at a 3+ streak. Each figure copied verbatim from the draft;
  a tile whose source is UNAVAILABLE shows the explicit unavailable state
  naming the source, never a zero.
- Severity/priority chips: closed-deal outcomes render as chips (won =
  good, lost = crit), open deals with a live competitive mention or a
  roadmap gap get an AT-RISK (warn) chip, insufficient-data deals get a
  muted chip. A dimension that hit its 3+ streak renders a BREACH chip.
  Chipped rows carry the matching left severity stripe.
- Main audited table: the closed-deal list (deal, account, outcome,
  amount, dimensions cited) as the primary table, every listed deal
  present in the same order as the draft; the open-deal table (deal,
  stage, amount, objection) and the repeating-patterns table (dimension,
  count, streak deal IDs) render in full alongside it.
- Owner + next-step: each open-deal row renders its PM assist line inline
  under the objection; each repeating-pattern hit renders its recommended
  product action and owner from the draft.
- Provenance footer: source files, run timestamp, checker PASS, and
  "Generated from the audited draft; every figure traces to source."
- Every figure, quote, deal ID, account name, and dimension traces to the
  passed draft verbatim. Add no data, invent no owner, and never reorder
  in a way that changes meaning. UNAVAILABLE stays explicit. One
  self-contained HTML file (inline CSS and SVG), and the same no-em-dash
  bar the draft carries.

## Formatting (the checker verifies this too)
- Real markdown headers (##/###) for every section — never bolded
  prose standing in for a header.
- A table wherever the content is naturally tabular: the open-deal
  list (deal, stage, amount, objection), the closed-deal list (deal,
  outcome, amount, dimensions cited), and the repeating-patterns
  section (dimension, count, streak deal IDs) all qualify — render
  them as tables, not paragraphs.
- Bold the single most important figure or call per section — the
  amount at risk, the outcome, the streak count. One per section,
  the one that matters most, not every number in sight.
- No walls of prose. A paragraph running past ~3 sentences becomes a
  table row or a bullet instead.

## Voice (VP of Product bar — the checker verifies this too)
Every section reads like a VP of Product with 20 years of pattern-
matching across deals wrote it, not a summary intern.
- High information density: no filler, no throat-clearing ("it is
  important to note," "as we can see," "moving forward").
- Every claim cites its evidence inline — a deal ID, a source file,
  a figure. An uncited claim is a violation, not a style choice.
- Confident and precise: state the call ("Cortexa beat us on
  latency in 3 of 4 competitive losses this month"), never a hedge
  ("latency might be an issue").
- Zero unsupported adjectives. "Significant," "robust," "major," and
  "strong" are banned unless immediately followed by the number
  that earns them — a number or nothing.

## Numbers and quotes
Every figure (amounts, discounts, latencies, scores) copied exactly
from a source file — never rounded, averaged, or invented. Quotes
verbatim with speaker attributed. Every takeaway cites a deal ID
that exists in the export.

## Formatting rule (hard)
Never use an em dash (—) anywhere in the output. Use a period,
comma, or colon instead. This applies to every section of the
brief, no exceptions.

## State file (mandatory, first read of every run)
STATE.md lives in this skill folder
(.claude/skills/sales-deal-intelligence/STATE.md) and ALWAYS exists —
it is pre-seeded with prior deals. Open it before touching any
source and transcribe the pattern log's per-dimension counts and
deal IDs into your working notes. Sanity-check inherited counts:
each count must equal the number of deal IDs listed for its streak.
If you cannot read STATE.md, stop and flag the run — never proceed
with a "no baseline" fallback. After a passing run, the checker
appends: date, deals covered (open/closed/flagged), dimensions cited
per closed deal, updated pattern log, and any threshold hits. Every
count the checker writes must be its own recomputation, never copied
from the draft — a wrong count here suppresses a due alert weeks
later.

## Known failure modes
(Write every mistake here the day it happens.)
- 2026-07-03: a PM assist for an open deal read "reassure them the
  McLeod connector is on the near-term roadmap" — a feature
  commitment wearing a helpful hat. Checker flagged it. Assists
  explain what exists today; roadmap gaps go in section (b), not in
  the prospect's ear.
- 2026-07-10: a deal auto-closed by RevOps hygiene (no activity, no
  loss reason) was tagged across all five dimensions from stage
  history alone, advancing streaks with invented evidence. No
  usable sources = insufficient-data flag, excluded from streak
  arithmetic.
- 2026-07-17: the brief read like a correct data dump: five
  paragraphs of tagged deals with no synthesis, so a VP had to read
  all of (a)-(c) to find the one deal or streak that actually
  mattered. Added a mandatory Bottom Line block (3-5 cited bullets,
  first thing after the header, written last), a VP-of-Product
  voice bar (dense, cited, confident, no unsupported adjectives),
  and stricter formatting (real headers, tables for deal lists and
  pattern counts, one bold figure per section). The brief now leads
  with the whole picture in 15 seconds instead of burying it.

## Checker criteria (binary — ALL must hold or the run fails)
1. Every deal_id in the export appears exactly once across (a), (b),
   and insufficient-data flags; the open/closed split matches the
   CSV (header row excluded). A silently missing or duplicated deal
   fails.
2. Every takeaway, objection, and evidence line cites a deal ID that
   exists in the export; quotes and figures spot-checked verbatim
   against the source files.
3. No PM assist contains a feature promise, ship date, or roadmap
   commitment — "coming soon," "planned," and "on the roadmap" all
   fail, regardless of hedging.
4. Dimension tags use the cited definition: substantively discussed
   = cited (even if non-deciding); absent or affirmatively-not-a-
   factor = not cited. Every closed-deal block has both cited lines
   and a "Not cited:" line, consistent with each other.
5. Streaks recomputed by the checker itself from STATE.md's pattern
   log plus this week's closed deals in close-date order,
   insufficient-data deals excluded. Every 3+ streak declared with
   deal IDs; every break stated; a hedge or a wrong count fails.
6. Insufficient-data flags are explicit (deal ID + what's missing),
   never silent omissions or padded paragraphs of invented context.
7. No em dash (—) appears anywhere in the draft. Any occurrence
   fails, regardless of context.
8. The Bottom Line block runs immediately after the header, before
   section (a), with 3-5 bullets, each citing something concrete
   found in the body (a deal ID, a dimension + streak count, a
   section reference). A bullet that restates the header, hedges,
   or is generic enough to fit any week's run fails the run, even
   if every other criterion holds.
9. Voice bar held throughout: no unsupported adjectives ("significant,"
   "robust," "major," "strong") standing alone without a number, no
   hedging language, no filler phrasing ("it is important to note,"
   "moving forward"). A claim missing both a citation and a
   number-backed adjective fails on both counts.
10. Presentation layer (only built after PASS): the HTML report is
   generated from the passed draft, never an unpassed or flagged one.
   Every figure, quote, deal ID, account, and dimension in the report
   traces to the draft verbatim, with nothing added, dropped, or
   re-ranked in a way that changes meaning. Every UNAVAILABLE source
   shows an explicit unavailable state, never a zero or a blank. The
   report is one self-contained file (inline CSS and SVG) and holds the
   same no-em-dash bar. Any invented figure, dropped deal, or reordering
   that changes the story fails the run.
There is no "pass with caveat." If any criterion is unmet or
unverifiable, the run fails and the exact failing checks go to the
flags file.
