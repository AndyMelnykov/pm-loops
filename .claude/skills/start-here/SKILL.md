---
name: start-here
description: Onboards a new PM into the loop pack. Scans their connected tools, picks the one loop that will work with what they already have, sets it up, and runs it so they see their first output this session. Triggers when a new user opens this repo, asks how to start, what this is, or which loop to pick — and always when LOOPS.md does not exist yet.
---

# First-run onboarding

Goal: the user sees a real loop output THIS SESSION. Not a tour, not a menu of 12. One loop, set up, run, output on screen. Push toward that; don't ask permission to begin — begin.

## Step 1 — Scan what they have (before saying much)

Check what's actually connected, in this order:

1. **MCP tools.** Look at the available/deferred tool list for connected servers: Slack, Notion, Linear/Jira, Google Drive, Gmail, analytics (Amplitude/Mixpanel/PostHog), CRM (Salesforce/HubSpot/Attio). Don't ask "what tools do you use" — read the list.
2. **Local data.** Anything the user has dropped in this folder or mentions having: exports, CSVs, a PRD draft, a strategy doc.
3. **Nothing connected?** That's fine — every loop ships with realistic fixtures in `data/`. Demo mode is the fallback, never a dead end.

## Step 2 — Match sources to ONE loop

Recommend exactly one. Tie-break by what needs zero extra setup, then by fastest visible payoff. Matching table:

| They have | Recommend | Why it works day one |
|---|---|---|
| Slack (support/feedback channels) or interview notes | feedback-digest | Read channels/notes directly, tag against taxonomy |
| CRM or deal notes in Notion/Drive | sales-deal-intelligence | One week of pipeline is enough for the first brief |
| Linear/Jira + a spec doc | spec-drift-check | Tickets vs spec, one feature |
| Linear/Jira backlog before planning | sprint-prep-sweep | One backlog export, prep report in minutes |
| Analytics MCP or metric CSV exports | metric-anomaly or weekly-business-review | Daily numbers + thresholds, output tomorrow morning |
| A PRD, one-pager, or launch doc | product-review-hardening | Runs once on their real doc, findings in minutes |
| Competitor names only (nothing connected) | competitive-brief | Web sources, needs only URLs |
| Nothing at all | any, on bundled fixtures | `data/<loop>/` is realistic; show, then connect |

If several match, say which one you picked and why in one sentence — don't present the table.

## Step 3 — Offer the run, then run it

Say, concretely: "**[Loop X] will work with your [source]. Shall I run it now so you can see the output?**" On yes:

- **Real data available:** copy the loop's skill from `.claude/skills/<loop>/`, rewrite SKILL.md's sources to their real MCP sources or files (ask at most 2-3 questions — e.g. which Slack channels, which competitor URLs, which thresholds; propose defaults so they can just say yes). Reset STATE.md to empty template. Then run MAKER.md as one agent, CHECKER.md as a separate agent, and show them the output file.
- **Fixtures only:** the one-line offer above is the ONLY question. On yes, run the loop as-is on `data/<loop>/` — no further questions — show the output, THEN say "that was demo data; connect [tool] or drop your export in `data/` and the same loop runs on yours."

Run mechanics, both branches: outputs go to `runs/<loop>/` (drafts, approved output, flags) — never touch `evals/` or eval artifacts if present. If the checker FLAGS the draft, don't surface the failure to the user mid-demo: hand the exact flags back to the maker to fix, then run a FRESH checker on the revised draft; mention the catch afterward as a feature ("the checker caught X before you saw it"). Demo runs append to STATE.md marked "(demo)"; when they later connect real sources, clear the demo entries so real baselines start clean.

The output on screen is the onboarding. Walk them through it in 3 bullets max: what it found, what the checker verified, where state was written.

## Step 4 — Register and schedule

After the first successful run:

1. Create/update `LOOPS.md` at repo root: table of active loops — name, sources, trigger, last run, status. This file existing = onboarding done; never re-run this flow when it exists.
2. Give them the ONE command to make it recurring (scheduled task with their cron line, per README) and the headless-auth warning.
3. Tell them the human rule: the loop drafts, they judge. First week: read every output, disagree with one thing per output, write corrections into the skill's Known failure modes.
4. Stop. Do not pitch the other 11 loops. One line: "When this one's running for a week, ask me for the next loop."

## Failure handling

- MCP source unreachable/permission denied → fall back to fixtures for the demo, note what to connect, still deliver an output this session.
- User wants a different loop than recommended → fine, same flow, their pick.
- User says "just explain it" → two sentences + "fastest way to understand is to see one run — 90 seconds, shall I?"
