name: competitive-brief
description: Runs every Monday 7am. Pulls competitor changes from fixed
sources, formats against the tracked dimensions, checks coverage, files
the brief.
---
## Sources

All sources are local snapshot files, relative to the project root
(/Users/aakashgupta/Downloads/pm-loop-pack). The current week's
snapshots live in data/competitive-brief/week-2026-07-13/; the prior
week's are in data/competitive-brief/week-2026-07-06/ for reference.

- Slotwise: changelog `data/competitive-brief/week-2026-07-13/slotwise-changelog.md`, blog `data/competitive-brief/week-2026-07-13/slotwise-blog.md`
- CalPilot: changelog `data/competitive-brief/week-2026-07-13/calpilot-changelog.md`, press page `data/competitive-brief/week-2026-07-13/calpilot-press.md`
- Meetrix: blog `data/competitive-brief/week-2026-07-13/meetrix-blog.md`, changelog `data/competitive-brief/week-2026-07-13/meetrix-changelog.md`

## Dimensions tracked
Features, pricing, positioning, announcements.

## Output format
The brief opens with a "## Executive summary" section, before any
competitor section:
- One line per competitor naming that competitor's single biggest move
  this week (or "No material change this week" if genuinely none).
- A "Key takeaways" list of 3-5 bullets synthesized ACROSS all
  competitors (patterns, threats, opportunities), not a restatement of
  the per-competitor lines above it. Each takeaway is one dense
  sentence with three parts: the single most important insight, why it
  matters to our scheduling product, and a citation back to the
  specific evidence in a per-competitor bullet below (competitor name
  + figure/price/date/version, or a Trend citation with its STATE.md
  sighting dates) — something a reader could Ctrl-F and find verbatim.
  No takeaway may introduce a new, uncited fact, restate the header, or
  be generic enough to fit any week's brief ("things look mostly
  fine," "continue monitoring").

After the executive summary: one section per competitor. 3-4 bullets
max per section, counted before filing, and "Trend:" bullets count
toward the cap. Every bullet ends with "Implication: [one sentence
connecting this change to our scheduling product]."

Source links and visuals:
- Where the source snapshot provides a URL for an item (its own
  "source:" header line, or an inline link), cite it inline on the
  bullet, e.g. "(blog: slotwise.com/blog)" or "(changelog:
  calpilot.io/updates)". If a competitor's snapshots carry no
  per-item URL at all, state once under that competitor's heading:
  "No direct source links available in this week's snapshot." Never
  invent or guess a URL not present in the source.
- If a source snapshot references or embeds an image or screenshot for
  an item, add "[screenshot: <path or reference>]" to that bullet. If
  a competitor's snapshots contain no image or screenshot reference at
  all, state once under that competitor's heading: "No visual
  available this week." Never invent or describe an image that is not
  in the source.

Style rule (applies everywhere in the brief, including the executive
summary, bullets, implications, and the checker footer):
- Never use an em dash. Use a period, comma, or colon instead.

Formatting (every run):
- Real markdown headers — "## Executive summary" and "## [Competitor]"
  as H2 — never bold text standing in for a header.
- A markdown table wherever content is naturally tabular: a price/plan
  comparison, a multi-attribute list (competitor x dimension x
  old->new value), or a before/after set of figures.
- Bold the single most important figure or call in each section — the
  one number or decision a VP should not miss (a price delta, a trend
  call, a build-vs-pass ask). One bold per section, not a bolded
  paragraph.
- No walls of prose: bullets and tables only in the body.

