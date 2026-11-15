# Metric anomaly: state

## Open flags

- api_error_rate: OPENED 2026-07-15 run (data day 2026-07-14).
  Crossed: 1.84% vs 0.461% 7-day baseline (07-07 through 07-13),
  +298.8%. Candidate cause: deploy v2.31.0 (payments-api,
  2026-07-13 17:40 PT), new retry logic on the payments gateway
  client. Status: OPEN, day 1, not yet sustained.
  Baseline rule: exclude 2026-07-14 from the 7-day rolling average
  until this flag is closed.

## Last run

- 2026-07-15 (evaluating data through 2026-07-14): api_error_rate
  crossed for the first time (1.84% vs 0.461% baseline, +298.8%),
  new flag opened, day 1. Candidate cause: deploy v2.31.0
  (payments-api). No other metric crossed; p95_latency (+8.79%)
  logged as a watch near-miss, not a flag. Output saved to
  runs/metric-anomaly/2026-07-15.md.

## Pattern log

- api_error_rate: flagged 2026-07-14. Escalate as sustained shift at
  3 consecutive days. Exclude flagged days from baseline until closed.

## Lessons learned

- 2026-05-19: bot-wave signup spike got absorbed into the 7-day
  average and masked a real dip. Fix: exclude flagged days from
  the baseline until the flag is closed (rule added to SKILL.md).
