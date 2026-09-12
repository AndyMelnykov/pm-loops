# The PM Loop Pack

12 working loops for product managers. Each one packages a recurring PM task — competitive brief, feedback digest, sprint prep, metric watch — as a maker/checker/gate/state contract instead of a one-off prompt.

From the Product Growth deep dive: Loops for PMs. Get the guide at news.aakashg.com.

## New here? Don't read this — run it

Open Claude Code in this folder and say **"get me started."** Claude scans what you have connected (Slack, Notion, Linear, analytics, CRM…), picks the one loop that works with it, and offers to run it so you see your first output in minutes. Nothing connected? Every loop ships with realistic demo data in `data/` — you still get an output this session. The rest of this README is for after you've seen one run.

---

## Problem

PMs already do this work weekly — a competitor scan, a feedback rollup, a sprint-prep pass, a metric watch — by hand or with a throwaway prompt. Two things go wrong at that size:

- **No memory across runs.** A plain prompt re-reports last week's item as news, lets a metric that dipped just under threshold quietly roll into the new baseline, and forgets what it already excluded and why.
- **No separation between drafting and grading.** The same model that wrote the brief is the one "checking" it, so it rationalizes its own gaps — a checker that trusts the draft's claims instead of re-deriving them from source files will pass a wrong attribution as long as the digits appear *somewhere* in the source (a real failure mode logged in [`competitive-brief`](.claude/skills/competitive-brief/SKILL.md#known-failure-modes)).

A loop fixes both: a persistent state file per task, and a checker that is a separate agent invocation with no exposure to the maker's reasoning.

## Product

A loop is six pieces working together: **trigger, skill file, maker prompt, checker prompt, gate, state file.** Concretely, for the weekly competitive brief:

```text
1. Monday 7am trigger fires.
2. Maker reads STATE.md (last run, pattern log, lessons learned) and SKILL.md.
3. Maker pulls the week's changes from the named sources.
4. Maker drafts the brief + a separate state-append working file.
5. Checker (fresh invocation) re-derives every figure and citation from the
   SAME source files — never trusts the draft's claims.
6. Pass: brief is filed, STATE.md is appended, checker footer cites evidence.
   Fail: exact failing checks are written to runs/<loop>/flags/[date].md.
7. Human reads the filed brief before anything reaches a stakeholder.
```

The 12 shipped loops, grouped by task pattern:

**Repeating Synthesis** (same sources, same format, new content each cycle)
1. Weekly competitive brief
2. Feedback theme digest (tickets, sales notes, reviews, NPS, user interviews)
3. Sales deal intelligence
4. Weekly business review

**Event-Triggered Extraction** (fires when something happens)
5. Spec drift check
6. Launch readiness sweep

**Periodic Prep Documents** (recurring docs for the same stakeholders)
7. Product review hardening
8. Sprint prep sweep
9. Stale doc sweep

**Threshold Monitoring** (watches, fires only when a line is crossed)
10. Metric anomaly flag
11. Onboarding friction monitor
12. AI quality watchdog

**Readiness test — is this actually a loop?** Before building or running one, answer four questions:
1. Does this task repeat at least weekly?
2. Can you write the "done" criteria before the agent starts?
3. Is a wrong output caught before it reaches a stakeholder?
4. Does a human review before anything irreversible happens?

All four yes: build the loop. Any no: it's a prompt, not a loop.

## Demo

There's no recorded screencast yet (see Limitations). What you actually see, using the bundled competitive-brief fixtures under `data/competitive-brief/` as-is:

```text
$ claude -p --bare "/competitive-brief"

Maker reads STATE.md: prior run flagged "Slotwise ships an AI Assist
capability weekly" at 2 consecutive sightings (2026-06-29, 2026-07-06).
Maker reads this week's snapshots and drafts runs/competitive-brief/drafts/2026-07-13.md:

  ## Executive summary
  - Slotwise: 3rd consecutive AI Assist ship (meeting prep notes, v4.19).
  - CalPilot: Pro pricing $18 -> $24/user/mo (annual), effective 2026-08-01.
  - Meetrix: launched Signals (booking-funnel intent alerts).

  Key takeaways:
  - Trend: Slotwise's weekly AI Assist cadence is now a pattern (3rd
    straight week: 2026-06-29, 2026-07-06, 2026-07-13) ...

Checker (separate invocation) re-reads the source snapshots, recomputes
every price/date/version, confirms the trend against STATE.md's pattern
log, and either:
  PASS -> files runs/competitive-brief/weekly-2026-07-13.md,
          appends STATE.md, adds a checker footer citing evidence.
  FAIL -> writes runs/competitive-brief/flags/2026-07-13.md and stops.
```

