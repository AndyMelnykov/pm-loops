# Sprint prep sweep — state

## Last run
- 2026-07-21 (Sprint 42 prep): 10 tickets swept, 6 findings across 4 tickets (3 blocks-planning findings on CORE-1799/1845/1847, plus a 4th blocks-planning finding on CORE-1799 for acceptance criteria, 2 fix-before-planning findings on CORE-1844/1846), 2 repeat offenders (CORE-1799, CORE-1843), 4 ready. Draft passed checker on first pass after the checker converted two quoted elements to labeled paraphrases (source text contained an em dash the new output style rule forbids reproducing verbatim).

## Repeat offenders
- CORE-1799, check: sized (estimate null). First failed 2026-07-07. 3rd consecutive sweep as of 2026-07-21. Owner: Tomás Rivera.
- CORE-1843, check: acceptance criteria present. First failed 2026-07-07. 3rd consecutive sweep as of 2026-07-21. Owner: Priya Raman.

## Lessons learned
- 2026-07-07: "AC: see spec" was accepted as acceptance criteria; the spec had none either. Rule added: a pointer is not criteria, verify testable statements exist in the field or the linked spec.
- 2026-07-07: CORE-1812 was checked but never listed, and the team assumed it was ready. Rule added: every export ticket appears in the report by ID; the checker reconciles counts.
- 2026-07-21: new output-quality rules (no em dash anywhere in the report, plain-language summary first) were added. First real run under them surfaced a conflict: two source fields in the backlog export contain an em dash inside the text being quoted. Rule added: when a verbatim quote would contain an em dash, drop the quotation marks, reproduce the content with the em dash replaced by a comma or period, and label it "(paraphrase)" rather than presenting an altered string as a verbatim quote.
