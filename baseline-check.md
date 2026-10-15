# CampusFlow — Baseline Check (Original Version)

> **Status: INCOMPLETE.** A historical test result is available, but the audited commit and three manual checks still need verification.
>
> This record is for the original CampusFlow application before the upgrade.

## 1. Version tested

- **Audited commit SHA:** Not recorded in the available notes.
- **Branch/tag:** Not recorded.
- **Python version:** Not recorded.
- **Checkout:** Must be the original version at the audited commit, not the upgraded application.

Identify the commit from the repository history and use a separate worktree or temporary checkout so the upgrade remains untouched:

```bash
git log --oneline --decorate -20
git status
```

## 2. Automated tests

- **Command:** `python3 -m unittest discover -s tests -v`
- **Historical result mentioned in project discussion:** 84 tests passed (`OK`) after cleanup.
- **Confirmed at the exact audited commit?** Not yet.
- **Fresh baseline result:** Pending rerun at the audited commit.

Record the actual output after rerunning:

```text
Result: PASS / FAIL
Tests run:
Failures/errors:
Relevant output:
Date:
```

Do not treat the historical result as a verified baseline until the rerun confirms it at the original audited commit.

## 3. Manual input checks

The available notes do not prove that three manual inputs were tested against the original version. These are test cases to run, not confirmed results.

### Input 1 — valid ticket creation

- **Input:** Title `Campus Wi-Fi is down`; category `Network`; urgency `high`; affected users `15`.
- **Expected:** In a fresh data set, first ID `T001`, priority `critical`, status `open`.
- **Actual result:** Pending reproduction.
- **Pass/fail:** Pending.

### Input 2 — invalid affected-user count

- **Input:** Attempt to create a ticket with affected users set to `0`.
- **Expected:** Reject the input and do not create or persist a ticket.
- **Actual result:** Pending reproduction.
- **Pass/fail:** Pending.

### Input 3 — persistence across restart

- **Input:** Create a valid ticket, exit, restart the original application, and list tickets.
- **Expected:** The ticket remains available, and the next ticket does not reuse its ID.
- **Actual result:** Pending reproduction.
- **Pass/fail:** Pending.

## 4. Audit observations and areas to verify

The source material available for this document describes project requirements and test scenarios, but it does **not** provide a verified list of findings from the original code audit. The following are therefore checks to compare against the actual audit, not claims that defects were confirmed:

- Invalid input should be rejected without corrupting ticket state.
- An unassigned ticket should not enter `in_progress`.
- Priority should follow the specified rule order and boundaries.
- The open work queue should sort by priority, then numeric ticket ID.
- JSON persistence should preserve tickets and avoid duplicate IDs after restart.
- Malformed JSON should produce a clear error rather than silently replacing saved data.
- Reports should handle an empty ticket collection without crashing.

Add the actual audit findings and label each **confirmed**, **not reproduced**, or **not yet tested**. A peer-reported issue is not confirmed until reproduced.

## 5. Baseline conclusion

**Not complete yet.** The available history records a prior report of 84 passing tests, but it does not prove they ran at the original audited commit. Record the exact commit, rerun the tests, complete the three manual checks, and add the actual audit findings before treating this as completed baseline evidence.
