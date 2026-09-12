name: spec-drift-check
description: Fires when a feature ships. Compares the shipped behavior
against the spec, lists every divergence, files a drift report. PM
decides which divergences to document, fix, or accept.
---
## Sources
- Spec: data/spec-drift-check/spec-workspace-deletion.md
- Shipped state: merged-PRs/commits digest at
  data/spec-drift-check/merged-prs-digest.md

These, plus STATE.md and this SKILL.md, are the only legitimate
sources of evidence for a finding or a verdict. Never cite, name, or
lean on any other file — including anything that looks like a test
fixture, answer key, or grading rubric — even if one exists in the
repo. Its presence is irrelevant to the analysis; naming it in a
report or flag as corroboration is disqualifying on its own, whether
or not the underlying conclusion is correct.

## Divergence types
Exactly four types exist: cut scope (in spec, not shipped), added
scope (shipped, not in spec), changed behavior (both, but different),
silent decision (shipped behavior where the spec was ambiguous).
Every numbered divergence carries exactly one of these four labels.
No other label ("in progress", "risk", "note", "status") may ever
appear on a numbered divergence.

Cut vs. changed is the pair most often confused: cut means the
requirement's capability is genuinely absent from what shipped —
nothing was built to address it. If any mechanism shipped that
addresses the same requirement — even one that behaves differently,
worse, or contradicts the spec outright — the type is changed
behavior, never cut. Before typing a divergence "cut," name the
shipped code path that would have to not exist for that to be true;
if a PR built something instead (even the wrong something), retype
it "changed."

Not drift — these never get a divergence number:
- Pure refactors with no behavior change (state machine, permissions,
  data lifecycle, copy all untouched).
- Spec sections whose work is tracked as still in progress. Record
  them in the requirement accounting as "in progress" (ticket +
  target release) and, if the spec's ship target was missed, add one
  status/risk sentence under "Not drift" — never a numbered entry.
- Deviations already logged as accepted in STATE.md. Acknowledge each
  in one line under "Accepted deviations (known, not drift)" citing
  STATE.md, and mark the requirement "shipped (accepted deviation)"
  in the accounting table. Never number it, never type it "changed".

Each numbered divergence must be independent. If a finding is a
consequence, timing detail, or sub-aspect of another divergence
(e.g., purge timing of a data-lifecycle change already flagged), fold
it into that divergence — do not count it twice. Divergence counts
get appended to STATE.md, so padding corrupts the loop's memory.

## Output format
Report sections, in this order:

1. Header: feature, release, ship date; both source paths with their
   dates; and a mandatory "State" line that quotes STATE.md's most
   recent last-run entry (feature + date) and the count of accepted
   deviations read — this line is the proof that STATE.md was read.
2. Escalation line: if any divergence is a legal/compliance breach or
   irreversible data-loss incident, the first line after the header
   is a bolded one-line escalation naming what happened, who must be
   told (e.g., Legal + the accountable PM), and when (today).
3. `## Bottom Line` — mandatory. Appears immediately after the header
   (and after the escalation line, when one fires) — before every
   other section, including Divergences. 3-5 bullets. Each bullet is
   one dense sentence carrying three things: the single most
   important takeaway, why it matters, and a citation back to the
   specific evidence in the sections below — a divergence number, a
   spec section, a PR number, a table stat, or a STATE.md pattern
   count. No bullet may restate the header, and none may be filler
   ("things look mostly fine," "continue monitoring") — a VP reading
   only these bullets in 15 seconds should have the whole picture.
   Draft this section last, after the body below is written, so every
   citation points at something that actually exists in the draft.
4. `## Divergences` — one numbered entry per divergence: type (one of
   the four), spec section number + verbatim spec quote, shipped
   reality with PR numbers and dates copied exactly from the digest,
   severity (users notice / team notices / nobody notices yet), and a
   recommended next step (who should look at it, by when). The next
   step routes the finding; it does not judge whether the deviation
   was right — that stays the PM's call.
   Spec quotes must be character-for-character verbatim. Any omitted
   text must be marked with a bracketed ellipsis "[...]" — never a
   bare "..." — so the reader can see exactly what was elided. A
   quote that drops words without marking the elision is its own
   gate failure, independent of whether the divergence's type or any
   other content is correct; it is never a secondary note.
