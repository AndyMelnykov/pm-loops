name: stale-doc-sweep
description: Runs monthly. Cross-references team docs against the
last 90 days of shipped changes, flags every doc section that
describes outdated behavior.
---
## Sources
- Docs to sweep: data/stale-doc-sweep/docs/ (all .md files)
- Ground truth: data/stale-doc-sweep/changelog.md (last 90 days)
- Current pricing: data/stale-doc-sweep/pricing-current.md

## Step 0 — state (MANDATORY, before anything else)
Read .claude/skills/stale-doc-sweep/STATE.md. This is not optional
and is never "not applicable": if the file exists, the run is
stateful. The report MUST open with a "State consulted" line naming
STATE.md's last-run date and the number of prior open flags. A report
that lacks this line, or that claims the loop is stateless, is an
automatic checker FAIL.

For every entry in STATE.md's pattern log, classify it in this run
(match by quoted claim, not section heading):
- RESOLVED — the doc has since been corrected. Report it in a
  "Resolved since last sweep" section with the fix date. Never
  silently drop it or fold it into "content matches".
- CARRIED-OVER (Nth consecutive sweep) — still stale, fewer than 3
  consecutive sweeps counting this one. Label it carried-over with
  first-flagged date and owner. Never present it as a fresh flag.
- CHRONIC — stale for 3+ consecutive sweeps counting this one
  (e.g., flagged in the 2 prior sweeps and still stale now = 3 =
  chronic). Escalate in a dedicated "Chronic, escalation" section
  with the owner named and an explicit escalation ask. Never
  re-list it as a new flag.

## Staleness test
A doc section is stale if it describes behavior the changelog
shows was changed, removed, or renamed. An old Last-updated date
alone is NOT staleness. Docs whose header marks them
"Evergreen — review annually" are policy-level and are exempt
from date-based suspicion; flag them only on a direct
changelog contradiction. Do not flag style, tone, or formatting.
Docs that match current changelog and pricing stay unflagged —
state the reason per doc in "Not flagged (and why)".

## Quotes and numbers
- Anything inside quotation marks must be verbatim from the source
  file, character for character (including "/user/mo" suffixes).
  If you shorten or reword, drop the quotation marks and label it
  "(paraphrase)". The checker diffs quotes against sources.
- Recompute every number (price, date, count) directly from
  changelog.md / pricing-current.md at report time and cite the
  source entry. Never carry a number from memory or a prior report.

## Owners and next-hour actions
- Every flag names an owner, taken from the doc header or STATE.md's
  pattern log. If genuinely absent from both, write
  "[owner unknown — check doc header]" — never omit the field.
- End the report with a "Next-hour actions" section: one line per
  open flag — owner, doc, the exact edit to make — so a reader can
  route every fix immediately.

## Writing style
- Never use an em dash (—) anywhere in the report. Use a period,
  comma, or colon instead. This applies to every section, including
  the plain-language summary, flag text, and paraphrases.

## Output format
Report sections, in order:
1. Plain-language summary (3-5 sentences, no jargon): the very first
   thing in the report, above everything else including the header.
   States how many stale docs were found, as a plain count, and the
   single most important thing the reader should do next. No loop
   jargon (no "chronic," "carried-over," "STATE.md," "gate"). Must be
   understandable to someone with zero context on this loop or the
   product.
