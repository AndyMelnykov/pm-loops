# Product review hardening — state

## Last run
- 2026-07-17: "Guided Setup Checklist" PRD (guided-setup-draft.md), 8
  findings (2 blocks-review, 5 weakens-review, 1 minor). Angles hit:
  1, 2, 3, 4.

## Pattern log
- undefined-activation-metric: seen in "Referral rewards" (2026-05-20),
  "Usage-based alerts" (2026-07-02), and "Guided Setup Checklist"
  (2026-07-17). 3rd consecutive occurrence: promotion-eligible, promote
  to Team context.
- missing-rollback-plan: seen in "Usage-based alerts" (2026-07-02) and
  "Guided Setup Checklist" (2026-07-17). 2 consecutive occurrences, not
  yet promotion-eligible (promotes at 3).

## Lessons learned
- 2026-07-02: FAILURE MODE — the maker's findings paraphrased the draft
  ("the metrics section is vague about activation") instead of quoting
  it verbatim. Author couldn't locate the lines; the checker passed it
  anyway. Fix: checker now verifies every quote is a character-for-
  character substring of the draft. Rule added to SKILL.md → Known
  failure modes and Checker criteria.
- 2026-06-30: Flagged "no rollback plan" on a doc that covered it in an
  appendix. Rule: read appendices before filing angle-4 findings.