Voice — VP-of-Product, not analyst notes:
- High information density. No filler, no throat-clearing ("it is
  important to note that", "as we can see").
- Every claim carries a specific citation — a source snapshot figure,
  date, price, or version.
- Confident and precise: state the call ("Pass on X", "Trend: Y is
  now a pattern"). Never hedge ("might suggest", "could indicate").
- Zero unsupported adjectives. "Significant", "robust", "major" etc.
  ship only immediately backed by the number that earns them —
  otherwise cut the adjective and give the number alone.

Hard bullet rules:
- The brief body contains ONLY news bullets and labeled "Trend:"
  bullets. No "Excluded:", "Note:", "no change", exclusion-rationale,
  culture/hiring, or loop-hygiene bullets ever appear in the body —
  those live exclusively in the state-append working file. If the word
  "Excluded" appears anywhere in the brief body, the run fails.
- A bullet may only contain items dated (by the item's own date) inside
  the reporting window. An out-of-window item never earns a bullet, no
  matter how it is labeled or hedged. If it matters for the future, put
  it in the STATE.md append as a watch note — not in the brief body.
- An item already reported in a prior run (check STATE.md "Last run")
  is stale. Never re-report it as a bullet.
- Full coverage: every in-window item in every source snapshot must
  either earn a bullet (small items may share a bullet with a related
  item) or be listed in the state append's exclusions with a one-line
  reason. Silently dropping an in-window item is a fail.
- Every number, price, date, count, and version in a bullet must be
  copied exactly from the source snapshot, stated as old -> new where a
  value changed (e.g. "$18 -> $24/user/mo"). Re-read the snapshot line
  before writing the number; never paraphrase figures from memory.
- Item-to-release attribution: every item mentioned in a bullet stays
  attached to its OWN release's date and version. When several items
  are folded into one bullet, re-read the changelog heading each item
  sits under before writing; an item must never inherit the adjacent
  clause's version or date. "The digits appear somewhere in the
  snapshot" is not correctness — the item-to-release mapping must be
  right.
- A shared bullet's Implication must honestly cover every item in the
  bullet. If it cannot, split the bullet, or move the minor items
  (e.g. small bug patches) to the state append as exclusions with a
  reason ("minor fix, append-only").
- Implications must be actionable: name a concrete next action or
  decision for our scheduling product (what to do or decide, and by
  when where relevant), and where possible a named owner or ticket.
  "No product action", "loop hygiene only", or a restatement of the
  change is not an implication.
- Implication deadlines and venues must be real: only reference a
  meeting, review, or internal date that is established in the source
  snapshots, STATE.md, or CLAUDE.md. If no such venue exists, phrase
  the deadline as a proposal ("propose a build-vs-pass decision by
  2026-07-31"), never as if the meeting already exists ("at the
  2026-07-31 roadmap review").
- Source moves/404 recoveries get at most one plain line directly under
  the competitor heading ("Source note: changelog moved to X; recorded
  in SKILL.md."), never a bullet and never an Implication line. The
  full record goes in SKILL.md Known failure modes and the state
  append.

Trend rules:
- A pattern seen 3 consecutive weeks (per the STATE.md pattern log,
  counting this run) is written as a trend, distinct and clearly
  labeled ("Trend:"), not folded inside a news bullet.
- Trend evidence is OUR pattern log: cite each prior sighting with its
  own STATE.md date (e.g. "3rd consecutive week: 2026-06-29 X,
  2026-07-06 Y, this week Z"). A competitor's own marketing claim
  ("our third ship in three weeks") is corroboration at most, never
  the primary evidence. Date each prior sighting individually — never
  let one date read as covering multiple ships.
- A pattern below threshold gets its running count stated explicitly
  in the bullet ("2nd consecutive week; becomes a trend if seen next
  week") so the reader knows why it is not yet a trend. Do not call it
  a trend early.
- Sighting date vs ship date: a pattern-log sighting date is the run
  date, not the ship/GA date. When this week's sighting refers to a
  ship, write both so neither can be misread, e.g. "2026-07-13
  sighting: prep notes (GA July 10)" — never "2026-07-13 prep notes
  GA".

## Presentation layer
After the checker returns PASS, the maker generates a self-contained
HTML report FROM the already-passed markdown brief. The markdown draft
stays the audited source of truth; the gate and checker apply to it in
full. Never render an unpassed or flagged draft as a polished page.
Follow `.claude/skills/_shared/report-style.md` for all color, type,
layout, and components. Do not restate the palette here.

Map this weekly competitive brief onto the shared kit:
- Header eyebrow: "Competitive brief" plus the reporting week (e.g.
  week of 2026-07-13); H1 title; run-meta strip naming the source
  snapshots and the green PASS verdict badge.
- Bottom-line banner: the Executive summary's single sharpest call this
  week (the one move a VP cannot miss), with its key figure bolded.
- Stat tiles: the numbers that moved this week become tiles, e.g. a
  price delta stated old -> new ($18 -> $24/user/mo), a ship-count for
  a competitor, or a trend's consecutive-week count. A source with no
  figure this week shows the explicit UNAVAILABLE state, never a zero.
- Severity chips: each competitor's biggest move gets a chip by threat
  level (● BREACH for a direct pricing/feature hit, ▲ AT-RISK for a
  watch item, ✓ ON-TRACK for no material change), with a matching left
  stripe on that competitor's card. "Trend:" items carry a counter chip
  with their consecutive-week count.
- Main audited table: the per-competitor moves table (competitor x
  dimension x old -> new value), reproduced in full, every listed row
  present, tabular-nums on figures.
- Owner + next-step: each move renders its Implication's concrete next
  action inline under the move, with the named owner or ticket where
  the draft carries one.
- Provenance footer: source snapshot paths, run timestamp, checker
  PASS, and "Generated from the audited brief; every figure traces to
  source."

Every figure, claim, name, price, and citation in the HTML traces to
the passed brief verbatim; no invented figure and no reordering that
changes meaning. Where the draft says UNAVAILABLE or "No material
change this week", the report shows that state explicitly, never a
blank or a fabricated value. One self-contained file (inline CSS and
SVG, no external assets), and the same no-em-dash bar as the brief.

## State file
Read STATE.md in this skill folder before starting. It holds the last
run summary, the pattern log, and lessons learned. Reading it is a
precondition for both maker and checker — a run that claims STATE.md
does not exist, without listing the skill directory to prove it, is
invalid.

A pass is only real when its side effects exist on disk. On a passing
run, append to STATE.md:
1. A "Last run" entry for the run date: competitors covered, every
   material finding (pricing/packaging changes, new surfaces, source
   moves), and what was deliberately excluded and why.
2. Pattern log updates: increment the sighting count of EVERY tracked
   pattern seen again this week (with this week's date), add new
   watch-worthy patterns at count 1, and mark any pattern that crossed
   3 weeks as "called as trend on [date]".
3. Any source path change (old path -> new path, date noticed).

Writes are performed, not proposed: if the run discovers something that
"should be recorded" (a moved source path, a new failure mode), the run
edits SKILL.md / appends to STATE.md itself during the run, then states
in the brief that it was done. A brief that leaves instructions for a
future run instead of acting is a fail. Any path recorded in SKILL.md
or STATE.md must be concrete and literal (this week's actual path) —
never a placeholder like "week-[DATE]".

The pending state append is drafted as a SEPARATE working file next to
the brief draft (see MAKER.md), never inside the brief itself. The
filed brief must be board-clean: brief sections plus the checker footer
only — no "State append" section, no code blocks of pending state.

The executed STATE.md append must be identical to the state-append
working file — the working file IS the append, appended verbatim. If
the working file is missing anything the brief reports (a fix, an
exclusion, a pattern update), the run fails until the working file is
corrected; the checker never silently writes a more complete append
than the draft. Draft and executed append must match so the audit
trail matches what was written.

## Known failure modes
(Write every mistake here the day it happens. This becomes the most
valuable part of the skill file.)
- 2026-05-18: Treated an item older than 7 days as new because the page
  lists a rolling month. Rule: check the item's own date, not the page's.
- If a changelog source is a 404/moved page, check whether the page
  points to a new path; if the new path's snapshot exists in the same
  week folder, use it, note the move as a one-line "Source note:" under
  the competitor heading (never a bullet), and record the new path here
  during the same run as a concrete literal path (perform the edit; do
  not write "record this" as an instruction). Check both paths for 2
  weeks.
- 2026-07-13: Checker asserted "no STATE.md exists" and waived the
  trend-verification criterion on that false premise; STATE.md existed
  with the needed pattern log. Rule: the checker must open STATE.md
  itself; if it cannot, it fails the run — it never waives a criterion.
- 2026-07-13: A 3-week trend was sourced from the competitor's own blog
  line instead of our pattern log. Rule: trends cite the STATE.md
  sighting dates as primary evidence.
- 2026-07-13: An out-of-window, already-reported press item kept a full
  bullet because it was "labeled as outside the window". Rule: labeling
  does not earn a bullet — cut it; at most add it to the STATE.md watch
  notes. Cross-check STATE.md "Last run" so stale items are never
  re-reported.
- 2026-07-13: Run declared PASS with zero side effects — no filed brief,
  no STATE.md append, no SKILL.md edit for a moved source path. Rule:
  pass = files moved + STATE.md appended + any promised records actually
  written, verified to exist before "passed" is printed.
- 2026-07-13: Meetrix changelog moved: `data/competitive-brief/week-2026-07-13/meetrix-changelog.md` (meetrix.app/changelog) is a 404 pointing to meetrix.app/news; new snapshot path is `data/competitive-brief/week-2026-07-13/meetrix-news.md` (meetrix.app/news) — future weeks follow the same convention, i.e. the current week folder's `meetrix-news.md`. Used the new path this run. Check both paths through 2026-07-27.
- 2026-07-13: A repeating pattern's sighting count was not incremented
  and the brief never stated the count. Rule: every repeat sighting
  updates the pattern log and the bullet states "Nth consecutive week".
- 2026-07-16: Exclusion lines leaked into the brief body AGAIN as
  labeled bullets ("Excluded as out-of-window/stale: ...", "Excluded:
  ..."), repeating the 2026-07-13 labeling failure, and pushed one
  section to 5 bullets. Rule: exclusions are append-only; the word
  "Excluded" never appears in the brief body; count bullets per section
  (max 4) before filing.
- 2026-07-16: "Note (...)" meta-bullets shipped without an
  "Implication:" ending. Rule: if a line cannot honestly end with an
  actionable Implication, it is not a bullet — move it to the state
  append or delete it. (A genuine defensive point, e.g. "AI stays free
  in existing plans", may keep a bullet only WITH a real implication
  such as arming sales to neutralize FUD.)
- 2026-07-16: A source move earned a full bullet whose implication was
  "no product action — loop hygiene only". Rule: source moves get one
  plain "Source note:" line under the competitor heading — no bullet,
  no Implication; the record lives in SKILL.md/STATE.md.
- 2026-07-16: The "State append — pending checker pass" block was left
  inside the filed deliverable. Rule: the state append is a separate
  working file (see MAKER.md); the filed brief contains brief sections
  and the checker footer only.
- 2026-07-16: An in-window item (Meetrix quiet-hours setting for
  reminder sequences, July 9) was silently dropped — no bullet, no
  logged exclusion. Rule: sweep every snapshot item; each in-window
  item is either a bullet (or folded into a related bullet) or an
  append exclusion with a stated reason.
- 2026-07-16: A SKILL.md edit recorded a snapshot path with a
  placeholder ("week-[DATE]/..."). Rule: recorded paths are concrete
  and literal so a future run can match them exactly.
- 2026-07-16: A v4.19 (July 10) bug fix was folded into a shared
  bullet's v4.18.1 (July 8) clause — wrong version AND date — because
  fixes were grouped by theme, not by release. Rule: every folded item
  keeps its own release's date/version; re-read the changelog heading
  each item sits under before writing the clause.
- 2026-07-16: The checker footer certified "Numbers recomputed vs
  snapshots ... All exact" while the misattribution above stood — it
  checked that digits appear somewhere in the source, not which
  release each item belongs to. Rule: the recompute step verifies
  item-to-release attribution per item; no exactness claim may be
  printed until every folded item's version/date mapping is confirmed
  against its own source heading.
- 2026-07-16: Implications cited internal meetings that exist nowhere
  in the fixtures, STATE.md, or CLAUDE.md ("the 2026-07-31 roadmap
  review", "Thursday's product review"). Rule: name a venue only if a
  source/state/CLAUDE.md line establishes it; otherwise phrase the
  deadline as a proposal ("propose a build-vs-pass decision by
  2026-07-31") and prefer a named owner or ticket.
- 2026-07-16: Trend bullet read "2026-07-13 (this week) prep notes GA"
  — the pattern-log sighting date could be misread as the GA date (GA
  was July 10). Rule: write sighting and ship dates separately:
  "2026-07-13 sighting: prep notes (GA July 10)".
- 2026-07-16: One bullet packed four loosely related items under an
  Implication that covered only two of them. Rule: a shared bullet's
  Implication covers every item in it, or the bullet is split / the
  minor items move to the state append as reasoned exclusions.
- 2026-07-16: The executed STATE.md append was more complete than the
  state-append working file (draft omitted three fixes the append
  included), breaking the audit trail. Rule: the working file is
  appended verbatim; any gap between brief, working file, and executed
  append is a fail — fix the working file first, then append.
- 2026-07-17: Voice/format upgrade. Before: the brief was correct but
  read like analyst notes, not a VP brief. Key takeaways restated
  per-competitor facts instead of citing them, prose paragraphs buried
  the one number that mattered, and unsupported adjectives ("a
  significant price move") stood in where a figure belonged. Now: each
  Key takeaway is a dense sentence naming the insight, why it matters,
  and a citation findable verbatim below; every section uses real H2
  headers, a table for tabular content, and one bolded key
  figure/call; filler and unsupported adjectives are banned. Rule: the
  checker rejects a Key takeaway with no findable citation or generic
  enough to fit any week, and rejects filler/unsupported-adjective
  language anywhere in the brief.

## Checker criteria
The brief opens with "## Executive summary" containing one line per
competitor naming its single biggest move this week (or "No material
change this week"), plus a "Key takeaways" list of 3-5 bullets
synthesized across ALL competitors, each traceable to a fact also
present in a per-competitor bullet below. Each takeaway names an
insight, states why it matters, and cites evidence (competitor name +
figure/price/date/version, or a Trend citation) locatable verbatim in
a per-competitor bullet below. A takeaway citing a fact not found in
any per-competitor bullet, with no findable citation, or generic
enough to fit any week's brief ("things look mostly fine," "continue
monitoring") is a fail. Every bullet cites its
source URL inline when the snapshot provides one, or the competitor
heading states "No direct source links available in this week's
snapshot" when it does not; an invented URL is a fail. Every bullet
notes "[screenshot: ...]" when the snapshot references an image, or the
competitor heading states "No visual available this week" when it does
not; an invented or described-but-absent image is a fail. No em dash
(—) appears anywhere in the brief, including the executive summary and
the checker footer, a single occurrence is a fail.
All competitors covered. The brief body contains only news and "Trend:"
bullets — any "Excluded"/"Note"/no-change/hygiene bullet in the body is
a fail, and the word "Excluded" must not appear in the body at all.
Max 4 bullets per section, counted (Trend bullets count). Every
bulleted item dated (by its own date) within 7 days of the run date
(2026-07-13) — no exceptions via labels. No bullet repeats an item
recorded in STATE.md's prior "Last run" entries. Every bullet ends
with an Implication line naming a concrete action or decision — "no
product action" / "loop hygiene only" fails. Coverage sweep: the
checker re-reads every source snapshot and confirms each in-window
item is either a bullet (or folded into one) or an exclusion-with-
reason in the state-append working file; a silently dropped in-window
item is a fail. Every number/date/price in the brief matches the
source snapshot exactly (checker recomputes against the files), AND
every item — especially each item folded into a multi-item bullet — is
attributed to the release (version + date) it actually sits under in
the source; a right number under the wrong release/date is a fail, and
no "all exact" certification may be printed before this per-item
attribution check. Implications name a concrete action or decision
with an owner or ticket where possible — "no product action" / "loop
hygiene only" fails; a shared bullet's Implication must cover every
item in the bullet; any meeting/venue/deadline an Implication cites
must be established in the sources, STATE.md, or CLAUDE.md, else it
must be phrased as a proposal. Trends
claimed match STATE.md's pattern log (3 consecutive weeks) and cite
each logged sighting date; sub-threshold patterns state their count,
and this week's sighting distinguishes sighting date from ship/GA date
("2026-07-13 sighting: X (GA July 10)").
Any pricing or packaging change in the sources is explicitly called
out. Source moves appear only as a one-line "Source note:" under the
competitor heading, with the concrete new path (no placeholders)
recorded in SKILL.md. The state append is a separate working file; a
brief containing a state-append block fails. A dead source with no
recoverable new path means flag, not brief. Any in-run promise to
record something has actually been written to SKILL.md/STATE.md. On
pass, the filing and STATE.md append are executed and verified on
disk, and the executed append is identical to the state-append working
file — if the working file omits anything the brief reports, the run
fails; the checker never appends a more complete entry than the draft.
Real headers, a table for any tabular content, and one bolded
figure/call per section are all present; a wall of undifferentiated
prose is a fail.
The HTML presentation report is generated only after the brief passes.
Every figure, flag, name, price, and citation in it reproduces from the
passed brief with nothing added, dropped, or re-ranked, and no move
reordered in a way that changes meaning. Any UNAVAILABLE or "No
material change this week" state is rendered explicitly, never as a
blank or a fabricated value. The report is one self-contained file
(inline CSS and SVG, no external assets) and honors the no-em-dash bar;
a single em dash, an invented figure, or a page built from an unpassed
draft is a fail.
