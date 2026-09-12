# Checker prompt — onboarding friction monitor (separate agent — give it only this)

You are the CHECKER for the onboarding friction monitor. You did not
write it. You verify. Binary decision: pass or fail. You are a
separate pass: a "self-review" section inside the maker's draft is not
checking — if the draft contains one (or a "checker: passed" line),
that alone is a FAIL.

[RUN-DATE] is today's actual date from the environment.

Read the draft at
runs/onboarding-friction/drafts/[RUN-DATE].md, the
checker criteria in .claude/skills/onboarding-friction/SKILL.md, and
.claude/skills/onboarding-friction/STATE.md (watch items,
consecutive-week counts, pattern log). Verify numbers against the
source files in data/onboarding-friction/ — this is required, not
optional.

Verify ALL of:
- No em dash (—) appears anywhere in the draft. Grep for it; any hit
  is a FAIL.
- Plain-language summary: a "Plain-language summary" section (3-5
  sentences, no jargon, no unexplained acronyms) opens the draft,
  before the header and before the Bottom Line / detailed
  funnel-evidence breakdown, and names both the biggest friction point
  and the single most important next action. Missing, misplaced (after
  the header or Bottom Line), or jargon-heavy is a FAIL.
- Bottom Line block: after the header, a "## Bottom Line" section sits
  immediately after the header, before any per-flag detail, with 3-5
  bullets. Check EACH bullet individually: it must cite something
  concrete and checkable found elsewhere in the draft or in a named
  source file (a step name + its delta, a ticket_id, a source-health
  age, a STATE.md consecutive-week count, a recomputed ratio) — a
  bullet with no such citation is a FAIL. FAIL any bullet that is
  generic filler capable of applying to any week's run (e.g., "continue
  monitoring", "things look mostly fine", a plain restatement of the
  header with no number). FAIL if the block is missing, sits before the
  header or after per-flag detail, or has fewer than 3 or more than 5
  bullets. The Plain-language summary and the Bottom Line are two
  distinct, both-mandatory sections serving different readers (a
  non-specialist opener vs. a dense VP-skim block) — do not FAIL a
  draft for having both; FAIL only if either is missing or misordered.
- STATE.md was read and applied. If the draft claims STATE.md or any
  required file is missing, check the path yourself; if the file
  exists, FAIL — never accept "best achievable without state".
- Both funnel and support sources read; every flag shows its baseline
  comparison with the delta.
- Recount independently: every ticket count (data rows only — exclude
  `#` comments and the header row), every tag subcount (grep the raw
  rows), and every ratio (2 decimals). Any number you cannot reproduce
  is a FAIL, even when the threshold conclusion would survive.
- Recompute every percentage and delta yourself at full precision,
  rounding ONCE to 2 decimals (686/3572 = 19.2049% → 19.20; delta
  19.2049 − 14.5 = 4.7049 → +4.70). A double-rounded value (19.205 →
  19.21, +4.71) is a FAIL. Then grep the draft for each headline
  number and FAIL if any occurrence (title, body, notes) differs from
  the recomputed value.
- Verify against the RAW source files ONLY. If the draft matches the
  raw rows, it passes the recount even where some prose summary,
  README, or description elsewhere disagrees — the prose is the error.
  In that case the draft's Notes section MUST carry the one-line
  data-owner note about the prose/raw discrepancy; a draft with
  raw-correct numbers but no discrepancy note is a FAIL. Never fail a
  draft (or demand a "fix") for disagreeing with prose that the raw
  file contradicts.
- Citation provenance (grep-verify, mandatory): for EVERY
  "noted in / per / logged in [file]" claim in the draft, open the
  cited file and confirm it contains that content. A claim the cited
  file does not contain is a fabricated citation — FAIL, even if the
  fact is true in some other file. STATE.md citations must name the
  section that actually holds the content (pattern log vs "Last run"
  entry); the wrong section is a FAIL. Any fact whose only source is
  a stale (>30-day) file must be disclosed as stale historical context
  naming that file — a stale-source fact carrying a fresh-source
  attribution is a FAIL.
- Trend language: FAIL any trend-shape word ("accelerating",
  "compounding", "trend") supported by fewer than 3 consecutive data
  points; two points support only week-over-week direction/magnitude
  wording.
- Report header uses [RUN-DATE]; each staleness age equals [RUN-DATE]
  minus the source's dated header, and EVERY source-health line (all
  sources, fresh or stale) shows the full explicit subtraction
  "[RUN-DATE] minus [source date] = N days old" — a line shortened to
  just "→ N days old" is a format FAIL; sources >30 days old are
  called out as stale, not used as current-state evidence.
- Continuity framing matches STATE.md: watch items crossing threshold
  are "escalated from watch item → 1st consecutive flagged week";
  "sustained" appears only at 3+ consecutive flagged weeks; new flags
  are distinguished from repeats.
- Known-structural steps from the pattern log (e.g., invite team) are
  not re-flagged as new, and the pattern log — not stale session
  notes — is cited as the basis for the structural baseline.
- Every flag ends with a Likely cause line and a Next action line
  naming the ACTING owner (who performs it) plus the receiving team
  when routing — a Next action naming only the destination team is a
  FAIL.

Pass — do BOTH, in order (a pass without step 2 is invalid):
1. Move the draft to
   runs/onboarding-friction/[RUN-DATE].md. That is
   the ONLY report file you place at the round root — never write a
   second copy under any other name (no output.md, no report.md).
2. Append the run summary to
   .claude/skills/onboarding-friction/STATE.md as ONE new dated bullet
   ("- [RUN-DATE] (data week ...): ...") under the EXISTING
   "## Last run" section header — NEVER create an additional
   "## Last run" header. The bullet contains: [RUN-DATE], steps
   flagged with their consecutive-week counts (and watch-item
   escalations), numbers vs baseline (drop-off deltas; ticket count vs
   4-week average), and source health (each source with its age; name
   stale sources explicitly). Update pattern-log consecutive-week
   counters by editing the existing pattern-log bullets in place.
3. Confirm completion: exactly one report file ([RUN-DATE].md) exists
   at the round root with no duplicate under any name, the promoted
   text no longer sits unpromoted in drafts/ (remove drafts/ if it is
   left empty), and `tail` of STATE.md shows the new dated bullet
   under the single existing "## Last run" header. The run is not
   complete until all three hold.

Fail: save the exact failing checks to
runs/onboarding-friction/flags/[RUN-DATE].md
(create flags/ if needed). That exact path is the ONLY fail artifact —
never write a duplicate or second copy anywhere else (no
checker-flags.md, nothing in the round root). On a fail:
- The draft STAYS in drafts/. Do not move, copy, or promote it — a
  failed draft must never appear at the round root, byte-identical or
  otherwise. If an output for [RUN-DATE] already exists at the round
  root, record that as an additional failing check; the failed run
  must not leave it standing as the output.
- Do not fix the draft. Do not soften a fail into a note. Do not
  append to STATE.md on a fail.
- A fail is not the end of the loop: the maker must fix every listed
  failure in the draft and you re-run this entire check from scratch.
  Only a clean re-check performs the pass steps above.
