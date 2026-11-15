#!/usr/bin/env python3
"""Eval runner for the PM loop pack. Read evals/README.md first.

Modeled on the ai-quality-watchdog loop: a fixed eval set with literal
pass criteria, every criterion scored PASS/FAIL with a one-line reason,
and a history.csv so a change can be compared against a baseline.

Subcommands:
  run      run a loop end to end on its eval cases, grade, log history
  grade    grade an existing output file against a case (no loop run)
  regrade  re-grade a previous results folder after editing criteria
  compare  compare two labeled runs criterion by criterion

Standard library only. Python 3.9+.
"""
import argparse
import csv
import datetime as dt
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

EVALS = Path(__file__).resolve().parent
REPO = EVALS.parent
RESULTS = EVALS / "results"

# Top-level folders never copied into the run workspace. evals/ is
# excluded so the maker and checker cannot read the answer key.
COPY_IGNORE_TOP = {".git", "evals", "runs", "node_modules", ".venv", "venv"}

HISTORY_FIELDS = [
    "date", "label", "skill_hash", "case", "trials", "case_passes",
    "criteria_pass_rate", "gate_pass_rate", "failed_criteria",
    "cost_usd", "notes",
]

DETERMINISTIC = {
    "must_contain", "must_not_contain", "regex", "not_regex",
    "heading_order", "section_bullets", "gate_passed", "state_advanced",
    "file_unchanged",
}
KNOWN_TYPES = DETERMINISTIC | {"judge"}


