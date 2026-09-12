name: product-review-hardening
description: Runs the night before a product review. Attacks any
review-bound doc — PRD, one-pager, launch plan, strategy memo —
from four angles, files findings ranked by severity. PM fixes the
top ones before anyone else reads the doc.
---
## Attack angles
1. Unstated assumptions treated as facts
2. Edge cases with no specified behavior
3. Metrics without definition, source, or baseline
4. Questions engineering will ask that the doc doesn't answer

Angle assignment rule: a finding goes under the angle that best
describes WHO trips over it. Contradictions between the spec and a
shared component / Non-goals promise are engineering questions —
file them under Angle 4, in one finding, quoting BOTH sides of the
contradiction verbatim (never split one contradiction across angles
or quote only one side).

## Scope
Any doc headed into a product review: PRDs, one-pagers, launch
plans, strategy memos. The four attack angles apply unchanged; angle
4 covers whatever discipline will interrogate the doc (engineering
for specs, exec staff for strategy memos).

## Team context
- Recurring questions from the last five product reviews: "what exactly counts
  as the activation event?", "what's the rollback plan if the experiment
  hurts guardrails?", "does this touch shared components other teams own?"
- Engineering's known sore spots: migration cost for `workspace_settings`
  schema changes, feature-flag cleanup after ship/kill decisions, any
  change that quietly modifies the invite modal or integrations catalog.

## Drafts to harden
Current drafts live in data/product-review-hardening/ (paths
relative to the repo root, /Users/aakashgupta/Downloads/pm-loop-pack):
- guided-setup-draft.md (PRD)
- usage-alerts-launch-onepager.md (launch one-pager)
Harden the doc named in the invocation; default to the PRD if none
is named.

## Output format
- Never use an em dash (—) anywhere in the output. Use periods or
  commas or colons instead. This applies to the summary, every
  finding, and the top-fixes list.
