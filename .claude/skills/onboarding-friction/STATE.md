# Onboarding monitor — state

## Last run
- 2026-07-06: No new flags. Connect data source at 15.5% vs 14.5% baseline (+1.0, under threshold — noted as a watch item). Invite team at 41.0%, at its known structural baseline. Ticket volume 13 vs 4-week avg 12 (normal). Source health: funnel + support both fresh; session-notes.md already >30 days old, excluded from current-state evidence.
- 2026-07-17 (data week 2026-07-06): 2 flags. Connect data source at 19.20% vs 14.5% baseline (+4.70), escalated from last run's watch item, 1st consecutive flagged week. Onboarding ticket volume at 27 vs 4-week avg 12 (2.25x), new flag; 14 of 27 tickets (51.85%) tagged connect-data + confusing-setup, the common driver of both flags. Invite team at 42.76% vs 41.5% baseline (+1.26), not flagged, structural per pattern log. Source health: funnel-2026-07-06.csv, baseline-8week.csv, support-onboarding-2026-07-06.csv all 4 days old (fresh); funnel-2026-06-29.csv and support-onboarding-2026-06-29.csv 11 days old (fresh); session-notes.md 44 days old (stale, excluded from current-state evidence, used only as disclosed historical context).

## Pattern log
- Invite team: structurally high drop-off (~40-42%) for the full history of this monitor. Confirmed by UX research (session-notes.md): skipping the invite step is deliberate solo-evaluation behavior, not friction. Known baseline — do NOT flag as new degradation unless it exceeds 41.5% baseline by more than 3 points. Escalate as sustained only at 3 consecutive weeks above that.
- Connect data source: watch item since 2026-07-06 run (+1.0 over baseline); crossed the 3-point threshold on the 2026-07-17 run (+4.70) and is now flagged, 1st consecutive flagged week. Escalate to sustained if flagged 3 consecutive weeks running.

## Lessons learned
- 2026-04-14: Funnel export renamed "Step 5: Invite" to "Invite team"; step vanished from report. Rule added: match steps by position AND fuzzy name for 2 weeks after any rename.
- 2026-05-18: Used stale session notes as if current and drew a wrong conclusion. Rule added: 30-day freshness gate on every source's own dated header.
