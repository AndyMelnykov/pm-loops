name: feedback-digest
description: Runs every Friday. Reads the week's feedback from all
sources, tags each item against the theme taxonomy, ranks themes by
week-over-week growth against STATE.md, files a one-page digest.
---
## Sources
Paths are relative to the repo root (/Users/aakashgupta/Downloads/pm-loop-pack).
For the week ending 2026-07-17:
- Support tickets: data/feedback-digest/support-tickets-2026-07-17.csv
- Sales notes: data/feedback-digest/sales-notes/2026-07-17.md
- App reviews: data/feedback-digest/app-reviews-2026-07-17.csv
- NPS verbatims: data/feedback-digest/nps-verbatims-2026-07-17.csv
- User-interview notes: data/feedback-digest/interview-notes/ (every
  file in the directory; each file is one interview with one customer)

## Theme taxonomy
Fixed list. Do not invent new themes; anything that fits none goes to "unclustered."
1. **Permissions & roles confusion** — users can't understand, configure, or trust roles/permissions: unclear role definitions, wrong access granted or denied, missing viewer/audit capabilities, role-mapping blockers.
2. **Dashboard performance** — dashboards, reports, or analytics pages loading slowly or timing out.
3. **Export & reporting issues** — CSV/Excel/PDF/API exports broken, truncated, missing columns, corrupted, or scheduled exports failing.
4. **Mobile app crashes** — the iOS/Android app crashing or force-closing.
5. **Billing & invoicing errors** — wrong charges, duplicate invoices, VAT/tax mistakes, missing receipts, seat-count billing errors.
6. **Onboarding friction** — new customers struggling with setup, import, invites, or the setup wizard.

## Counting rule
One mention per customer per theme per week, across all sources
combined. One loud customer cannot fake a trend. Interview quotes
are tagged against the same taxonomy and counted the same way — an
hour-long interview is one customer, not ten mentions.
- CSV totals exclude the header row. Total items = data rows only.
- When stating how many items a single customer filed, enumerate the
  item IDs (e.g., ticket numbers) and count the enumeration — never
  eyeball it. The count you publish must equal the number of IDs you
  can list.

## Growth ranking rule
Rank themes by week-over-week growth, never by raw volume.
- Baseline = last week's per-theme counts in STATE.md (most recent
  entry under "Last run").
- growth % = (this week − last week) / last week, rounded to the
  nearest whole percent. Show the arithmetic as "last→this (+X%)".
- Top 3 = the three themes with the highest growth %. Break ties by
  this-week count. A high-volume theme with low growth does not
  belong in the top 3.
- Ordinals: before writing any "ranked Nth by growth" claim, sort
  all six growth percentages descending and count the position —
  never eyeball it. A positive growth % always outranks 0%, and 0%
  outranks any decline. Write the sorted order in your working notes
  and check every ordinal in the digest against it.

## State file (mandatory, first read of every run)
STATE.md lives in this skill folder
(.claude/skills/feedback-digest/STATE.md) and ALWAYS exists — it is
pre-seeded with prior weeks. Open it before touching any source file
and transcribe last week's six theme counts and the pattern log into
your working notes. Never write "no state carried over" or "no
pattern log exists"; if you cannot read STATE.md, stop and flag the
run — do not file a volume-ranked digest as a fallback.

Trust the numbers, re-derive the prose: STATE.md's counts, streak
dates, and growth figures are authoritative, but any narrative claim
in a prior entry (e.g., "ranked 5th by growth") must be re-derived
from the recorded counts before you repeat it. If a prior entry's
prose conflicts with recomputation, use the recomputed value and
note the discrepancy in the digest — never propagate a prior wording
error forward.

Pattern log rules:
- A theme in the top 3 by growth for 3 consecutive weeks (including
  this run) MUST be called out as a **sustained shift** in the
  digest.
- A theme at 2 consecutive weeks is logged as **watch next week** —
  do not call it sustained.
- After a passing run, the checker appends: date, all six theme
  counts, top growers with growth %, unclustered count, source
  health, and updates each theme's streak in the pattern log. Every
  number and ordinal the checker writes into STATE.md must be its
  own recomputation, never copied from the draft's prose — a wrong
  value written here misleads every future run.