- Immediately after the required STATE.md "Last run" header line (see
  State file section below), open the report with a **Bottom Line**
  section, before any findings: 3-5 bullets, each one dense sentence
  carrying three things: the single most important takeaway, why it
  matters to tomorrow's review, and a citation to specific evidence in
  the body below it (a finding ID, a section name, or a mechanically
  recomputed count, e.g. "3 of 5 blocks-review findings trace to the
  same undefined activation metric (1.1, 1.3, 3.2): this is the
  meeting-killer, not a wording nit"). Never restate the header. Never
  use filler that could paste into any run unchanged ("things look
  mostly fine," "continue monitoring"): a bullet that isn't
  falsifiable against this specific doc's findings doesn't belong
  here. This section comes before the per-angle findings.

Per finding: severity (blocks-review / weakens-review / minor),
section, quoted text, one-line suggested fix.
- "One-line" is literal: the fix is a single sentence, one action,
  no second sentence of rationale. If the rationale matters, fold it
  into the sentence or cut it.
- If a finding's quote touches anything adjacent to a Non-goals item,
  the finding itself must say inline why it is not a Non-goals
  violation (e.g., "questions feasibility of the promised as-is
  deep-link, not the rework decision"). Do not leave that distinction
  to a checker note a skimming reviewer will never see.
- Summary table: one row per severity with the count AND the finding
  IDs listed (e.g., "weakens-review | 11 (1.2, 1.3, ...)"). Counts
  must be recomputed mechanically from the filed findings (grep/count
  the finding headers, do not tally from memory) and must sum to the
  total number of findings in the document.
- End with a "Top fixes before review" list: 3-5 concrete next-hour
  actions the PM can execute tonight, each tied to a finding ID.

### Formatting bar
- Real markdown headers (##/###) for every section, not bolded prose
  standing in for a header.
- A table wherever the content is naturally tabular: the summary
  table, any before/after or multi-attribute comparison, any list of
  findings sharing more than two attributes.
- Bold the single most important figure or call in every section
  (e.g., **3 blocks-review**, **not ready for review**); bold is
  reserved for that one thing, not sprinkled through the prose.
- No walls of prose: a paragraph running past ~3 sentences gets
  broken into a list or table instead.

## Presentation layer
After the checker returns PASS, the maker generates a self-contained
HTML report from the passed markdown draft. The audited draft stays
the source of truth; the gate and checker apply to it in full. Never
render an unpassed or flagged draft as a polished page.

Follow `.claude/skills/_shared/report-style.md` for color, type,
layout, and components. Reference it; never redefine palette, scale,
or components locally.

Map this loop concretely:
- Header carries the hardened doc name, its type (PRD, one-pager,
  launch plan, strategy memo), and the review date; the run meta
  strip names the draft's source path and the green PASS badge, and
  renders the STATE.md "Last run" line verbatim from the output header.
- Bottom-line banner reproduces the draft's `## Bottom Line` bullets;
  the single biggest exposure renders first as a full-width crit
  banner naming the meeting-killer, the finding IDs it traces to, and
  what tomorrow's review breaks on. The one bolded figure (e.g.
  **not ready for review**) stays bolded.
- Stat tiles show gap counts by severity from the recomputed summary
  table: blocks-review / weakens-review / minor, plus a total tile.
  Each tile is a big tabular number over its uppercase severity label.
- Each hard question / gap renders as a card with a severity chip
  (● blocks-review = crit, ▲ weakens-review = warn, ✓ minor = good)
  and a matching left severity stripe, grouped under its attack angle.
- The main audited table is the findings table: one row per finding
  carrying the question or weakness (verbatim quoted text), why it
  bites (the angle / one-line consequence), the suggested answer or
  fix, and the owner. Every filed finding present, none reordered in a
  way that changes meaning; any not-a-Non-goals-violation note renders
  inline on its row.
- Owner + next-step line renders inline under each card from the
  "Top fixes before review" list, tied to its finding ID.
- Provenance footer names the draft source path and STATE.md, the run
  timestamp, checker PASS, and "Generated from the audited draft;
  every finding traces to source". Pattern-log references and
  promotion-eligible flags carry through verbatim.
- Any UNAVAILABLE source or missing count renders as an explicit
  muted UNAVAILABLE tile naming the source, never a blank or a zero.

Same rules as the draft: every claim, finding ID, count, quote, and
owner name traces to the passed draft verbatim; no invented gap and no
reordering that changes meaning; UNAVAILABLE stays explicit; one
self-contained file (inline CSS, inline SVG, no external assets); same
no-em-dash bar.

## State file
Read STATE.md in this skill folder before starting — it always
exists; NEVER claim the loop is stateless or that no state file is
present. Prove you read it by opening the output header with the
STATE.md "Last run" date and doc name. It holds the last run summary,
the pattern log, and lessons learned.
- Any finding matching a pattern in STATE.md's Pattern log (promoted
  or merely logged) must name that pattern and list its prior
  occurrences.
- A finding type appearing in its 3rd consecutive doc must be flagged
  in the finding as "promotion-eligible: promote to Team context",
  per the rule below.
- After a passing run, the CHECKER appends to STATE.md: date, doc
  name and type, findings count by severity, which angles hit. A run is not
  "passed" until that append is written — "checker: passed" with a
  stale STATE.md is a failed run.
A finding type that appears in 3 consecutive docs gets promoted into
the Team context section — it's not a finding anymore, it's a rule
your drafts should already follow.

## Known failure modes
(Write every mistake here the day it happens. This becomes the most
valuable part of the skill file.)
- 2026-06-30: Flagged "no rollback plan" on a doc that covered it in an
  appendix. Rule added: read appendices before filing angle-4 findings.
- 2026-07-02: Findings paraphrased the draft instead of quoting it
  verbatim, so authors couldn't Ctrl-F to the offending line. Rule:
  every finding's "quoted text" must be a verbatim substring of the
  draft. See STATE.md → Lessons learned.
- 2026-07-16: FALSE ENVIRONMENT CLAIM — a run asserted "no state file
  in this run (stateless loop)" while STATE.md existed and was
  mandatory reading. Rule: never assert a file is absent without a
  directory listing proving it; STATE.md in particular always exists
  and must be read and echoed (Last run line) in the output header.
- 2026-07-16: MISCOUNTED SUMMARY — the table said 10 weakens-review
  and "15 quotes verified" when the document contained 11 and 16.
  Rule: recompute all counts mechanically (count finding headers) and
  verify the table sums to the actual findings before writing it; the
  checker independently recounts and fails on any mismatch.
- 2026-07-16: CHECKER SELF-PASSED A NON-COMPLIANT RUN — it waived the
  pattern-reference criterion on a false premise and skipped the
  STATE.md append, yet printed "passed". Rule: the checker never
  waives a criterion; any state-rule violation or count mismatch is a
  hard FAIL written to round-N/flags/, never softened into a note.
- 2026-07-16: SKIPPED PATTERN REFERENCE — an undefined-activation
  finding failed to cite STATE.md's `undefined-activation-metric`
  pattern or flag it promotion-eligible on its 3rd consecutive doc.
  Rule: check every finding against the Pattern log before filing.
- 2026-07-16: MULTI-SENTENCE "one-line" FIXES — several suggested
  fixes ran 2-3 sentences. Rule: one sentence, one action, hard limit;
  the checker fails findings whose fix contains more than one sentence.
- 2026-07-16: CONTRADICTION SPLIT AND HALF-QUOTED — an invite-modal
  contradiction was filed under Angle 1 and quoted only one side.
  Rule: contradictions with shared components / Non-goals promises go
  under Angle 4 and quote both conflicting lines verbatim.
- 2026-07-17: VOICE/FORMAT UPGRADE — output used to read like a
  compliance checklist: flat finding lists, hedged language ("this
  might be a concern," "seems significant"), and a "Plain-language
  summary" that restated the verdict without citing anything a
  reviewer could check. Now it reads like a VP wrote it: the summary
  is **Bottom Line**, bullets only, each one citing a finding ID,
  section, or count from the body below it; MAKER.md carries a
  VP-of-Product voice bar (dense, cited, no hedges, no unsupported
  adjectives); SKILL.md carries a formatting bar (real headers, tables
  for tabular content, bold on the one number that matters per
  section). See Output format above and Checker criteria below.

## Checker criteria
The report opens with a **Bottom Line** section (3-5 bullets)
positioned before the first finding. Every bullet must cite something
concrete already in the body (a finding ID, a section name, or a
count) and that citation must actually resolve (the finding ID
exists, the count matches the checker's own recount, the section is
real); a missing section, a bullet with no resolvable citation, or a
bullet generic enough to paste into any run unchanged (e.g., "continue
monitoring," "overall in good shape") is a FAIL, not a note.
Every finding cites a section and quotes the draft verbatim (the quote
must appear character-for-character in the draft file). Findings that
match any pattern logged in STATE.md — promoted or not — reference it
by name; a 3rd-consecutive occurrence is flagged promotion-eligible.
Each suggested fix is exactly one sentence. Summary-table counts are
independently recounted by the checker and must match the filed
findings and sum to the total; any attestation ("N quotes verified")
must state the true N. The output header echoes STATE.md's Last run
line. Anything listed under the draft's Non-goals section is out of
scope and must not be filed as a finding; findings adjacent to a
Non-goal carry an inline not-a-violation note. A pass requires the
STATE.md run-summary append to be written; a run that violates any
state rule, miscounts, or claims STATE.md is absent MUST be failed to
round-N/flags/ — no waivers, no notes in lieu of a fail.
The HTML presentation report is generated only after the draft
passes. Every finding ID, count, quote, suggested fix, and owner name
in it reproduces from the passed draft verbatim, with nothing added,
dropped, or re-ranked, and no finding reordered in a way that changes
meaning; the severity tiles equal the checker's own recount. Any
UNAVAILABLE source renders as an explicit state naming the source,
never a blank or a fabricated value. The report is one self-contained
file (inline CSS and SVG, no external assets) and honors the
no-em-dash bar; a single em dash, an invented gap, or a page built
from an unpassed draft is a FAIL.
The output contains zero em dashes (—) anywhere; any instance is a
FAIL, no waivers.
