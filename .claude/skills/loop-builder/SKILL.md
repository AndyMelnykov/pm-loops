---
name: loop-builder
description: Builds a new six-piece loop (trigger, skill file, maker, checker, gate, state file) from a user's rough description, at the same quality bar as the shipped 12. Triggers when the user asks to create, build, add, or design a new loop, or describes a repeating task they want automated ("every week I...", "whenever a deal closes I...").
---

# Loop builder

From a one-line ask ("I want a loop that summarizes my standups") to a complete, tested loop. Ask only what you can't safely assume; propose defaults for everything else so the user can just say yes.

## Step 0 — Readiness test (silent unless it fails)

Answer the four questions from the user's description before building:
1. Repeats at least weekly (or per-event)?
2. Can "done" criteria be written before the agent starts?
3. Is wrong output caught before a stakeholder sees it?
4. Human review before anything irreversible?

If any fails, say so plainly: "This is a prompt, not a loop — [which question fails and why]." Offer the prompt instead. Don't build a loop that will produce confident wrong output on a schedule. Watch for the three known non-fits: deciding what to build next (judgment, not a rule), per-user personalization (recommendation engine's job), anything touching the live product without human approval.

## Step 1 — Extract or ask

From their description plus a scan of connected MCP tools and local files, fill this spec. **Ask at most 3-4 questions, only where a wrong assumption breaks the loop**; everything else gets a stated assumption they can correct:

| Piece | Ask if unknown | Safe to assume |
|---|---|---|
| Sources (exact channels/paths/URLs) | YES — never guess a data source | — |
| "Done" / gate criteria | YES — this is their judgment, encoded | propose a draft they edit |
| Thresholds (for monitoring loops) | YES — propose numbers, get a yes | — |
| Trigger cadence | — | infer from the task (weekly synthesis → Monday 7am; monitoring → daily; event → on-event) |
| Task pattern | — | classify: repeating synthesis / event-triggered extraction / periodic prep / threshold monitoring |
| Output format | — | default: short sections, every claim cited, ends with next action |
| Output destination | — | default: file under `runs/<name>/`, human routes onward |

Batch the questions in ONE message with proposed defaults inline ("I'll assume X unless you say otherwise").

## Step 2 — Write the four files

Create `.claude/skills/<name>/`: `SKILL.md`, `MAKER.md`, `CHECKER.md`, `STATE.md`. Copy the structure and voice of the shipped loops (open one shipped skill folder as the live template — don't work from memory).

**SKILL.md** must contain: name + description (with trigger cadence), Sources, format/dimensions/taxonomy as fits the pattern, State file contract (what maker reads, what checker appends, a pattern-promotion rule — e.g. "3 consecutive weeks → trend"), Known failure modes (seeded with 1-2 plausible ones for this domain), Checker criteria.

**Quality bar — bake these into MAKER.md and CHECKER.md; they are what separates a 60-score loop from a 95-score loop:**
- Every number recomputed from source and cited (value, comparison window, % change). Never "significant" where a number exists.
- Dedup rules explicit (e.g. count one mention per customer, not per ticket).
- Must-NOT-flag rules explicit: known baselines, documented exceptions, marked-evergreen docs, in-progress work, single flaky data points. Precision failures cost more trust than misses.
- State continuity: prior open flags carried forward or explicitly closed ("resolved since last run"), never silently dropped; repeated findings labeled as ongoing (day N), not re-announced as new; state promotion rules applied.
- Freshness gate: name a max age for each source; stale source = flag, not silent inclusion.
- Every flag ends with the next-hour action: one concrete step to verify or rule out.
- Checker is binary pass/flag, checks against SKILL.md criteria AND recomputes 2-3 spot numbers itself, never fixes the draft, never softens a fail into a note.

**STATE.md**: template (Last run / Pattern log / Lessons learned) seeded empty — no fake history. (Known failure modes in SKILL.md are the one exception: seed 1-2, labeled "Plausible risk — not yet observed," never as dated incidents.)

**State-append authorship**: the maker drafts the state-advance block at the end of its draft; the checker verifies it and, on pass, appends it to STATE.md. The checker never authors state content itself.

**MAKER.md / CHECKER.md paths**: drafts to `runs/<name>/drafts/[date].md`, approved output to `runs/<name>/[date].md`, flags to `runs/<name>/flags/[date].md`. `[date]` = the data day being analyzed, not the run day. Pattern-promotion rules scale to the cadence: 3 consecutive runs (weeks for weekly loops, days for daily ones) → promoted.

## Step 3 — Test before handing over

Never deliver an untested loop:
1. If real sources are reachable, run against them. Otherwise generate a small realistic fixture in `data/<name>/` — include one planted defect the loop must catch and one decoy it must not flag.
2. Run MAKER.md as one agent, CHECKER.md as a separate fresh agent.
3. If the checker flags: when the maker misread the data, have the maker fix the draft and rerun a fresh checker; when the miss traces to a loop-file gap (criteria the maker couldn't have known), fix the loop files too and log it in Known failure modes.
4. Show the user the output and what the checker verified. If it ran on fixtures, say so and point at what to swap.

## Step 4 — Register and schedule

1. Add the loop to `LOOPS.md` (name, sources, trigger, last run, status). Create the file if it doesn't exist — a user whose first act is building their own loop is onboarded by definition; loop-builder takes precedence over start-here in that case.
2. Give the cron line for their cadence: `claude -p --bare "/<name>"` — plus the headless-auth warning from the README.
3. Remind them of the first-week rule: read every output, disagree with one thing, write corrections into Known failure modes — and the 6-week gate audit.

## Voice

Loop files read like the shipped ones: terse, direct, active, short paragraphs, no filler. If the user's ask maps closely onto one of the shipped 12, say so and offer to adapt that loop instead of building from scratch.