# ---------------------------------------------------------------- utils

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def read(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def load_config():
    p = EVALS / "config.json"
    return json.loads(read(p)) if p.exists() else {}


def claude_bin():
    cand = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    if cand:
        return cand
    for name in ("claude.exe", "claude"):
        p = Path.home() / ".local" / "bin" / name
        if p.exists():
            return str(p)
    die("claude CLI not found. Put it on PATH or set CLAUDE_BIN.")


def load_eval_set(loop):
    p = EVALS / loop / "eval-set.json"
    if not p.exists():
        have = sorted(d.name for d in EVALS.iterdir() if (d / "eval-set.json").exists())
        die(f"no eval set for '{loop}'. Loops with evals: {', '.join(have) or 'none'}")
    es = json.loads(read(p))
    validate(loop, es)
    return es


def validate(loop, es):
    run = es.get("run", {})
    for key in ("prompt", "approved_globs", "draft_globs", "state_paths"):
        if key not in run:
            die(f"{loop}: run.{key} missing in eval-set.json")
    seen = set()
    for case in es["cases"]:
        st = case.get("setup", {}).get("state")
        if st and not (EVALS / loop / st).exists():
            die(f"{loop}/{case['id']}: state snapshot {st} not found")
        fx = case.get("setup", {}).get("fixtures")
        if fx and not (EVALS / loop / fx).is_dir():
            die(f"{loop}/{case['id']}: fixtures dir {fx} not found")
        for c in case["criteria"]:
            if c["type"] not in KNOWN_TYPES:
                die(f"{loop}/{case['id']}/{c['id']}: unknown type {c['type']}")
            key = (case["id"], c["id"])
            if key in seen:
                die(f"{loop}/{case['id']}: duplicate criterion id {c['id']}")
            seen.add(key)


def skill_hash(loop):
    """Hash of the skill files under test (STATE.md excluded: each case
    supplies its own frozen snapshot)."""
    h = hashlib.sha256()
    files = sorted((REPO / ".claude" / "skills" / loop).glob("*.md"))
    files.append(REPO / ".claude" / "skills" / "_shared" / "report-style.md")
    for f in files:
        if f.name == "STATE.md" or not f.exists():
            continue
        h.update(f.name.encode())
        h.update(f.read_bytes().replace(b"\r\n", b"\n"))
    return h.hexdigest()[:10]


def pick_case(es, case_ids):
    if not case_ids:
        return es["cases"]
    by_id = {c["id"]: c for c in es["cases"]}
    missing = [c for c in case_ids if c not in by_id]
    if missing:
        die(f"unknown case(s): {', '.join(missing)}. Have: {', '.join(by_id)}")
    return [by_id[c] for c in case_ids]


# ------------------------------------------------------------ workspace

def make_workspace(loop, es, case):
    ws = Path(tempfile.mkdtemp(prefix=f"loop-eval-{loop}-"))

    def ignore(d, names):
        out = [n for n in names if n == "__pycache__"]
        if Path(d).resolve() == REPO:
            out += [n for n in names if n in COPY_IGNORE_TOP]
        return out

    shutil.copytree(REPO, ws, ignore=ignore, dirs_exist_ok=True)
    setup = case.get("setup", {})
    if setup.get("state"):
        dst = ws / ".claude" / "skills" / loop / "STATE.md"
        shutil.copyfile(EVALS / loop / setup["state"], dst)
    if setup.get("fixtures"):
        dst = ws / "data" / loop
        if setup.get("fixtures_mode", "overlay") == "replace" and dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(EVALS / loop / setup["fixtures"], dst, dirs_exist_ok=True)
    # Mark the workspace as onboarded so CLAUDE.md's first-session flow
    # (start-here) does not hijack the run.
    if not (ws / "LOOPS.md").exists():
        (ws / "LOOPS.md").write_text(
            "# Active loops\n\nEval workspace. Onboarding already done.\n",
            encoding="utf-8")
    return ws


def snapshot_text(loop, case):
    st = case.get("setup", {}).get("state")
    if st:
        return read(EVALS / loop / st)
    p = REPO / ".claude" / "skills" / loop / "STATE.md"
    return read(p) if p.exists() else ""


def run_claude(prompt, cwd, extra_args, timeout, model=None):
    cmd = [claude_bin(), "-p", "--output-format", "json", *extra_args]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, input=prompt, capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        out, err, code = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        out = e.stdout if isinstance(e.stdout, str) else ""
        err, code = f"timed out after {timeout}s", -1
    meta = {"exit_code": code, "duration_s": round(time.time() - t0, 1),
            "stderr": (err or "")[-2000:]}
    try:
        j = json.loads(out)
        meta.update({k: j.get(k) for k in
                     ("result", "total_cost_usd", "num_turns", "is_error", "subtype")})
    except (json.JSONDecodeError, TypeError):
        meta["result"] = (out or "")[-4000:]
    return meta


def collect(loop, es, ws, tdir):
    """Copy everything the run produced into the trial folder, keeping
    repo-relative paths so the eval set's globs work against it."""
    src = ws / "runs" / loop
    if src.exists():
        shutil.copytree(src, tdir / "runs" / loop, dirs_exist_ok=True)
    for rel in es["run"]["state_paths"]:
        p = ws / rel
        if p.exists():
            (tdir / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, tdir / rel)


# -------------------------------------------------------------- grading

def matches(tdir, globs):
    out = []
    for g in globs:
        out += sorted(Path(x) for x in glob.glob(str(tdir / g)) if Path(x).is_file())
    seen, uniq = set(), []
    for p in out:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def heading_pos(text, title):
    pat = re.compile(r"^[ \t]*(#{1,6}[ \t]+|\*\*)[ \t]*" + re.escape(title), re.I | re.M)
    m = pat.search(text)
    return m.start() if m else -1


def section_body(text, title):
    start = heading_pos(text, title)
    if start < 0:
        return None
    rest = text[start:].split("\n", 1)
    body = rest[1] if len(rest) > 1 else ""
    nxt = re.search(r"^[ \t]*(#{1,6}[ \t]+\S|\*\*[^*\n]+\*\*[ \t]*:?[ \t]*$)", body, re.M)
    return body[:nxt.start()] if nxt else body


def grade_deterministic(c, ctx):
    t = c["type"]
    if t == "gate_passed":
        ok = bool(ctx["gate_files"])
        return ok, ("approved output: " + ", ".join(ctx["gate_files"]) if ok
                    else "no approved output; checker did not pass the draft"
                    + (f" (flags: {', '.join(ctx['flag_files'])})" if ctx["flag_files"] else ""))
    if t == "state_advanced":
        before = ctx["state_before"].replace("\r\n", "\n")
        need = c.get("values", [])
        for rel, txt in ctx["state_after"].items():
            if txt.replace("\r\n", "\n") != before and all(v.lower() in txt.lower() for v in need):
                return True, f"{rel} changed and contains {need}"
        return False, f"no state file changed with {need} (checked {', '.join(ctx['state_after']) or 'none present'})"
    if t == "file_unchanged":
        txt = ctx["state_after"].get(c["path"])
        if txt is None:
            return False, f"{c['path']} missing after run"
        same = txt.replace("\r\n", "\n") == ctx["state_before"].replace("\r\n", "\n")
        return same, f"{c['path']} " + ("unchanged" if same else "was edited")

    text = ctx["state_text"] if c.get("in") == "state" else ctx["output"]
    if not text:
        return False, "no output to grade"
    flags = 0 if c.get("case_sensitive") else re.I
    if t in ("must_contain", "must_not_contain"):
        hay = text if c.get("case_sensitive") else text.lower()
        found = [v for v in c["values"] if (v if c.get("case_sensitive") else v.lower()) in hay]
        if t == "must_contain":
            miss = [v for v in c["values"] if v not in found]
            return not miss, ("all present" if not miss else f"missing {miss}")
        return not found, ("none present" if not found else f"found {found}")
    if t in ("regex", "not_regex"):
        m = re.search(c["pattern"], text, flags | re.M)
        if t == "regex":
            return bool(m), (f"matched {m.group(0)!r}" if m else f"no match for /{c['pattern']}/")
        return not m, ("no match" if not m else f"matched {m.group(0)!r}")
    if t == "heading_order":
        pos = [(v, heading_pos(text, v)) for v in c["values"]]
        miss = [v for v, p in pos if p < 0]
        if miss:
            return False, f"heading(s) not found: {miss}"
        order = [v for v, _ in sorted(pos, key=lambda x: x[1])]
        return order == c["values"], ("in order" if order == c["values"] else f"actual order {order}")
    if t == "section_bullets":
        body = section_body(text, c["section"])
        if body is None:
            return False, f"section '{c['section']}' not found"
        n = len(re.findall(r"^(?:[-*]|\d+\.)\s+\S", body, re.M))
        ok = c.get("min", 0) <= n <= c.get("max", 10**6)
        return ok, f"{n} top-level bullets (want {c.get('min')}-{c.get('max')})"
    raise ValueError(t)


JUDGE_PROMPT = """You are a strict, independent grader for an automated PM report.
You did not write it and you have no stake in it passing.

Answer every question below about the REPORT with pass true or false and
a one-line reason that quotes or points to the report text. Rules:
- Grade only what the report actually says. No partial credit.
- If the report is ambiguous on a question, it fails that question.
- The ANSWER KEY is the ground truth for this case; trust it over the report.

ANSWER KEY
{reference}

QUESTIONS
{questions}

Return ONLY a JSON object, no prose before or after:
{{"results": [{{"id": "<question id>", "pass": true, "reason": "<one line>"}}]}}

REPORT (between the markers)
<<<REPORT
{report}
REPORT>>>
"""


def grade_judge(items, case, ctx, cfg, model):
    if not items:
        return {}
    if not ctx["output"]:
        return {c["id"]: (False, "no output to grade") for c in items}
    qs = "\n".join(f"- {c['id']}: {c['question']}" for c in items)
    prompt = JUDGE_PROMPT.format(reference=case.get("reference", "(none)"),
                                 questions=qs, report=ctx["output"])
    with tempfile.TemporaryDirectory(prefix="loop-eval-judge-") as d:
        meta = run_claude(prompt, d, cfg.get("judge_args", []), 600,
                          model or cfg.get("judge_model"))
    raw = meta.get("result") or ""
    ctx["judge_cost"] = meta.get("total_cost_usd") or 0
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        res = {r["id"]: (bool(r["pass"]), str(r.get("reason", ""))[:300])
               for r in json.loads(m.group(0))["results"]}
    except Exception:
        return {c["id"]: (False, f"judge returned unparseable output: {raw[:200]!r}") for c in items}
    return {c["id"]: res.get(c["id"], (False, "judge gave no answer")) for c in items}


def build_ctx(loop, es, case, tdir, output_file=None, state_file=None):
    run = es["run"]
    if output_file:
        approved, drafts, flagf = [Path(output_file)], [], []
        gate = [Path(output_file)]
    else:
        approved = matches(tdir, run["approved_globs"])
        drafts = matches(tdir, run["draft_globs"])
        flagf = matches(tdir, run.get("flag_globs", []))
        gate = matches(tdir, run.get("gate_globs", run["approved_globs"][:1]))
    graded = approved or drafts[-1:]
    output = "\n\n".join(read(p) for p in graded)
    state_after = {}
    if state_file:
        state_after[run["state_paths"][0]] = read(state_file)
    elif not output_file:
        for rel in run["state_paths"]:
            if (tdir / rel).exists():
                state_after[rel] = read(tdir / rel)
    before = snapshot_text(loop, case)
    changed = [t for t in state_after.values() if t.replace("\r\n", "\n") != before.replace("\r\n", "\n")]
    rel = lambda ps: [str(p.relative_to(tdir)) if tdir in p.parents else str(p) for p in ps]
    return {"output": output, "graded_files": rel(graded), "gate_files": rel(gate),
            "flag_files": rel(flagf), "state_after": state_after,
            "state_before": before, "state_text": "\n\n".join(changed),
            "judge_cost": 0}


def grade(loop, es, case, ctx, cfg, use_judge=True, judge_model=None):
    results = []
    judge_items = [c for c in case["criteria"] if c["type"] == "judge"]
    jres = grade_judge(judge_items, case, ctx, cfg, judge_model) if use_judge else {}
    for c in case["criteria"]:
        if c["type"] == "judge":
            if not use_judge:
                results.append({"id": c["id"], "type": "judge", "pass": None, "reason": "skipped (--no-judge)"})
                continue
            ok, why = jres[c["id"]]
        else:
            ok, why = grade_deterministic(c, ctx)
        results.append({"id": c["id"], "type": c["type"], "pass": ok, "reason": why})
    scored = [r for r in results if r["pass"] is not None]
    return {"criteria": results,
            "passed": sum(1 for r in scored if r["pass"]),
            "scored": len(scored),
            "case_pass": bool(scored) and all(r["pass"] for r in scored),
            "gate_pass": bool(ctx["gate_files"]),
            "graded_files": ctx["graded_files"],
            "judge_cost_usd": ctx.get("judge_cost", 0)}


def print_grade(case_id, g):
    print(f"\n  {case_id}: {g['passed']}/{g['scored']} criteria passed"
          f"{'  (CASE PASS)' if g['case_pass'] else ''}  graded: {', '.join(g['graded_files']) or 'nothing'}")
    for r in g["criteria"]:
        mark = "SKIP" if r["pass"] is None else ("PASS" if r["pass"] else "FAIL")
        print(f"    {mark:4}  {r['id']:<28} {r['reason']}")


# ------------------------------------------------------------- summary

def summarize(loop, es, label, h, trials_by_case, notes):
    summary = {"loop": loop, "label": label, "skill_hash": h,
               "eval_set_version": es.get("eval_set_version"),
               "date": dt.date.today().isoformat(), "cases": {}}
    rows = []
    for cid, trials in trials_by_case.items():
        crit = {}
        for t in trials:
            for r in t["grade"]["criteria"]:
                if r["pass"] is None:
                    continue
                k = crit.setdefault(r["id"], [0, 0])
                k[0] += int(r["pass"])
                k[1] += 1
        n = len(trials)
        passes = sum(1 for t in trials if t["grade"]["case_pass"])
        gates = sum(1 for t in trials if t["grade"]["gate_pass"])
        tot_p = sum(v[0] for v in crit.values())
        tot_n = sum(v[1] for v in crit.values()) or 1
        cost = sum((t["meta"].get("total_cost_usd") or 0) + t["grade"]["judge_cost_usd"] for t in trials)
        failed = ";".join(f"{k}({v[0]}/{v[1]})" for k, v in crit.items() if v[0] < v[1])
        summary["cases"][cid] = {"trials": n, "case_passes": passes, "gate_passes": gates,
                                 "criteria": {k: v for k, v in crit.items()},
                                 "criteria_pass_rate": round(100 * tot_p / tot_n, 1),
                                 "cost_usd": round(cost, 4)}
        rows.append({"date": summary["date"], "label": label, "skill_hash": h, "case": cid,
                     "trials": n, "case_passes": passes,
                     "criteria_pass_rate": round(100 * tot_p / tot_n, 1),
                     "gate_pass_rate": round(100 * gates / n, 1),
                     "failed_criteria": failed, "cost_usd": round(cost, 4), "notes": notes})
    return summary, rows


def append_history(loop, rows):
    p = EVALS / loop / "history.csv"
    new = not p.exists() or p.stat().st_size == 0
    with p.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HISTORY_FIELDS)
        if new:
            w.writeheader()
        w.writerows(rows)