## Output format (exact — the checker verifies each element)
Formatting bar (applies throughout, not just the Bottom Line): real
markdown headers (##/###) for every section — never bold text
standing in for a heading. A markdown table wherever content is
naturally tabular (comparisons, multi-attribute lists, before/after
values) — the full theme table is mandatory, and the sources-read
line renders as a table once there are 3+ sources. Bold the single
most important figure or call in each section (the growth % in a
top-3 heading, the header's total item count, the WoW figure that
matters most in the table row). No walls of prose — 3 sentences per
paragraph, max; prefer bullets.

1. Header: "Weekly Feedback Digest — week ending YYYY-MM-DD" plus a
   sources-read line with per-source item counts (header rows
   excluded).
2. **Bottom Line** — the mandatory synthesis block. Comes immediately
   after the header, before any detailed section: 3-5 bullets, each
   one dense sentence carrying the single most important takeaway,
   why it matters to the business, and a citation back to specific
   evidence in the body below (a theme + growth %, a source ID, a
   table figure, an Owner). Write it last, after the sections in
   points 3-6 below are drafted, using only numbers and citations
   that already exist in the draft. Never a restatement of the
   header. Never generic filler ("things look mostly fine", "continue
   monitoring") that could describe any week's run. A VP should get
   the whole picture from this block alone in 15 seconds.
3. **Top 3 themes by week-over-week growth.** Each heading reads:
   "N. Theme, last to this unique customers (+X%)". Under each:
   2 verbatim quotes with customer name and source ID (interview
   quotes are eligible, cited per the citation format), then one
   "This week:" action line and an "Owner:" line. The action line
   is a concrete, PM-actionable next step someone can start this
   week, not a restatement of what users said (e.g., "Eng: pull
   traces for /api/v2/dashboard/summary and confirm whether the
   6-widget threshold in TK-88278 is the trigger" is actionable;
   "users are frustrated with dashboard speed" is not, and fails).
   The owner line names a specific team implied by the cited
   evidence (Eng, Support, Docs, Sales/CS, Billing, Design), never
   left blank and never "PM" alone unless no other team is implied.
4. **Sustained shifts** section: name any theme at 3+ consecutive
   weeks in top-3 growth as a sustained shift, list 2-week themes as
   watch-next-week, or state "none", always checked against
   STATE.md's pattern log. Each sustained-shift or watch call also
   gets an "Owner:" line naming the team that should carry it.
5. **Full theme table** with columns: Theme | This week | Last week
   | WoW growth | Customers. All six themes, last-week counts from
   STATE.md, growth % for every theme (including declines, e.g.
   -17%).
6. **Unclustered** list with source IDs and why each fits no theme.
7. **Coverage is total**: every source item must appear in exactly
   one of: a theme count, the unclustered list, or a one-line
   "Omitted:" note giving the item's citation and the reason (e.g.,
   "roadmap already communicated, no issue raised"). Silent
   omissions are a coverage failure even when omission itself is
   justified: tagged + unclustered + omitted must reconcile to the
   per-source totals.

## Presentation layer
After the checker returns PASS, the maker generates a self-contained
HTML report FROM the passed markdown draft. The draft stays the
audited source of truth; the gate and checker apply to it in full.
Never render an unpassed or flagged draft as a report.
- Follow .claude/skills/_shared/report-style.md for all color, type,
  layout, and components. Do not restate the palette here.
- Report header: eyebrow "feedback-digest" plus week-ending date, H1
  "Weekly Feedback Digest", run-meta strip listing the sources read
  and a green PASS badge.
- Bottom Line banner at the top of the body: the draft's Bottom Line
  bullets, with the single most important growth % or figure bolded.
- Stat tiles row: total items this week, per-source item counts, and
  the unclustered count, each a KPI tile with tabular number. A source
  that came back UNAVAILABLE shows the muted UNAVAILABLE tile naming
  that source, never a zero.
- Each top-3 theme renders as a card with a severity chip colored by
  growth direction (rising = warn/crit, flat = neutral) and a left
  severity stripe: heading "N. Theme, last to this (+X%)", the WoW
  delta shown with sign and an inline sparkline where a series exists.
- The full six-theme table is the audited data table: Theme | This
  week | Last week | WoW growth | Customers, every row present, growth
  shown for declines too, numeric columns right-aligned tabular-nums.
- The 2 verbatim quotes per theme render as blockquotes inside that
  theme's card, each with its inline customer name and source ID.
- The "This week" action and "Owner:" team render as the owner +
  next-step line under each theme card; sustained-shift and watch
  calls render with their owner line and a run-count counter chip.
- Unclustered and any "Omitted:" notes render with their source IDs
  above the provenance footer, which carries source files, run
  timestamp, checker PASS, and "every figure traces to source."
- Every figure, quote, and name traces to the passed draft verbatim.
  Add no data, drop nothing, reorder nothing that changes meaning.
  UNAVAILABLE stays explicit. One self-contained file, inline CSS and
  SVG, and the same no-em-dash bar as the draft.

## Citation format (traceability rule)
Every piece of feedback the digest cites, quotes, paraphrases, or
otherwise attributes to a customer must carry an inline identifier
the reader can actually follow up on: a ticket/review/NPS ID, or a
sales-note/interview-note file path plus location. A bare paraphrase
with no identifier ("several customers mentioned slow dashboards")
is not a citation and fails, even in prose outside the quote blocks
(e.g., the theme narrative, the sustained-shifts section, the
"This week" action lines). If an action line references specific
evidence (a ticket, a customer, a piece of data), name the
identifier inline next to that reference.
- Items with IDs (tickets TK-, reviews AR-, NPS-) are cited by ID.
- Sales notes have no IDs: cite the file plus the entry, e.g.
  "(sales-notes/2026-07-17.md, Wed 7/15 entry)", never a bare
  "(Wed 7/15)", so the checker can locate the item deterministically.
- Interview notes have no IDs either: cite the file plus the section,
  e.g. "(interview-notes/2026-07-14-kestrel-insurance.md, Permissions
  section)", never just the customer name.
