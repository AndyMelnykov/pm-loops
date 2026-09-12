# Connecting real data sources

Every loop ships pointed at bundled fixtures in `data/<loop-name>/` so you get a real
output on day one with nothing connected. This doc is what to do next: swap fixtures
for your actual Slack, Notion, Linear, CRM, or analytics data.

If you haven't run a loop yet, don't start here — say "get me started" and the
`start-here` skill does the first connection for you (2-3 questions, one real run).
Come back here when you're connecting the 2nd loop, connecting a source start-here
didn't ask about, or you just want to see the exact commands before you're mid-onboarding.

## The one thing that changes

A loop is six pieces (trigger, skill file, maker, checker, gate, state). Connecting a
real source touches exactly one of them: the **`## Sources`** section (or its
loop-specific equivalent — "Metrics watched," "Feature under review," etc.) near the
top of `.claude/skills/<loop-name>/SKILL.md`. Nothing else changes — not the taxonomy,
not the checker criteria, not the output format. If you find yourself editing the
maker/checker logic just to "make the real data work," stop — that's a sign the source
data doesn't actually match what the loop expects, not a reason to weaken the loop.

Every fixture path in every shipped `SKILL.md` is a stand-in for one of three source
shapes:

| Shape | Example in this repo | What "connecting" means |
|---|---|---|
| **Local file** | `data/competitive-brief/week-.../slotwise-changelog.md` | Point the path at your real export/doc, refreshed on the loop's cadence |
| **MCP-connected tool** | Slack channels, a Linear backlog, a CRM pipeline | Connect the tool once (`claude mcp add ...`), then describe the live query in `SKILL.md` (e.g. "the #support-escalations channel, last 7 days") instead of a file path |
| **Web source** | `competitive-brief`'s changelog/blog URLs | No MCP needed — give the maker the real URLs; it reads them directly |

## Step by step

1. **Check what's already connected.** `claude mcp list` in this repo, or just ask
   Claude — `start-here` does this scan automatically the first time.
2. **Connect the tool, if it isn't yet.** One `claude mcp add` command per tool (exact
   commands below). Most of these are OAuth: the first connection opens a browser to
   sign in, then Claude Code caches the token.
3. **Authenticate once, interactively.** Run `/mcp` in a normal (non-headless) session
   and complete the OAuth flow before you ever try this loop from cron. A headless
   `claude -p --bare` run cannot open a browser — it needs the token already cached (or
   an API-key/PAT-based server, which skips OAuth entirely; noted per-tool below).
4. **Edit that one skill's `SKILL.md` Sources section.** Replace the fixture path(s)
   with either a real file path or a plain-English description of the live query. Leave
   everything else in the file untouched.
5. **Reset `STATE.md`.** Copy the empty template pattern already in that file (or ask
   Claude to do it) so real baselines don't inherit fixture history — a Monday brief
   that "notices a 3rd-consecutive-week trend" made of two fixture weeks and one real
   week is a false trend.
6. **Do one real run by hand** before you schedule it: run MAKER.md, then CHECKER.md as
   a separate invocation, and read the checker footer. Confirm the cited file paths or
   source names are your real tool, not `data/<loop-name>/` — a silent fallback to
   fixtures is the most common way a "connected" loop quietly stays a demo.
7. **Schedule it.** See the README's "Running locally" section for `claude -p --bare`
   vs `/loop` vs event triggers, and the headless-auth gotcha (an API key in the
   scheduler's environment; OAuth tokens cached from step 3 usually carry over, but
   verify with a real scheduled run once before trusting it unattended).

## Per-tool connection commands

These are the official, currently-documented remote MCP servers for the tools this
pack's loops reference most. Endpoints and auth flows do change — if a command below
stops working, check that vendor's own MCP/integrations doc before assuming the tool
has no MCP server.

General syntax: flags go before the server name; `--` separates Claude's own flags from
a local (stdio) server's launch command.

```
claude mcp add --transport http <name> <url>                    # remote server (OAuth, usually)
claude mcp add --transport http <name> <url> --header "Authorization: Bearer <token>"  # token-auth remote server
claude mcp add <name> -- <command> [args...]                     # local (stdio) server
```