def print_summary(summary):
    print(f"\n== {summary['loop']} | label={summary['label']} | skill={summary['skill_hash']}")
    for cid, s in summary["cases"].items():
        print(f"   {cid}: criteria {s['criteria_pass_rate']}% | case passes {s['case_passes']}/{s['trials']}"
              f" | gate {s['gate_passes']}/{s['trials']} | cost ${s['cost_usd']}")
        for k, (p, n) in s["criteria"].items():
            if p < n:
                print(f"      failing: {k} {p}/{n}")


# ------------------------------------------------------------- commands

def cmd_run(a):
    cfg = load_config()
    es = load_eval_set(a.loop)
    cases = pick_case(es, a.case)
    h = skill_hash(a.loop)
    label = a.label or f"skill-{h}"
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    root = RESULTS / a.loop / label / stamp
    print(f"Running {a.loop} ({len(cases)} case(s) x {a.trials} trial(s)), skill hash {h}")
    print(f"Results: {root}")
    by_case = {}
    for case in cases:
        for i in range(1, a.trials + 1):
            tdir = root / case["id"] / f"trial-{i}"
            tdir.mkdir(parents=True, exist_ok=True)
            ws = make_workspace(a.loop, es, case)
            print(f"\n- {case['id']} trial {i}: running loop in {ws} ...", flush=True)
            try:
                meta = run_claude(es["run"]["prompt"], ws, cfg.get("loop_args", []),
                                  a.timeout, a.model)
                collect(a.loop, es, ws, tdir)
            finally:
                if a.keep_workspace:
                    print(f"  workspace kept: {ws}")
                else:
                    shutil.rmtree(ws, ignore_errors=True)
            (tdir / "run.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
            print(f"  exit {meta['exit_code']}, {meta['duration_s']}s, "
                  f"${meta.get('total_cost_usd') or 0:.2f}, turns {meta.get('num_turns')}")
            ctx = build_ctx(a.loop, es, case, tdir)
            g = grade(a.loop, es, case, ctx, cfg, not a.no_judge, a.judge_model)
            (tdir / "grade.json").write_text(json.dumps(g, indent=2), encoding="utf-8")
            print_grade(case["id"], g)
            by_case.setdefault(case["id"], []).append({"meta": meta, "grade": g})
    summary, rows = summarize(a.loop, es, label, h, by_case, a.notes or "")
    (root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    append_history(a.loop, rows)
    print_summary(summary)
    print(f"\nAppended {len(rows)} row(s) to evals/{a.loop}/history.csv")


def cmd_grade(a):
    cfg = load_config()
    es = load_eval_set(a.loop)
    (case,) = pick_case(es, [a.case])
    ctx = build_ctx(a.loop, es, case, Path("."), a.output, a.state)
    g = grade(a.loop, es, case, ctx, cfg, not a.no_judge, a.judge_model)
    print_grade(case["id"], g)


def cmd_regrade(a):
    cfg = load_config()
    root = Path(a.results_dir).resolve()
    old = json.loads(read(root / "summary.json"))
    loop = old["loop"]
    es = load_eval_set(loop)
    by_case = {}
    for case in es["cases"]:
        for tdir in sorted((root / case["id"]).glob("trial-*")) if (root / case["id"]).exists() else []:
            meta = json.loads(read(tdir / "run.json"))
            ctx = build_ctx(loop, es, case, tdir)
            g = grade(loop, es, case, ctx, cfg, not a.no_judge, a.judge_model)
            (tdir / "grade.json").write_text(json.dumps(g, indent=2), encoding="utf-8")
            print_grade(f"{case['id']} {tdir.name}", g)
            by_case.setdefault(case["id"], []).append({"meta": meta, "grade": g})
    summary, _ = summarize(loop, es, old["label"], old["skill_hash"], by_case, "")
    summary["regraded"] = dt.date.today().isoformat()
    (root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print_summary(summary)
    print("\nhistory.csv not changed by regrade; rerun `compare` to see the effect.")


def latest_summary(loop, label):
    d = RESULTS / loop / label
    runs = sorted(d.glob("*/summary.json")) if d.exists() else []
    if not runs:
        die(f"no results for {loop} label '{label}' under {d}")
    return json.loads(read(runs[-1])), runs[-1].parent


def cmd_compare(a):
    A, pa = latest_summary(a.loop, a.baseline)
    B, pb = latest_summary(a.loop, a.candidate)
    print(f"{a.loop}: baseline '{a.baseline}' (skill {A['skill_hash']}) vs "
          f"candidate '{a.candidate}' (skill {B['skill_hash']})")
    better, worse = [], []
    for cid in sorted(set(A["cases"]) | set(B["cases"])):
        ca, cb = A["cases"].get(cid), B["cases"].get(cid)
        if not ca or not cb:
            print(f"\n  {cid}: only in {'baseline' if ca else 'candidate'}, skipped")
            continue
        print(f"\n  {cid}: criteria {ca['criteria_pass_rate']}% -> {cb['criteria_pass_rate']}% | "
              f"case passes {ca['case_passes']}/{ca['trials']} -> {cb['case_passes']}/{cb['trials']} | "
              f"cost ${ca['cost_usd']} -> ${cb['cost_usd']}")
        for k in list(dict.fromkeys(list(ca["criteria"]) + list(cb["criteria"]))):
            xa, xb = ca["criteria"].get(k), cb["criteria"].get(k)
            ra = xa[0] / xa[1] if xa else None
            rb = xb[0] / xb[1] if xb else None
            if ra is None or rb is None:
                tag = "new" if ra is None else "removed"
            elif rb > ra:
                tag = "BETTER"
                better.append(f"{cid}/{k}")
            elif rb < ra:
                tag = "WORSE"
                worse.append(f"{cid}/{k}")
            else:
                tag = ""
            fa = f"{xa[0]}/{xa[1]}" if xa else "-"
            fb = f"{xb[0]}/{xb[1]}" if xb else "-"
            if tag or a.all:
                print(f"    {k:<28} {fa:>5} -> {fb:<5} {tag}")
    if worse and not better:
        verdict = "REGRESSED"
    elif better and not worse:
        verdict = "IMPROVED"
    elif better and worse:
        verdict = "MIXED: review each WORSE line before shipping"
    else:
        verdict = "NO DETECTABLE CHANGE"
    n = min(min(c["trials"] for c in A["cases"].values()), min(c["trials"] for c in B["cases"].values()))
    print(f"\nVerdict: {verdict}")
    if n < 3:
        print(f"Note: only {n} trial(s) per case. One flipped trial is noise at this size; use --trials 3 or more.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run a loop on its eval cases and grade it")
    r.add_argument("loop")
    r.add_argument("--case", action="append", help="case id (repeatable); default all")
    r.add_argument("--trials", type=int, default=3)
    r.add_argument("--label", help="name for this run, e.g. baseline or my-change (default skill-<hash>)")
    r.add_argument("--notes", help="free text stored in history.csv")
    r.add_argument("--model", help="model for the loop run")
    r.add_argument("--judge-model", help="model for judge criteria")
    r.add_argument("--no-judge", action="store_true", help="skip judge criteria (deterministic only)")
    r.add_argument("--timeout", type=int, default=2400, help="seconds per loop run")
    r.add_argument("--keep-workspace", action="store_true")
    r.set_defaults(fn=cmd_run)

    g = sub.add_parser("grade", help="grade an existing output file against one case")
    g.add_argument("loop")
    g.add_argument("--case", required=True)
    g.add_argument("--output", required=True, help="the report/draft markdown to grade")
    g.add_argument("--state", help="STATE.md after the run (for state criteria)")
    g.add_argument("--judge-model")
    g.add_argument("--no-judge", action="store_true")
    g.set_defaults(fn=cmd_grade)

    rg = sub.add_parser("regrade", help="re-grade a results folder after editing criteria")
    rg.add_argument("results_dir")
    rg.add_argument("--judge-model")
    rg.add_argument("--no-judge", action="store_true")
    rg.set_defaults(fn=cmd_regrade)

    c = sub.add_parser("compare", help="compare the latest runs of two labels")
    c.add_argument("loop")
    c.add_argument("baseline")
    c.add_argument("candidate")
    c.add_argument("--all", action="store_true", help="show unchanged criteria too")
    c.set_defaults(fn=cmd_compare)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