- Pseudonymous review quotes: attribute as "App Store review
  (AR-xxxx), Customer Name", never present a reviewer handle as if
  it were a person's name.

## Style rule: no em dashes
Never use an em dash (—) anywhere in the output, including headings,
quotes' surrounding prose, action lines, and STATE.md updates. Use a
period, comma, or colon instead. This is a hard formatting rule, not
a style preference: an em dash anywhere in the draft fails the run.
(Verbatim quotes pulled from source text are exempt only if the
source text itself contains one; do not alter a verbatim quote to
remove it, but do not introduce new em dashes in your own prose.)

## Dedupe claims
- A customer may be listed as a cross-source duplicate ONLY if you
  can point to their items in 2+ distinct sources. Before adding a
  name to any dedupe note, record the specific row/entry in each
  source in your working notes. A customer appearing in exactly one
  source is never a duplicate, no matter how it "feels".

## Accuracy rules
- Every number in the digest is recomputed from raw rows before
  filing; recount once more during a final self-verification pass.
- Quotes are verbatim, with correct source IDs.
- No embellishment: do not attribute deadlines, app versions,
  severities, or any fact to a customer unless that customer's own
  item states it. If only 4 of 5 customers cite a version, say "4 of
  5 cite 4.12.1", not "all on 4.12.x".
- No unsupported adjectives: "significant", "robust", "notable",
  "meaningful", and similar get cut unless a number immediately
  follows that earns them. A number, or nothing.
- The maker never writes a checker verdict or "self-review passed"
  into the draft. Verdicts belong to the checker alone.

## Known failure modes
(Write every mistake here the day it happens.)
- 2026-06-19: sales notes folder was empty because the week rolled over Saturday, not Friday. Check both week files when Friday is month-end.
- 2026-06-26: counted one enterprise customer's 5 tickets as 5 mentions and it distorted the ranking. The counting rule exists for a reason — dedupe by customer before counting.
- 2026-07-17: a run claimed "no prior-week counts were available (no state carried over)" without ever opening STATE.md, then ranked by raw volume and missed a 3-week sustained shift. STATE.md always exists — open it first, paste last week's counts into the draft, and rank by growth only.
- 2026-07-17: off-by-one twice — a customer's ticket count was published as 7 when listing the IDs shows 8, and the CSV header row was counted in the total (said 42 tickets; the file has 41 data rows). Enumerate IDs to count per-customer items; subtract the header from file totals.
- 2026-07-17: embellished cited items — added a deadline the ticket never stated and generalized an app version to customers whose items didn't mention it. Only state what the source text says, per item.
- 2026-07-17: checker declared "passed (with caveat)" while two hard criteria were unmet, then skipped filing weekly-*.md and appending to STATE.md. The verdict is binary; a caveat on an unmet criterion is a fail, and the pass-path file/state actions are contractual.
- 2026-07-17: wrote "ranked 5th by growth (+11%)" when sorting the six growth values (+120/+75/+67/+11/0/−17) puts that theme 4th — +11% beats 0%. Worse, the wrong ordinal was then appended to STATE.md's pattern log, poisoning future baselines. Derive every ordinal from the sorted growth list, and never repeat a prior entry's narrative ordinal without re-deriving it from the recorded counts.
- 2026-07-17: dedupe note listed a customer as a cross-source duplicate who appeared in exactly one source (a single NPS verbatim — no ticket, review, or sales note). Every name in a dedupe list must be backed by located items in 2+ distinct sources.
- 2026-07-17: a sales-note item was silently omitted (an ask already on the communicated roadmap) with no trace in the digest. Justified omissions still need a one-line "Omitted:" note with citation and reason so item-level coverage is auditable.
- 2026-07-17: sloppy citations — a sales-note item cited as a bare "(Wed 7/15)" instead of the file + entry, and a review quote attributed to the reviewer's handle as if it were a person's name. Follow the citation-format section exactly.
- 2026-07-17: voice/format upgrade — the digest used to read like a competent analyst's log: correct counts, no synthesis up top, prose-heavy sections, unsupported adjectives ("significant delays") with no number attached, bold used in place of real headers. Added the mandatory Bottom Line block (3-5 cited, dense bullets, first thing after the header), a VP-of-Product voice bar (no filler, no hedges, every adjective needs a number or gets cut), and a stronger formatting bar (real markdown headers, tables wherever content is tabular, bold on the one figure that matters per section). The output now reads like a VP of Product wrote it, not a checklist a summarizer filled in.
- 2026-07-17: a digest passed with action lines that just restated the complaint ("dashboard is slow, investigate") with no owning team and no next step a PM could hand off, and one prose sentence cited "several customers" with no IDs at all. Action lines must be concrete and owned; every attribution to a customer needs an inline identifier, not just the quote blocks.

