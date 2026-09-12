# Weekly business review — state

## Watch items

- trial_to_paid_conversion — flagged on the 2026-06-29, 2026-07-06,
  2026-07-13, and 2026-07-20 runs (week of 2026-06-22: 16.2%,
  -12.0% vs prior week; 2026-06-29: 14.8%, -8.6%; 2026-07-06: 14.5%,
  -13.8% vs 4-week avg 16.83%; 2026-07-13: 14.1%, -11.7% vs 4-week
  avg 15.975%). Week 4. Write the next appearance as a continuing
  trend, week 5 — not fresh news.
- support_ticket_volume — flagged on the 2026-07-20 run (week of
  2026-07-13: 842, +31.6% WoW vs 640, +35.6% vs 4-week avg 620.75).
  Week 1 (new). Root cause: Salesforce connector timeout (RELAY-1206),
  fix tracked in RELAY-1205, in code review. If flagged again next
  run, write as continuing, week 2.

## Last run

- 2026-07-20 (week of 2026-07-13): new_trials 461, trial_to_paid
  14.1% (FLAG, watch week 4), weekly_active_accounts 5512,
  ai_assist_adoption 32.4%, net_new_arr $158k, churned_arr $34k,
  support_ticket_volume 842 (FLAG, new, watch week 1), api_uptime
  99.96%, nps UNAVAILABLE (source data/weekly-business-review/
  nps-export.csv not found). Flags raised: trial_to_paid_conversion
  (continuing, week 4), support_ticket_volume (new, week 1).
  Unavailable sources: nps (nps-export.csv not found).

## Delivery preference

- Not yet asked. After this PASS, ask the user whether they want the
  WBR delivered automatically each week (e.g. Slack, email, or
  another channel) instead of only landing as a markdown file under
  runs/weekly-business-review/, and record their answer here so
  future runs don't ask again once it's set.

## Lessons learned

- 2026-06-22: NPS export missing, row silently dropped, review
  shipped one metric short. Fix: fixed row count — every listed
  metric appears as a number or an UNAVAILABLE flag (rule added to
  SKILL.md).
- 2026-07-06: callout used "down roughly a fifth" with no source
  numbers. Fix: every callout cites exact values from the export
  (rule added to SKILL.md).
