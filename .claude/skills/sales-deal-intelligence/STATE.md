# Sales deal intelligence — state

## Last run
- 2026-07-17: deals covered, 5 open (NW-1051, NW-1054, NW-1057,
  NW-1058, NW-1060), 5 closed (NW-1044 lost 2026-07-13, NW-1046 won
  2026-07-14, NW-1048 lost 2026-07-15, NW-1049 won 2026-07-16,
  NW-1050 lost 2026-07-16), 2 flagged insufficient-data (NW-1062
  open: intro call was small talk only; NW-1063 closed: RevOps
  auto-close, no loss reason, no notes, contact dark since April).
  NW-1044 cited: features (deciding), competition, champion
  strength; not cited: price, timing. NW-1046 cited: price
  (non-deciding), features (deciding), competition, champion
  strength (deciding); not cited: timing. NW-1048 cited: features
  (non-deciding), competition, timing (deciding); not cited: price,
  champion strength. NW-1049 cited: features (deciding), champion
  strength (deciding); not cited: price, competition, timing. NW-1050
  cited: price (non-deciding), features, competition, champion
  strength; not cited: timing. Features hit 3+ consecutive on
  2026-06-30 and is still running, now at 7 with no break.
  Competition hit 3+ this week (NW-1044 through NW-1048) then broke
  at NW-1049 (no competitor cited); now at 1. Champion strength is
  at 2 consecutive (NW-1049, NW-1050), one citation from its first
  alert.

- 2026-07-10: deals covered — 7 open, 2 closed (NW-1036 lost
  2026-06-30, NW-1042 lost 2026-07-08), 0 flagged. NW-1036 cited:
  price (non-deciding), features, competition, champion strength;
  not cited: timing. NW-1042 cited: price (non-deciding), features,
  competition; not cited: timing, champion strength. Competition and
  features both at 2 consecutive — one more citation reaches alert
  threshold.
- 2026-07-03: deals covered — 8 open, 1 closed (NW-1029 lost
  2026-06-05, processed late after CRM backfill). NW-1029 cited:
  features, competition, timing; not cited: price, champion
  strength.

## Pattern log
- competition: cited in closed deals NW-1036, NW-1042, NW-1044
  (2026-07-13, lost to Cortexa), NW-1046 (2026-07-14, lost to
  FreightIQ), NW-1048 (2026-07-15, lost to Cortexa); hit 3+ at
  NW-1044, peaked at 5 through NW-1048; broke at NW-1049 (no
  competitor). NW-1050 (2026-07-16, lost to Cortexa) cited. Current:
  1 consecutive (NW-1050). Alert at 3.
- features: cited in NW-1036, NW-1042, NW-1044, NW-1046, NW-1048,
  NW-1049, NW-1050, no break since 2026-06-30. Current: 7
  consecutive. Alert at 3 (standing hit, still active).
- price: cited in NW-1036, NW-1042 (non-deciding both), then broken
  at NW-1044 (never got there), cited at NW-1046 (non-deciding),
  broken at NW-1048 (decoy: budget referred to timing, not price),
  not cited at NW-1049 (affirmative "took list, no discount asked"),
  cited at NW-1050 (non-deciding). Current: 1 consecutive (NW-1050).
  Alert at 3.
- timing: last cited NW-1029 (2026-06-05); broken by NW-1036; not
  cited NW-1042, NW-1044, NW-1046; cited at NW-1048 (2026-07-15,
  migration-deadline decider); broken by NW-1049; not cited NW-1050.
  Current: 0 consecutive. Alert at 3.
- champion strength: cited in NW-1036 only, broken by NW-1042
  (current 0 per 2026-07-10 correction); cited at NW-1044
  (2026-07-13, weak/solo champion) and NW-1046 (2026-07-14, Mei Lin,
  deciding), broken by NW-1048 (not discussed), cited at NW-1049
  (2026-07-16, Deb, deciding) and NW-1050 (2026-07-16, split
  champion). Current: 2 consecutive (NW-1049, NW-1050). Alert at 3,
  one citation away.

## Lessons learned
- 2026-07-03: a PM assist promised a connector "on the near-term
  roadmap." Rule added to SKILL.md known failure modes and the
  no-commitments rule hardened.
- 2026-07-10: an auto-closed no-activity deal was fully tagged from
  stage history alone. Fix: insufficient-data flag, excluded from
  streak arithmetic. Rule added to SKILL.md.
- 2026-07-17: added a hard formatting rule (no em dash anywhere in
  output, checker scans for it) and a VP-of-Product voice/format bar
  (tables, Bottom Line block, bold key figures, no unsupported
  adjectives or hedging). NW-1063 (Quayside) was another RevOps
  auto-close with no loss reason; correctly flagged insufficient-data
  and excluded from streak arithmetic rather than repeating the
  2026-07-10 mistake.