## Checker criteria (binary — ALL must hold or the run fails)
1. Every source read — including every file in the interview-notes
   directory; per-source counts match the raw files (header rows
   excluded).
2. **Bottom Line** block exists as the first section after the
   header, before any detailed section, with 3-5 bullets. Every
   bullet cites something concrete found in the body below (a theme
   + growth %, a source ID, a table figure, an Owner) — a bullet
   that only restates the header, or that is generic filler
   ("continue monitoring", "things look mostly fine") generic enough
   to apply to any week's run, fails the block.
3. Every item tagged to a taxonomy theme, listed as unclustered, or
   covered by an explicit "Omitted:" note with citation and reason;
   tagged + unclustered + omitted reconciles to per-source totals.
   Silent omissions fail.
4. Counts respect the one-mention-per-customer rule, and every
   customer named as a cross-source duplicate verifiably appears in
   2+ distinct sources — the checker locates each named customer's
   items; one single-source name in the dedupe list fails.
5. Growth ranks computed against last week's counts in STATE.md —
   the checker opens STATE.md itself, re-derives the top 3, and
   verifies every "ranked Nth by growth" ordinal in the digest
   against its own sorted growth order.
6. Sustained shifts / watch calls match STATE.md's pattern log, and
   each sustained/watch call has an owning team.
7. Full theme table shows this-week, last-week, and growth % for all
   six themes; top-3 headings show growth %.
8. Each top-3 theme has 2 verbatim quotes with correct IDs, a
   concrete "This week" action tied to the cited evidence (not a
   restatement of the complaint), and a named "Owner:" team;
   citations follow the citation-format section (sales notes cited
   as file + entry, review quotes attributed as "App Store review
   (AR-xxxx), Customer Name", not a handle).
9. No unsupported claims (spot-check deadlines, versions, ARR
   figures against source text) and no unsupported adjectives
   ("significant", "robust", and similar without a number attached).
10. Every attribution to a customer anywhere in the draft, not just
    inside quote blocks, carries a traceable inline identifier (ID,
    or file + entry/section). A bare paraphrase with no identifier
    fails the run.
11. No em dash (—) appears anywhere in the draft's own prose (quotes
    verbatim from source text are exempt if the source itself has
    one).
12. Formatting bar: real markdown headers throughout (no bold
    standing in for a heading), the full theme table rendered as an
    actual markdown table, the single most important figure or call
    in each section bolded, no wall-of-prose paragraphs (4+ sentences
    with no headers or bullets).
13. Presentation layer: any HTML report is generated only after this
    run PASSes. Every figure, quote, theme, and flag in the HTML
    reproduces from the passed draft with nothing added, dropped, or
    re-ranked, and no theme reordered against the draft's growth
    order. Any UNAVAILABLE source stays explicit as an UNAVAILABLE
    tile, never a zero. The file is fully self-contained (inline CSS
    and SVG, no external assets) and honors the same no-em-dash bar.
There is no "pass with caveat." If any criterion is unmet or
unverifiable, the run fails and the exact failing checks go to the
flags file.