Every figure above ($18 -> $24, the 3rd-consecutive-week trend) is real fixture data already in this repo, not invented for this README — see `data/competitive-brief/week-2026-07-13/` and `.claude/skills/competitive-brief/STATE.md`.

## Architecture

```text
  PM (you)
     |
     | schedule (cron) / /loop (session) / event webhook
     v
  TRIGGER
     |
     v
  MAKER  (agent invocation #1)
     reads:  SKILL.md, STATE.md, source data
             (bundled fixtures in data/, or your connected
             Slack / Notion / Linear / analytics / CRM)
     writes: draft + state-append working file
     |
     v
  CHECKER  (agent invocation #2 — separate context, no view of the
            maker's reasoning; re-derives claims from source files,
            never trusts the draft)
     |
     +-- FAIL --> runs/<loop>/flags/[date].md   (loop stops here)
     |
    PASS
     |
     v
  GATE side effects (deterministic, verified on disk)
     - file runs/<loop>/[date].md
     - append STATE.md verbatim
     - checker footer citing the evidence checked
     |
     v
  HUMAN REVIEW   <-- every loop stops here; never bypassed
     |
     v (explicit approval)
  Stakeholder / Slack / Notion / email
     (manual send — no loop wires this automatically)
```

There is no vector store, no long-running server, and no model-held session state. Each loop's memory is a plain STATE.md file; each loop's sources are named files or connected tools read fresh on every run.

## Core workflows

**Running a shipped loop** (example: competitive brief) — trigger fires → maker reads STATE.md and drafts → checker re-verifies against source files as a separate invocation → gate either files the brief + appends state, or flags and stops → human reads the filed brief before it goes anywhere. Walked in full in Demo above.

**Building a new loop** — tell Claude Code "build me a loop that [does X]." The `loop-builder` skill runs the same four-question readiness test, asks only what it can't safely assume (sources, done-criteria, thresholds — with proposed defaults), writes all six pieces at the shipped-loop quality bar, and test-runs it with a separate checker before handing it over. An untested loop is never handed over.

## AI design decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Agent architecture | Maker and checker are separate invocations, always | The model that wrote the draft is too lenient grading its own homework — see the logged failure where a checker waived a criterion by asserting "no STATE.md exists" without opening it |
| Checker grounding | Checker re-derives every figure/citation from source files, never from the draft's claims | A prior run passed with the footer "all exact" while an item was attributed to the wrong release — digits matched *somewhere*, but not the right place |
| Memory | Flat per-loop `STATE.md`, maker reads it in, checker appends verbatim on pass | Without it, a metric that dips just under threshold rolls into next week's baseline unflagged, and stale items get re-reported as news |
| Retrieval | Named local files / connected-tool reads, no embeddings or vector index | Each loop's sources are a small, fixed, named set (three competitors' changelogs, one sprint board) — exact paths are cheaper and more auditable than semantic search at this scale |
| Gate logic | Deterministic checklists (bullet counts, date windows, citation presence) rather than subjective LLM judgment | Keeps pass/fail reproducible run to run instead of drifting with model mood |
| Writes | Human-in-the-loop required before anything reaches a stakeholder | Loop output feeds real decisions and external comms; nothing irreversible ships unreviewed |
| New-loop admission | Four-question readiness test before any loop is built | Prevents turning one-off prompts into "loops" that nobody maintains |

## Safety / trust model

### Autonomous

- Read bundled fixtures or connected sources (Slack, Notion, Linear, analytics, CRM)
- Draft to `runs/<loop>/drafts/`
- Run the checker's re-derivation against source files
- Append `STATE.md` once a pass's side effects are verified on disk

### Requires review

- The filed brief itself, before being treated as final
- Gate criteria — audited every 6 weeks; gates rot silently while status stays green
- A skill file, reread whenever the product's strategy changes (the loop otherwise keeps running on the old one)

### Requires approval