2. Header: run date, docs swept count, sources used.
3. "Bottom Line" (3-5 bullets, cited): comes right after the header,
   before any detailed section. This is the citation-bearing summary
   for a reader who already knows the loop, distinct from the
   plain-language summary above it. Each bullet is one dense
   sentence: the single most important takeaway, why it matters, and
   a citation to the specific evidence for it further down in this
   same report (a doc path, a flag label, an owner name, a STATE.md
   sweep count, a recomputed figure). Never a restatement of the
   header. Never vague filler ("things look mostly fine," "continue
   monitoring").
4. State consulted: STATE.md last-run date + prior open flags count.
5. Resolved since last sweep (if any).
6. Chronic, escalation (if any): owner named, escalation ask.
7. Flags: per flag, status label (NEW or CARRIED-OVER, Nth sweep),
   doc path, verbatim quoted outdated claim, the contradicting
   changelog entry (verbatim quote or marked paraphrase), owner,
   suggested one-line fix.
8. Not flagged (and why): every unflagged doc with its reason.
9. Next-hour actions.
10. Checker verification (filled by checker, every criterion PASS or
    FAIL, "not applicable" is forbidden).

Formatting: real markdown headers (`##`) per section, not bolded
prose masquerading as a heading. Render a table wherever content is
naturally tabular, the flags list, the chronic-escalation list, the
resolved-vs-still-open comparison, never force a multi-attribute list
into paragraph sentences. Bold the single most important figure or
call in each section (an owner name, a sweep count, a price delta,
the total open-flag count). No walls of prose: if a section would
run past 3-4 lines of continuous text, restructure it as a table or
bullets instead.

## Presentation layer
After the checker returns PASS, and only then, the maker generates a
self-contained HTML report FROM the passed markdown draft. The draft
stays the audited source of truth; the gate and checker apply to it in
full. Never render an unpassed or flagged draft as a polished report.
Follow .claude/skills/_shared/report-style.md for color, type, layout,
and components; never redefine the palette, scale, or component kit
here.
Map this sweep concretely:
- Bottom-line banner: how many docs are stale and how many are
  critical (chronic or direct-contradiction), pulled verbatim from the
  Bottom Line and plain-language summary.
- Stat tiles: total docs scanned, stale count, critical count. A tile
  whose source is UNAVAILABLE shows the explicit unavailable state,
  never a zero.
- Each stale doc renders a severity chip and a left stripe, keyed by
  staleness severity (chronic or direct changelog contradiction =
  crit; carried-over = warn; new single flag = accent), matching the
  draft's flag disposition, never invented.
- Main audited table, every listed doc present, in draft order: doc
  path -> last updated / age -> why stale (verbatim quoted claim plus
  contradicting changelog entry) -> owner -> refresh or archive
  (the one-line fix / next-hour action).
- Provenance footer: source files, run timestamp, checker PASS, and
  "Generated from the audited draft; every figure traces to source."
Every doc, date, name, quote, and figure traces to the passed draft
verbatim. Invent no staleness and do no reordering that changes
meaning. UNAVAILABLE stays explicit. One self-contained file (inline
CSS and inline SVG, no external assets). Same no-em-dash bar as the
draft.

## State file
After the checker passes, append to STATE.md: run date, docs swept,
flags raised (new/carried/chronic), which prior flags are resolved,
and which remain unfixed with their consecutive-sweep counts. A run
is not complete until this append happens; the checker owns it and
must not stamp a pass without it.

## Known failure modes
(Write every mistake here the day it happens. This becomes the most
valuable part of the skill file.)
- 2026-06-01: new-hire-faq.md was reorganized; old section anchors
  moved. Match flags by quoted claim, not by section heading, for
  2 sweeps.
- 2026-07-16: STATE.md was never read; the report claimed the loop
  was stateless. Rule: Step 0 is mandatory; a missing "State
  consulted" line is an automatic checker FAIL.
- 2026-07-16: reporting-guide.md "Export CSV button" hit its 3rd
  consecutive sweep but was re-listed as a fresh flag instead of
  being escalated as chronic with owner Miguel Torres named. Rule:
  count consecutive sweeps including the current one; 3+ = chronic
  escalation section with owner.
- 2026-07-16: support-playbook.md's prior "Inbox Rules" flag had
  been fixed but was silently folded into "content matches" instead
  of being reported as RESOLVED. Rule: every prior open flag gets an
  explicit resolved/carried/chronic disposition.
- 2026-07-16: onboarding-guide.md's Growth-plan flag (2nd
  consecutive sweep, owner Priya Raman) was presented as brand-new
  with no history or owner. Rule: label carry-overs with sweep count,
  first-flagged date, and owner.
