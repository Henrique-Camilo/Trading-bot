# RustChain bounty #16471 — silent-success audit finding

Claimant: `Henrique-Camilo`

## Finding: `scripts/bounty_claim.py::gh()` treats failed GitHub CLI calls as normal empty/default results

### Summary

The generic `gh(args, default=None)` helper in `scripts/bounty_claim.py` does **not inspect `subprocess.run(...).returncode`**. It immediately tries to parse `stdout`, and on any exception returns the supplied default.

That creates multiple concrete paths where the workflow can complete successfully while the intended GitHub effect never happened and no hard failure is surfaced.

Relevant helper:

```python
def gh(args, default=None):
    try:
        p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=90)
        return json.loads(p.stdout) if p.stdout.strip() else default
    except Exception:
        return default
```

### Concrete silent-success path A — claim lookup fails, run exits cleanly

`do_claim()` reads the bounty issue with:

```python
iss = gh(["issue", "view", str(num), "-R", REPO,
          "--json", "title,state,labels"], {})
if not iss or iss.get("state") != "OPEN":
    print("issue not open; ignoring")
    return 0
```

If `gh issue view` fails because of an authentication error, rate limit, transient network/API failure, repository permission drift, or another non-zero CLI exit that produces no parseable JSON on stdout:

1. `subprocess.run` returns non-zero.
2. `gh()` does not inspect the non-zero status.
3. Empty stdout returns `{}` (or malformed stdout is caught and also returns `{}`).
4. `do_claim()` interprets the transport/tooling failure as "issue not open".
5. It returns `0`, so the workflow can remain green.
6. The user's claim is not recorded and no retry/recovery signal is created.

This is exactly the bounty's target class: **the code reports a normal/no-op outcome while the intended effect did not happen, without surfacing the underlying failure.**

### Concrete silent-success path B — comment write fails but the function proceeds as if the explanatory action occurred

`live_url_gate()` uses the same helper for a write:

```python
gh(["issue", "comment", str(num), "-R", REPO, "--body", ...], None)
print(f"live-url {reason}; claim not recorded")
return False
```

If `gh issue comment` exits non-zero, the helper returns `None` exactly as it would for an intentionally ignored return value. The function then prints a normal status message and returns `False`. The explanatory comment was never posted, but nothing surfaces that write failure.

The same helper is also used for other issue comments in the claim flow, so the pattern can silently lose contributor-facing state transitions.

## Why this is distinct from the already-fixed `gh issue edit --add-label` defect

The repository already documents a specific GraphQL behavior where `gh issue edit --add-label` can fail without a non-zero exit, and `add_label()`/`remove_label()` were moved to `gh_ok()`.

This finding is broader and still present: **all read/write call sites using `gh()` remain fail-open on ordinary non-zero CLI exits** because `gh()` never checks `returncode`.

## Suggested fix

Make the generic helper fail loudly by default, similar to the hardened helper in `scripts/bounty_payout.py`:

```python
class GhError(RuntimeError):
    pass


def gh(args, default=None, allow_empty=False):
    p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=90)
    if p.returncode != 0:
        raise GhError(
            f"gh {' '.join(args[:3])} exited {p.returncode}: "
            f"{(p.stderr or '').strip()[:300]}"
        )
    if not p.stdout.strip():
        return default if allow_empty else default
    return json.loads(p.stdout)
```

For intentionally best-effort notification paths, catch `GhError` **at the call site**, log a workflow warning/error with enough context, and decide explicitly whether failure should block the state transition. Critical reads (`issue view`, comments used to determine ownership/claim state) should fail the run rather than being converted to "issue not open" or "no active claim".

## Regression tests

At minimum:

1. Stub `subprocess.run` with `returncode=1`, empty stdout, `stderr="HTTP 403"`; assert `do_claim()` does **not** return the same normal outcome as a genuinely closed issue.
2. Stub a failed `gh issue comment`; assert the failure is surfaced and not logged as though the contributor was notified.
3. Stub malformed JSON with returncode 0; assert it is distinguishable from a legitimate empty result.

## Impact

This defect can silently drop claim registration/notification activity during GitHub API or authentication failures while keeping the automation green. That is particularly damaging in a bounty board because claim ownership exists to prevent duplicate work; a silent failed read/write can make two contributors believe a bounty is free or leave a claimant without the guidance the bot intended to post.

No private credentials, live-node access, wallet signing, or spend was used for this finding. It is based entirely on the current public source.