- Anything reaching a stakeholder or leaving this repo — Slack, Notion, email
- Retiring a loop whose output people have stopped editing (a sign nobody's checking it anymore)

### Blocked

- Wiring a loop's output directly to Slack/Notion/email without the gate passing **and** human review
- Merging the maker and checker into one prompt or one invocation
- "Fixing" a bad output in chat instead of writing the mistake into that skill's Known failure modes section

## Evaluation

Every shipped loop was exercised with blind maker/checker runs and adversarial grading before shipping, and each skill folder's **Known failure modes** section is the resulting record — for example, `competitive-brief`'s log has 18 dated entries (2026-05-18 through 2026-07-16) covering real defects: stale re-reports, invented meeting venues, a checker that certified "all exact" over a wrong item-to-release attribution, exclusion text leaking into the filed body.

That log is real and growing, but it is not yet a reproducible evaluation suite: there is no `evals/` directory, no fixed case set per loop, and no published task-success/citation-precision/cost numbers. Treat the failure-mode logs as an honest defect history, not a benchmark. Closing that gap is on the roadmap below.

## Observability

There's no structured, machine-readable trace (no per-run token/latency log). What exists today, per loop:

- **`STATE.md` "Last run"** — what happened, what was found, what was excluded and why
- **Checker footer** — appended to every filed brief, citing the specific file + value checked for each criterion (a criterion with no cited evidence is itself a checker failure)
- **`runs/<loop>/flags/[date].md`** — the exact failing checks, written on a FAIL, without touching the draft
- **`Known failure modes`** in each SKILL.md — a dated postmortem log, the closest thing this repo has to a regression trace

This is legible to a human reviewing one run, but not queryable across runs. See Limitations.

## Running locally

Each loop file names its runner. There are three, and picking the wrong one is the most common setup mistake:

**Scheduled task** (most loops in this pack). Runs unattended on a schedule, no session open. Use the Claude desktop app's scheduled tasks or your OS scheduler calling:

```
claude -p --bare "/skill-name"
```

**/loop** (in-session intervals only). Runs a prompt or skill every N minutes while your session is open:

```
/loop 30m /metric-anomaly
```

It dies when the session closes and recurring tasks expire after 7 days. Right for watching something during launch week. Wrong for the Monday 7am brief.

**Event trigger** (the event-triggered loops). A webhook or automation calls the same headless command when the event fires, or you run it by hand the moment it happens.

**Headless auth gotcha.** Cron and automation contexts don't always inherit your interactive login — `claude -p` can fail with "Not logged in" even when your terminal session works. Test the exact command from your scheduler once before trusting the schedule; set an API key in the scheduler's environment if it can't reach the keychain.

## Limitations

- No recorded demo (GIF/video/screenshots) yet — the Demo section above is a textual walkthrough against real fixtures, not a captured run.
- No reproducible evaluation suite: quality claims rest on the Known-failure-modes logs and pre-ship adversarial testing, not a fixed, rerunnable case set with published numbers.
- Observability is document-based (STATE.md, checker footers, flags/), not structured traces — there's no cross-run query surface for token cost, latency, or tool-call history.
- Gates are hand-authored per loop and rely on a 6-week manual audit cadence; there's no automated detection of a gate that's gone stale.
- Retrieval assumes a small, named source set per loop; it doesn't generalize to large or unstructured corpora without embeddings.
- `/loop`-based runs expire after 7 days and die when the session closes — not a substitute for real scheduling on the loops that need it.
- Headless scheduling can silently fail auth if the scheduler's environment lacks an API key (see Running locally).

## Roadmap

### Reproducible eval suite

Why: pass/fail claims currently rest on manual adversarial-grader testing done once at ship time. A fixed case set per loop (input, expected behavior, forbidden behavior) would make quality claims inspectable on demand instead of only claimed.

### Structured run traces

Why: the Known-failure-modes logs capture lessons but not a per-run trace of tool calls, tokens, or latency. A lightweight trace would make diagnosing a bad run faster than reconstructing it from STATE.md and checker footers.

### Automated gate-drift detection

Why: gates currently depend on a human remembering to audit them every 6 weeks. Automated detection would catch a gate that's gone stale before three sprints pass silently under a green status.

---

## Maintaining your loops

- Never correct a loop in chat. Write every mistake into the skill file's "Known failure modes" section, where it compounds.
- Audit each gate every 6 weeks. Gates rot silently while the status stays green.
- Reread each skill file when your product's position changes. The loop runs on your old strategy until you tell it otherwise.
- Retire any loop whose output you've stopped editing. A loop nobody argues with is a loop nobody's checking.

## The rule that makes all 12 work

Every loop writes to a file. You approve before anything reaches a stakeholder or ships. The loop gathers and drafts. You judge.
