# Loop evals

Use these to answer one question: **did my change to a skill make it better or worse?**

The design copies the `ai-quality-watchdog` loop. That loop scores a live AI feature against a fixed eval set every night. This folder does the same for the loops themselves:

| ai-quality-watchdog | evals/ |
|---|---|
| `eval-set.json`: fixed inputs, each with literal pass criteria | `evals/<loop>/eval-set.json`: fixed cases, each with an answer key and criteria |
| Every example scored PASS/FAIL with a one-line reason | Every criterion scored PASS/FAIL with a one-line reason |
| `history.csv`: pass rate per night | `evals/<loop>/history.csv`: pass rate per run, stamped with the skill version |
| Alert when the pass rate drops vs the baseline | `compare`: baseline vs candidate, criterion by criterion |

## What a case is

A case is one frozen scenario:

- **Inputs:** the loop's fixtures in `data/<loop>/`, optionally overridden by `cases/<ID>/fixtures/`.
- **Frozen state:** `cases/<ID>/STATE.md` is copied over the skill's STATE.md before every run. Loops append to STATE.md as they run, so without this freeze no two runs see the same input.
- **Answer key** (`reference`): the correct result, recomputed by hand from the fixtures.
- **Criteria:** what a correct output must and must not do. Most criteria come straight from the skill's Known failure modes.

Criterion types:

| type | checks | needs a model? |
|---|---|---|
| `must_contain` / `must_not_contain` | literal strings in the output (case-insensitive) | no |
| `regex` / `not_regex` | a pattern in the output | no |
| `heading_order` | the sections exist and appear in this order | no |
| `section_bullets` | a section has min..max top-level bullets | no |
| `gate_passed` | the checker approved the draft (an approved file exists) | no |
| `state_advanced` | a state file changed and contains given strings | no |
| `file_unchanged` | a file the loop must not edit was left alone | no |
| `judge` | a yes/no question, graded by a separate `claude -p` call that sees only the output and the answer key | yes |

Prefer deterministic types. Use `judge` only for things a string can't settle, like "is checkout kept off the flag list" or "does it name the right cause."

## Isolation

Each trial runs in a throwaway copy of the repo in your temp folder. `evals/`, `runs/` and `.git` are **not** copied, so the maker and checker can't read the answer key. The run uses `--setting-sources project`, so your personal plugins and hooks don't change results (see `config.json`). The judge runs in an empty directory.

## Use it

Requires Python 3.9+ and the `claude` CLI (set `CLAUDE_BIN` if it's not on PATH).

```bash
# 1. Baseline the current skill (3 trials per case; model output varies)
python evals/run_evals.py run metric-anomaly --label baseline

# 2. Edit .claude/skills/metric-anomaly/*.md

# 3. Run the candidate
python evals/run_evals.py run metric-anomaly --label my-change --notes "tightened Bottom Line rule"

# 4. Compare
python evals/run_evals.py compare metric-anomaly baseline my-change
```

`compare` prints every criterion that moved (`BETTER` / `WORSE`) and a verdict: IMPROVED, REGRESSED, MIXED or NO DETECTABLE CHANGE. Read every WORSE line before shipping a MIXED result.

Other commands:

```bash
# Grade any report by hand: no loop run, good for writing new criteria
python evals/run_evals.py grade metric-anomaly --case MA-001 --output path/to/report.md [--state path/to/STATE.md] [--no-judge]

# Re-score saved outputs after you edit criteria (no new loop runs)
python evals/run_evals.py regrade evals/results/metric-anomaly/baseline/<timestamp>
```

Note: in `grade` mode the file you pass counts as the approved output, so `gate_passed` always passes there.

Flags for `run`: `--case MA-001` (repeatable), `--trials N`, `--model`, `--judge-model`, `--no-judge` (deterministic only, cheaper), `--keep-workspace` (to debug a run), `--timeout` (seconds per run, default 2400).

**Cost and noise.** Each trial is a full maker → checker loop run, so expect minutes and real tokens per trial; the cost lands in `history.csv`. With 3 trials, one flipped trial is a 33-point swing on that criterion, so treat a single-trial change as noise. Run more trials before you trust a small difference.

## Files

```
evals/
  run_evals.py               runner, grader, compare (standard library only)
  config.json                CLI args for loop runs and the judge
  <loop>/eval-set.json       cases: setup, answer key, criteria
  <loop>/cases/<ID>/STATE.md frozen state snapshot for that case
  <loop>/history.csv         one row per (run, case): committed record
  results/                   raw outputs per trial (gitignored)
```

## Coverage

| loop | cases | what the cases test |
|---|---|---|
| metric-anomaly | MA-001 | day 2 of an open flag, clean vs contaminated baseline, under-threshold decoy, decoy causes |
| ai-quality-watchdog | AQW-001 | confirmed regression, new failures with a shared cause, intermittents not called new, exhaustive clears, em-dash trap |

The other 10 loops have no eval cases yet.

## Adding a case

1. Pick a scenario. The best sources are a skill's **Known failure modes** entries (each is a ready-made regression test) and a "nothing happened" day (does the loop stay quiet?).
2. Freeze the state: put the STATE.md as it would stand *before* this run in `cases/<ID>/STATE.md`.
3. If the scenario needs different inputs, put them in `cases/<ID>/fixtures/`. They overlay `data/<loop>/`, or replace it with `"fixtures_mode": "replace"`.
4. Recompute the correct answer from the raw files yourself and write it into `reference`. Never copy it from a loop's output.
5. Write criteria. Give each one a `why` that points to the rule or failure mode it protects.
6. Check the criteria before spending tokens: grade a hand-written good report and a deliberately bad one with `grade`. Every criterion should pass on the first and the right ones should fail on the second.

When a loop makes a new mistake, write it into the skill's Known failure modes **and** add a criterion here, so the fix can't silently regress.
