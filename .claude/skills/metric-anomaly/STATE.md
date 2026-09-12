# Metric anomaly: state

## Open flags

- api_error_rate: OPENED 2026-07-15 run (data day 2026-07-14).
  Now SUSTAINED as of the 2026-07-16 run (day 3: 2026-07-14,
  2026-07-15, 2026-07-16 all crossed vs the 0.464% clean baseline,
  07-09 through 07-13). Candidate cause: deploy v2.31.0
  (payments-api, 2026-07-13 17:40 PT), new retry logic on the
  payments gateway client. Status: SUSTAINED, day 3.
  Baseline rule: exclude 2026-07-14, 2026-07-15, and 2026-07-16
  from the 7-day rolling average until this flag is closed.
- checkout_conversion: OPENED 2026-07-16 run (data day 2026-07-16).
  Crossed: 2.80% vs 3.150% clean 7-day baseline (07-09 through
  07-15), -11.1%. Candidate cause: deploy v2.31.0 (payments-api,
  2026-07-13 17:40 PT), checkout service refactor. Status: OPEN,
  day 1. Baseline rule: exclude 2026-07-16 from the 7-day rolling
  average until this flag is closed.

## Last run

- 2026-07-16 (evaluating data through 2026-07-16; also recomputed
  2026-07-15, which had no logged maker run): api_error_rate
  escalated to SUSTAINED, day 3 (0.95% vs 0.464% clean baseline,
  +104.7%; 07-14 and 07-15 also crossed at +296.6% and +182.3%
  respectively against the same clean baseline). checkout_conversion
  crossed for the first time (2.80% vs 3.150% clean baseline,
  -11.1%), new flag opened, day 1. Both hypotheses name deploy
  v2.31.0 (payments-api, checkout refactor plus payments gateway
  retry logic) as candidate cause. No other metric crossed;
  activation_rate (-4.31%) and p95_latency (+5.47%) logged as
  watch near-misses, not flags. Output saved to
  runs/metric-anomaly/2026-07-16.md.

## Pattern log

- api_error_rate: flagged 2026-07-14, 2026-07-15, 2026-07-16.
  Sustained shift as of 2026-07-16 (3 consecutive days). Exclude
  flagged days from baseline until closed.
- checkout_conversion: flagged 2026-07-16. Escalate as sustained
  shift at 3 consecutive days. Exclude flagged days from baseline
  until closed.

## Lessons learned

- 2026-05-19: bot-wave signup spike got absorbed into the 7-day
  average and masked a real dip. Fix: exclude flagged days from
  the baseline until the flag is closed (rule added to SKILL.md).

