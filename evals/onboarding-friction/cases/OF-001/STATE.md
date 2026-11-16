# Onboarding monitor — state

## Last run
- 2026-07-06: No new flags. Connect data source at 15.5% vs 14.5% baseline (+1.0, under threshold — noted as a watch item). Invite team at 41.0%, at its known structural baseline. Ticket volume 13 vs 4-week avg 12 (normal). Source health: funnel + support both fresh; session-notes.md already >30 days old, excluded from current-state evidence.

## Pattern log
- Invite team: structurally high drop-off (~40-42%) for the full history of this monitor. Confirmed by UX research (session-notes.md): skipping the invite step is deliberate solo-evaluation behavior, not friction. Known baseline — do NOT flag as new degradation unless it exceeds 41.5% baseline by more than 3 points. Escalate as sustained only at 3 consecutive weeks above that.
- Connect data source: watch item since 2026-07-06 run (+1.0 over baseline, under the 3-point threshold). Escalate to a flag if it crosses threshold; sustained only at 3 consecutive flagged weeks.

## Lessons learned
- 2026-04-14: Funnel export renamed "Step 5: Invite" to "Invite team"; step vanished from report. Rule added: match steps by position AND fuzzy name for 2 weeks after any rename.
- 2026-05-18: Used stale session notes as if current and drew a wrong conclusion. Rule added: 30-day freshness gate on every source's own dated header.