- 2026-07-16: checker stamped "passed" while waving the chronic-
  escalation criterion off as "not applicable". Rule: every checker
  criterion is answered PASS or FAIL against evidence; "not
  applicable" is forbidden; any FAIL fails the draft.
- 2026-07-16: STATE.md was not appended after the claimed pass. Rule:
  the append is part of the pass — no append, no pass.
- 2026-07-16: a shortened changelog line ("Starter ($29), Pro ($59),
  Scale ($119)") was presented inside quotation marks; the actual
  entry reads "Starter ($29/user/mo), Pro ($59/user/mo), Scale
  ($119/user/mo)". Rule: quotes are verbatim or marked "(paraphrase)".
- 2026-07-16: no owners were named anywhere in the report even
  though doc headers and STATE.md list them. Rule: owner is a
  required field on every flag and every next-hour action.
- 2026-07-17: reports were accurate but read like a compliance
  checklist, no section a VP could scan in 15 seconds, adjectives
  ("significant," "robust") standing in for numbers, multi-attribute
  flag lists buried in prose paragraphs. Now: every report opens
  with a "Bottom Line" (3-5 cited-takeaway bullets) before any
  detail; every claim in the body carries a specific citation and
  zero unsupported adjectives; tabular content (flags, chronic list,
  resolved list) renders as a markdown table with the key figure
  bolded, not a paragraph.

## Checker criteria
Answer each with PASS or FAIL plus one line of evidence. "Not
applicable" is forbidden. Any FAIL fails the draft.
1. Report contains a "State consulted" line citing STATE.md's
   last-run date; STATE.md was actually read.
2. Every STATE.md pattern-log entry has an explicit disposition in
   the report: RESOLVED, CARRIED-OVER (Nth sweep), or CHRONIC.
   Recompute sweep counts from STATE.md yourself — 3+ consecutive
   sweeps counting this run = must be in the chronic escalation
   section with owner named, not listed as new.
3. Previously flagged docs since corrected are reported as resolved,
   not re-flagged and not silently dropped.
4. Every flag pairs a quoted doc claim with a changelog or pricing
   entry; every quotation-marked string is verbatim in its source
   (spot-check by searching the source file); paraphrases are
   labeled.
5. No flags based on style, tone, or Last-updated date alone;
   evergreen-headed docs flagged only on direct contradiction.
6. Every flag and every next-hour action names an owner.
7. "Next-hour actions" section exists and covers every open flag.
8. On pass, STATE.md is appended (date, docs swept, flags raised,
   resolved, still-unfixed with sweep counts) before "checker:
   passed" is written.
9. The report opens with a "Bottom Line" section immediately after
   the header, before every other section, with 3-5 bullets. Every
   bullet names a citation to something concrete elsewhere in the
   draft (a doc path, a flag label, an owner, a STATE.md sweep
   count, a recomputed figure), spot-check each cited fact against
   the body. Reject if any bullet restates the header, hedges with
   filler ("things look mostly fine," "continue monitoring"), or is
   generic enough to paste unchanged into next month's report.
10. The report opens with a plain-language summary (3-5 sentences,
    no jargon), above the header and above the "Bottom Line" section.
    It states the count of stale docs found and the single most
    important next action, in language a reader with zero context on
    this loop or the product could understand. Reject if it uses loop
    jargon (e.g. "chronic," "carried-over," "STATE.md," "gate"), if
    it's outside the 3-5 sentence range, or if it's missing the count
    or the single most important action.
11. No em dash (—) appears anywhere in the report. Scan the whole
    draft, including the plain-language summary, Bottom Line, flags,
    and paraphrases. Any em dash is a FAIL regardless of context.
12. If an HTML presentation report was generated, it was built only
    after this PASS and every doc, date, owner, quote, and figure in
    it traces verbatim to the passed draft, with nothing added,
    dropped, or re-ranked and no severity chip that contradicts the
    draft's disposition. Any UNAVAILABLE source shows an explicit
    unavailable state, never a zero or blank. The file is fully
    self-contained (inline CSS and SVG, no external assets) and
    carries no em dash. Reject the report if any check fails; the
    markdown draft remains the audited source of truth.
