# AI watchdog — state

## Last run
- 2026-07-15: pass rate 86.7% (26/30). Failures: EX-007 (claimed Enterprise free trial, 3rd consecutive night), EX-022 (omitted AES-256), EX-024 (said admins can view all boards), EX-029 (pointed to public issue tracker). No alert fired: 7-day average was 89.5%, drop under 5 points. Flag raised: EX-007 hit 3 consecutive nights — escalate as confirmed regression on next failing run.

## Pattern log
- EX-007: failing since 2026-07-13 (3 consecutive nights: 07-13, 07-14, 07-15). Same failure every night: answer claims Enterprise has a 14-day free trial; it does not. Suspected cause: pricing-page prompt edit shipped 07-13. Escalate at 3 consecutive nights — threshold met; next failure must be reported as a confirmed regression, not a new failure.
- EX-024: intermittent (failed 4 of last 7 nights, never 3 in a row). Nuanced admin-permissions answer. Keep on watch; do not escalate yet.
- EX-019: failed once (07-11, truncation), passed since. Known to be latency-sensitive.

## Lessons learned
- 2026-07-02: Live feature timed out on 4 examples and they were scored FAIL. Rule added: timeouts are "no result," not failures — retry once, then flag the run as incomplete.
- 2026-07-10: EX-022 fails when the answer says "industry-standard encryption" without naming AES-256. Criteria are literal; do not give partial credit.
