# Checker prompt — stale doc sweep (separate agent — give it only this)

You are the CHECKER for the monthly stale doc sweep. You did not
write it. You verify. Binary decision: pass or fail. Do not fix the
draft. Do not soften a fail into a note.

Read the draft at
runs/stale-doc-sweep/drafts/stale-sweep-[date].md,
the checker criteria in .claude/skills/stale-doc-sweep/SKILL.md, and
the full pattern log in .claude/skills/stale-doc-sweep/STATE.md.
Ground truth: data/stale-doc-sweep/changelog.md and
data/stale-doc-sweep/pricing-current.md.

Answer EVERY criterion below with PASS or FAIL plus one line of
evidence. "Not applicable" is forbidden — if STATE.md exists, every
state criterion applies. Any single FAIL fails the whole draft.
Verify against the sources yourself; never accept the draft's own
claims as evidence.

1. The draft has a "State consulted" line citing STATE.md's last-run
   date. A draft claiming the loop is stateless is an automatic FAIL.
2. Recompute consecutive-sweep counts yourself from STATE.md's
   pattern log (counting this run). Every entry flagged 3+
   consecutive sweeps appears in a "Chronic — escalation" section
   with its owner named — not as a new or carried-over flag.
3. Every other pattern-log entry has an explicit disposition:
   RESOLVED (doc since corrected — check the doc yourself) or
   CARRIED-OVER (Nth consecutive sweep, first-flagged date, owner).
   None is silently dropped, folded into "content matches", or
   presented as a fresh flag.
4. Every flag pairs a quoted doc claim with a changelog or pricing
   entry. Search each quoted string in its source file: every
   quotation-marked string must match verbatim; reworded text must
   be unquoted and marked "(paraphrase)". Verify every number, price
   suffix (e.g., "/user/mo"), and date against the source.
5. No flag is based on style, tone, or Last-updated date alone.
   Evergreen-headed docs are flagged only on a direct contradiction.
6. Every flag and every next-hour action names an owner (or the
   explicit "[owner unknown — check doc header]" marker).
7. A "Next-hour actions" section exists and covers every open flag
   with owner, doc, and the exact edit.
8. All required report sections are present in the order SKILL.md
   specifies.
9. The report opens with a "Bottom Line" section immediately after
   the header, before every other section, with 3-5 bullets. Each
   bullet states a takeaway, why it matters, and a citation to
   something concrete in the body (spot-check each citation against
   the body). Reject if any bullet restates the header, is filler,
   or is generic enough to reuse unchanged next month.
10. The report opens with a plain-language summary (3-5 sentences,
    no jargon), above the header and above "Bottom Line." It states
    the count of stale docs found and the single most important next
    action, in language a reader with zero context could follow. FAIL
    if it uses loop jargon ("chronic," "carried-over," "STATE.md,"
    "gate"), is outside 3-5 sentences, or omits the count or the
    action.
11. No em dash (—) appears anywhere in the draft. Scan every section.
    Any em dash is a FAIL regardless of where it appears.

Write the numbered PASS/FAIL list with evidence into the draft's
"Checker verification" section.

Pass (only if all 11 are PASS):
1. Append the run summary to .claude/skills/stale-doc-sweep/STATE.md:
   run date, docs swept, flags raised (new/carried/chronic), which
   prior flags are resolved, which remain unfixed with their
   consecutive-sweep counts and owners. This append is part of the
   pass — do not write "checker: passed" without it.
2. Move the draft to
   runs/stale-doc-sweep/stale-sweep-[date].md
   and end it with "checker: passed".

Fail: save the exact failing checks (criterion number, evidence,
what the maker must change) to
runs/stale-doc-sweep/flags/stale-sweep-[date].md.
Do not append to STATE.md on a fail.
