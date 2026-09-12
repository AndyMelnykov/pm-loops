# Stale doc sweep — state

## Last run
- 2026-07-17: 8 docs swept, 4 flags raised (1 chronic escalation, 1 carried over, 2 new), 1 resolved. Draft passed checker on first pass.
- 2026-06-01: 8 docs swept, 3 flags raised (2 carried over from 2026-05-04, 1 new). Draft passed checker on first pass.

## Pattern log
- data/stale-doc-sweep/docs/reporting-guide.md, claim: "Export CSV" button at the top right of the Reports page: flagged 2026-05-04, 2026-06-01, 2026-07-17. CHRONIC (3rd consecutive sweep) as of 2026-07-17, escalated to owner. Owner: Miguel Torres. Still unfixed.
- data/stale-doc-sweep/docs/onboarding-guide.md, claim: Growth plan at $49/user/month: flagged 2026-06-01, 2026-07-17. CARRIED-OVER (2nd consecutive sweep) as of 2026-07-17. Owner: Priya Raman. Still unfixed.
- data/stale-doc-sweep/docs/onboarding-guide.md, claim: unlimited Inbox Rules and SLA policies: flagged 2026-07-17 (NEW). Owner: Priya Raman. Still unfixed.
- data/stale-doc-sweep/docs/new-hire-faq.md, claim: find them under Settings > Inbox Rules (routing described via old "Inbox Rules" name): flagged 2026-07-17 (NEW). Owner: Priya Raman. Still unfixed.
- data/stale-doc-sweep/docs/support-playbook.md, claim: "configure Inbox Rules to auto-route by keyword": flagged 2026-06-01, RESOLVED as of 2026-07-17 (doc updated by 2026-07-01 to say "Automations"). Owner: Dana Okafor.

## Lessons learned
- 2026-05-04: flagged security-overview.md purely for its 2024 date; owner pushed back, it is marked evergreen and policy-level. Rule added: never flag on date alone; evergreen-headed docs need a direct changelog contradiction.
- 2026-06-01: new-hire-faq.md headings changed after a reorg and two flags were double-counted. Rule added: match prior flags by quoted claim, not section heading.
- 2026-07-17: SKILL.md, MAKER.md, and CHECKER.md updated to require every report open with a plain-language summary (3-5 sentences, no jargon, stale-doc count, single most important next action) above the header, and to forbid em dashes anywhere in report output. Both are now checker criteria (10 and 11). Applied and verified on this run.