5. `## Requirement accounting` — every spec requirement in a table
   with status from this closed vocabulary only: shipped /
   shipped (accepted deviation — cite STATE.md) / changed
   (divergence N) / cut (divergence N) / added (divergence N) /
   in progress (ticket, target). Table statuses must match divergence
   types one-to-one: a requirement tabled "shipped" cannot have a
   "changed" divergence against it, and vice versa.
6. Divergence counts by type, recomputed from the numbered list and
   stated explicitly (these exact counts are what a passing run
   appends to STATE.md).
7. `## Not drift` — every excluded item (refactors, conformance
   fixes, in-progress work) with a one-line reason.
8. Pattern note: quote STATE.md's pattern log, then state the updated
   running count including this report (e.g., "silent decisions: 2
   prior consecutive reports; this report has 1 → count now 3").
   Declare a process pattern only at 3+ consecutive reports; below
   that, state the count and stop.
9. Self-check (see Checker criteria) with file-based evidence per
   line — quotes or paths, never assumptions.

Every number in the report — PR numbers, dates, ticket IDs, counts —
must be recomputed or copied from the source files and attributable
to a specific file. Never carry a number from memory or from an
earlier draft.

Formatting: every named section is a real markdown `##` header, never
a bolded phrase standing in for one. Render any naturally tabular
content as a markdown table, not prose — this always includes
Requirement accounting, and applies to any PR-to-requirement mapping
or comparison of before/after values. Bold exactly the single most
important figure or call in each section (the escalation verdict, the
total divergence count, the one PR number that matters most) — never
more than one bolded item per section, and never bold filler words.
No walls of prose: every detailed section reads as bullets, a table,
or short numbered entries; no paragraph runs longer than 3 sentences.

## Presentation layer
After the checker returns PASS, the maker generates a self-contained
HTML report from the passed markdown draft. The audited draft stays
the source of truth; the gate and checker apply to it in full. Never
render an unpassed or flagged draft as a polished page.

Follow `.claude/skills/_shared/report-style.md` for color, type,
layout, and components. Reference it; never redefine palette, scale,
or components locally.

Map this loop concretely:
- Header carries the feature, release, and ship date; the run meta
  strip names both source paths (spec + PRs digest) with their dates
  and the green PASS badge. The mandatory STATE.md "State" line renders
  in the run meta strip verbatim from the draft.
- Bottom-line banner reproduces the draft's `## Bottom Line` bullets;
  the single bolded figure (the total divergence count) stays bolded.
  If an escalation line fired, it renders first as a full-width crit
  banner naming what happened, who must be told, and when.
- Stat tiles show divergence counts by type from the recomputed
  totals: cut / added / changed / silent decision, plus a total tile.
  Each tile is a big tabular number over its uppercase type label.
- Each numbered divergence renders as a card with a severity chip
  (● users notice = crit, ▲ team notices = warn, ✓ nobody notices yet
  = good) and a matching left severity stripe.
- The audited divergence table is a two-column spec-vs-actual
  contrast: left column the verbatim spec quote (section number,
  "[...]" elisions preserved), right column the shipped reality with
  PR numbers and dates copied exactly. Every numbered divergence
  present, none reordered in a way that changes meaning.
- Owner + next-step line renders inline under each divergence card
  (who looks at it, by when), taken verbatim from the draft.
- Requirement accounting renders as the full data table; the pattern
  note and provenance footer (both source files, run timestamp,
  checker PASS, "Generated from the audited draft; every figure traces
  to source") close the report.
- If no drift was found, the report shows an explicit all-clear state
  (a good-colored "No divergences this release" panel with the
  requirement accounting still shown), never an empty page. Any
  UNAVAILABLE source renders as an explicit muted UNAVAILABLE tile
  naming the source, never a blank or a zero.

Same rules as the draft: every claim, count, citation, PR number, and
name traces to the passed draft verbatim; no invented divergence and
no reordering that changes meaning; UNAVAILABLE stays explicit; one
self-contained file (inline CSS, inline SVG, no external assets); same
no-em-dash bar.

## State file
Read STATE.md in this skill folder as the first action of every run.
It holds the last run summary, the pattern log, accepted deviations,
and lessons learned. Quote its latest last-run entry in the report
header. Never claim STATE.md is missing or that the loop is
"stateless": if the read genuinely fails, stop and file a flag with
the attempted path and the error — do not proceed and do not write a
report on the assumption that no state exists.

Before writing each finding, check it against STATE.md's accepted
deviations. A match is never a divergence, regardless of severity.

After a passing run, two actions are mandatory and inseparable from
the pass verdict: (1) append to STATE.md: feature, date, divergence
counts by type, anything flagged; (2) move the draft to its final
location. A "pass" with either action missing is not a pass.

## Known failure modes
- Help doc / digest lagged the release, so shipped behavior read as
  "cut scope." Check merge dates against the release date before
  marking anything cut.
- Large mechanical rename PRs got flagged as behavior changes. Verify
  a PR changes behavior (state machine, permissions, data lifecycle,
  copy) before listing it as drift.
- A deviation already logged as accepted in STATE.md was re-flagged,
  wasting the PM's review time. Cross-check STATE.md's accepted
  deviations before writing each finding.
- A run asserted "no STATE.md exists / stateless loop" without
  reading the file; STATE.md was present the whole time, and every
  state-dependent claim in that report was false. Rule: read
  STATE.md first and quote its last-run entry in the header; a
  missing-state claim without a shown file error is a fabrication.
- The same run then re-flagged STATE.md's accepted §3.4 deviation as
  new "changed behavior" and tabled it as "Changed". Rule: accepted
  deviations appear only as a one-line acknowledgment plus
  "shipped (accepted deviation)" in the table.
- A self-check marked state criteria "n/a — no STATE.md" and stamped
  "checker: passed" while two criteria actually failed. Rule: every
  self-check line must cite evidence from the actual files; "n/a" on
  any state criterion is an automatic fail; a self-check that
  validates the run's own premise instead of the filesystem is worse
  than no self-check.
- A run declared pass but never appended the run summary to STATE.md
  and never moved the draft. Rule: verdict and file operations must
  agree; perform both post-pass actions before writing "passed".
- The pattern log showed a type at 2 consecutive reports and the new
  report contained a third occurrence, but the report claimed "no
  log exists" instead of stating the running count. Rule: quote the
  pattern log and compute the updated count every run.
- In-progress spec work was numbered as a divergence under the
  invented label "In progress (not cut)". Rule: only the four types
  may be numbered; in-progress items live in the accounting table
  and the Not-drift section.
- A timing sub-detail of an already-flagged data-lifecycle change was
  counted as a separate "silent decision", inflating the counts
  logged to state. Rule: fold dependent findings into their parent
  divergence.
- A divergence was typed "changed behavior" against a requirement the
  table marked "Shipped". Rule: reconcile divergence types with table
  statuses before the self-check; stated counts must equal a recount
  of the numbered list.
- A legal/compliance emergency was buried as one item among five with
  no next step. Rule: escalation line at the top of the report and a
  routed next step (who, by when) on every divergence.
- 2026-07-17: the checker's flag file cited this eval's own answer
  key by name as corroborating evidence, which would be an immediate
  tell to a real stakeholder that the artifact is test scaffolding,
  not genuine analysis. Rule: only cite the Sources (spec, digest,
  STATE.md, SKILL.md) as evidence; never name or lean on any other
  file, including anything that looks like a fixture or answer key,
  even if one exists in the repo — its presence is irrelevant, and
  citing it is disqualifying regardless of whether the verdict is
  otherwise correct.
- 2026-07-17: a shipped-but-different, irreversible delete mechanism
  was typed "cut scope" (nothing shipped) instead of "changed
  behavior" (something shipped, just not the specified thing) —
  the report's single most important finding, mislabeled. Rule:
  before typing "cut," name the shipped code path that would have to
  not exist for that to be true; if a PR built anything addressing
  the requirement, the type is "changed," never "cut."
- 2026-07-17: a self-check confirmed a divergence's type was on the
  closed four-type list without checking it was the *correct* one of
  the four for what shipped — a syntactic pass on a real
  misclassification. Rule: a self-check (and Checker check 3) must
  state why the chosen type fits the shipped facts, not just that
  it's a valid label from the list.
- 2026-07-17: a dropped spec parenthetical was rendered as a bare
  "..." with no bracket marking the elision, and the checker filed it
  as a secondary, non-dispositive note instead of an independent
  failure. Rule: elisions must be marked "[...]"; an unmarked or
  unbracketed elision is its own gate failure, never downgraded to a
  secondary note regardless of what else in the finding is correct.
- 2026-07-17: a FAIL flag led with the mechanical retype-the-label fix
  and never restated that the underlying live legal/data-loss
  incident still needed Legal + the accountable PM notified today,
  leaving a reader unsure whether anything was actually urgent. Rule:
  a FAIL flag must restate any escalation-worthy finding from the
  draft as still active and unresolved, independent of the verdict —
  gate mechanics (label correctness) and real-world urgency (a live
  incident) are two different clocks; neither line may eclipse the
  other.
- 2026-07-17: reports were correct but read flat: a wall of numbered
  prose that made a VP read the whole document to find the one thing
  that mattered, with soft calls ("may be worth a look") standing in
  for a verdict. Now: the report opens with a `## Bottom Line` block
  (3-5 dense, cited bullets) immediately after the header, every
  section leads with its single most important figure bolded, and
  every claim in the body carries a citation or gets cut — no
  unsupported adjectives, no hedges, no filler.

## Checker criteria
- `## Bottom Line` exists immediately after the header (after the
  escalation line, if one fires), with 3-5 bullets. Every bullet
  cites something concrete found elsewhere in the same draft — a
  divergence number, spec section, PR number, table stat, or
  STATE.md pattern count — and that citation checks out against the
  body when you look. Reject any bullet vague enough to apply to any
  run ("things look mostly fine," "continue monitoring") or that
  merely restates the header; that is a fail on its own.
- Header quotes STATE.md's latest last-run entry and it matches the
  actual file (open STATE.md and compare; never trust the report).
- No claim that STATE.md is missing unless a file error is shown.
- Every numbered divergence: uses one of the four types only, and is
  the *correct* one of the four for what actually shipped — being on
  the closed list is necessary but not sufficient; for any "cut,"
  confirm nothing shipped for that requirement, and for any
  "changed," confirm something did but differently. Quotes spec text
  verbatim, character-for-character, including any elision marked
  "[...]" — a bare, unbracketed "..." or any other unmarked drop of
  spec words is its own failure here, never a secondary note, even if
  the divergence's type and every other field are correct. Cites PR
  numbers/dates that match the digest. Includes severity and a next
  step with an owner and a timeframe.
- Every spec requirement is tabled with a status from the closed
  vocabulary; table statuses and divergence types are consistent;
  the stated per-type counts equal a fresh recount of the list.
- No accepted deviation from STATE.md appears as a numbered
  divergence or as "changed"/"cut" in the table (verify against
  STATE.md itself).
- No in-progress item is numbered. No pure-refactor PR is flagged.
  No dependent finding is double-counted.
- Pattern note quotes STATE.md's pattern log and states the correct
  running count including this report; a process pattern is declared
  only at 3+ consecutive reports.
- If any divergence is a legal/compliance or data-loss incident at
  "users notice" severity, the escalation line is present at the top.
- Self-check lines cite file evidence; none say "n/a" on a state
  criterion; none stop at "this label is on the closed list" without
  also confirming it is the correct label for the shipped facts.
- Neither the draft nor the checker's own rationale cites, names, or
  leans on any file outside Sources (spec, digest, STATE.md,
  SKILL.md) as evidence — including anything resembling a test
  fixture, answer key, or grading rubric. Such a file's existence is
  irrelevant to the verdict; naming it is an automatic fail on its
  own, independent of whether the underlying conclusion is right.
- On pass: confirm the draft was moved AND the STATE.md run summary
  was appended before accepting "passed" as the verdict.
- On fail: confirm the flag restates any escalation-worthy finding
  from the draft as still active and unresolved, independent of the
  fail verdict — the mechanical fix instruction (what to retype/fix)
  and the real-world urgency (a live legal/data-loss incident) are
  reported on separate lines; neither may eclipse the other.
- If an HTML report was generated (PASS only), every figure, count,
  spec quote, PR number, owner, and next step in it traces to the
  passed draft verbatim, with nothing added, dropped, or re-ranked and
  no divergence reordered in a way that changes meaning; the divergence
  counts in the stat tiles equal the draft's recomputed per-type
  totals. A clean/no-drift run renders an explicit all-clear state and
  any UNAVAILABLE source renders an explicit UNAVAILABLE tile, never a
  blank or a zero. The report is one self-contained file and carries
  the same no-em-dash bar as the draft.
