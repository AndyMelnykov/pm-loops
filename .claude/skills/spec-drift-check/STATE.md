# Spec drift — state

## Last run
- 2026-07-17 / workspace-deletion (CORE-2214): 1 divergence, 1
  changed, 0 cut, 0 added, 0 silent decisions. Flagged/escalated:
  soft delete with 30-day recovery (spec 3.1) shipped as an
  immediate, synchronous, unrecoverable purge (PR #4831); Legal
  (DPA addendum v4, 7) and Priya Nair notified.
- 2026-06-30 / shared-inbox-rules (CORE-2107): 4 divergences — 1 cut,
  2 silent decisions, 1 changed. Flagged: rule-priority ordering
  shipped opposite of spec §4.2.
- 2026-06-11 / sso-scim-provisioning (CORE-2051): 3 divergences —
  2 silent decisions, 1 added. Nothing escalated.

## Accepted deviations (do not re-flag)
- 2026-07-06 / workspace-deletion (CORE-2214), spec §3.4: deletion
  notification email goes to workspace **owners only**, not all
  admins. Spec says all admins; Priya accepted the narrower audience
  on 2026-07-02 after beta feedback that the admin blast was noisy.
  Decision logged in CORE-2214 comment thread. Intentional deviation —
  exclude from future drift reports unless the recipient set changes
  again.

## Pattern log
- Silent decisions: seen shared-inbox-rules (2026-06-30),
  sso-scim-provisioning (2026-06-11). 2 consecutive reports — call as
  process pattern if it appears in a 3rd consecutive report. Streak
  broken by workspace-deletion (2026-07-17), which had 0 silent
  decisions; count stays at 2, not yet a declared pattern.

## Lessons learned
- 2026-06-12: help doc lagged release by 6 days on sso-scim; a shipped
  requirement read as cut. Rule added: check source dates vs release
  date before marking cut scope.
- 2026-07-01: re-flagged an already-accepted deviation on
  shared-inbox-rules. Rule added: cross-check accepted deviations in
  this file before writing each finding.