| Tool | Command | Auth | Headless-safe? |
|---|---|---|---|
| **Notion** | `claude mcp add --transport http notion https://mcp.notion.com/mcp` | OAuth (run `/mcp` once) | After first login, yes |
| **Linear** | `claude mcp add --transport http linear-server https://mcp.linear.app/mcp` | OAuth | After first login, yes |
| **Slack** | `claude mcp add --transport http slack-mcp-server https://mcp.slack.com/mcp` | OAuth, needs workspace admin approval once | After first login, yes |
| **Jira / Confluence (Atlassian)** | `claude mcp add atlassian --transport http https://mcp.atlassian.com/v1/mcp/authv2` | OAuth 2.1 or API token | Yes, especially with an API token |
| **GitHub** | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer <PAT>"` | Personal access token (fine-grained, at github.com/settings/personal-access-tokens/new) | Yes — token-based, no browser step |
| **HubSpot** | `claude mcp add --transport http hubspot https://mcp.hubspot.com/anthropic` | OAuth | After first login, yes |
| **Salesforce** | Hosted MCP: OAuth URL from Salesforce's own Hosted MCP setup page (org-specific, so there's no fixed URL to paste here). Local alternative: `@salesforce/mcp` npm package via stdio. | OAuth (hosted) or your org's CLI auth (local) | Local `@salesforce/mcp` is generally easier to run unattended |
| **PostHog** | `claude mcp add --transport http posthog https://mcp.posthog.com/mcp` (EU: `https://mcp-eu.posthog.com/mcp`) | Personal API key (see PostHog's MCP docs for the header format) | Yes — API-key based |

Not in the table because there's no clean official MCP path yet, as of this writing:

- **Gmail** — the current Google-hosted Gmail MCP has a known bug routing through the
  wrong OAuth client, so it can't actually grant Gmail scopes. Until that's fixed,
  export what you need (a thread, a digest) to a file under `data/<loop>/` instead of
  wiring Gmail live.
- **Amplitude, Mixpanel** — no official remote MCP server found at time of writing.
  Use their CSV/API export on the loop's cadence and point the Sources path at that
  file; this is exactly the shape `metric-anomaly` and `weekly-business-review`
  already expect.
- **App Store / Play Store reviews, NPS tools (Delighted, Wootric), Gong** — same:
  export on a cadence, point the fixture path at the real export. `feedback-digest`'s
  Sources section is already written as a list of file paths for this reason.

## Where each loop's sources map to real tools

| Loop | Fixture shape today | Realistic real source |
|---|---|---|
| `competitive-brief` | competitor changelog/blog snapshots (.md) | Real competitor URLs — no MCP, just real links |
| `feedback-digest` | tickets/reviews/NPS CSVs, sales notes, interview notes | Zendesk/Intercom export, Slack, Notion, App/Play Store export, NPS tool export |
| `sales-deal-intelligence` | deals CSV, AE/SE notes | Salesforce or HubSpot MCP (deals), Gong/Notion (notes) — already noted inline in its `SKILL.md` |
| `weekly-business-review` | metrics export | PostHog/warehouse export; Jira/Linear MCP for epic status |
| `spec-drift-check` | spec doc, merged-PRs digest | Notion/Confluence (spec), GitHub MCP (PRs/commits) |
| `launch-readiness` | checklist, PRD, help doc, macros, pricing copy, analytics events, rollback plan | Notion/Confluence, Zendesk macros export, GitHub, PostHog events |
| `product-review-hardening` | review-bound doc | Notion/Confluence/Google Docs export |
| `sprint-prep-sweep` | backlog export (JSON) | Linear MCP or Atlassian MCP (Jira) — already noted inline in its `SKILL.md` |
| `stale-doc-sweep` | docs dir, changelog, pricing doc | Notion/Confluence/GitHub wiki, GitHub releases |
| `metric-anomaly` | daily metrics CSV, changes log | PostHog export, GitHub/Linear deploy log |
| `onboarding-friction` | funnel/baseline/support CSVs, session notes | PostHog funnels, Zendesk/Intercom export |
| `ai-quality-watchdog` | eval set + live-output JSON | Stays file-based by design — this is your own eval harness output, not a third-party tool |

## Worked example: feedback-digest with a real Slack channel

Before (`.claude/skills/feedback-digest/SKILL.md`):

```
## Sources
- Support tickets: data/feedback-digest/support-tickets-2026-07-17.csv
- Sales notes: data/feedback-digest/sales-notes/2026-07-17.md
...
```

After connecting Slack (`claude mcp add --transport http slack-mcp-server
https://mcp.slack.com/mcp`, then `/mcp` to authorize):

```
## Sources
- Support tickets: #support-escalations and #support-general on Slack, messages
  from the last 7 days (via the Slack MCP connection)
- Sales notes: data/feedback-digest/sales-notes/2026-07-17.md
...
```

Only the one line changed. The theme taxonomy, counting rule, and checker criteria
below it are untouched.

## Confirming it's actually connected, not quietly demo-ing

The single most common failure is a loop that silently falls back to fixtures on a
permission error and reports success anyway. Before trusting a scheduled run:

- Read the checker footer of your first real run — it should cite your real tool
  (a Slack channel name, a Linear issue ID, a Salesforce deal ID), never a `data/`
  path.
- If a source is unreachable, `start-here`'s failure handling falls back to fixtures
  for demos — that's correct behavior during onboarding, but wrong for a scheduled
  loop. A scheduled run that can't reach its real source should flag, not silently
  demo.
- Re-run once from the exact headless command you'll schedule
  (`claude -p --bare "/skill-name"`) before trusting the cron line — OAuth tokens and
  API keys don't always inherit into a scheduler's environment the way they do in your
  interactive terminal.
