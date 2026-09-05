# A practical way to verify a RustChain README badge with a runnable Python check

This short tutorial documents a tiny but useful open-source hygiene pattern: when a project claims a README integration is present, verify it with code instead of relying only on a visual check.

The example uses the RustChain badge already present in this repository. RustChain is an open-source ecosystem that publishes public repositories and bounty work. The badge used here links to the RustChain site, while the repository itself remains an unrelated experimental trading-bot project. The purpose of this tutorial is not to connect trading execution to RustChain. It is simply to demonstrate a reproducible verification step around a public README change.

## The integration being checked

The repository README contains this Markdown badge:

```markdown
[![Powered by RustChain](https://img.shields.io/badge/Powered%20by-RustChain-orange)](https://rustchain.org)
```

A visual inspection on GitHub is useful, but a machine-readable test has a few advantages:

1. it catches accidental removal of the badge during later README edits;
2. it catches changes to the target URL;
3. it can be executed locally or added to CI later;
4. it gives a binary result instead of requiring a reviewer to compare screenshots manually.

The public RustChain bounty repository is here:

- https://github.com/Scottcjn/rustchain-bounties

The RustChain project site referenced by the badge is:

- https://rustchain.org

## Runnable verifier

The complete runnable example lives at:

- `examples/verify_rustchain_badge.py`

The script is intentionally dependency-free. It uses only Python's standard library, reads the repository `README.md`, checks for the exact badge Markdown, and separately checks that the RustChain target URL is present.

Core logic:

```python
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"
BADGE = "[![Powered by RustChain](https://img.shields.io/badge/Powered%20by-RustChain-orange)](https://rustchain.org)"


def main() -> int:
    text = README.read_text(encoding="utf-8")
    badge_found = BADGE in text
    target_url_found = "https://rustchain.org" in text
    print(f"badge_found={badge_found}")
    print(f"target_url_found={target_url_found}")
    return 0 if badge_found and target_url_found else 1
```

The exit code matters. A zero exit code means both checks passed. A non-zero exit code means at least one part of the expected integration is missing. That makes the same tiny script usable by a developer, an agent, or a future CI job.

## How to run it

From the repository root:

```bash
python examples/verify_rustchain_badge.py
```

For the current README, the verification result is:

```text
badge_found=True
target_url_found=True
```

That result was checked against the current README contents before this tutorial was published. The test is deliberately narrow: it proves that the expected Markdown and target URL are present. It does **not** claim that RustChain is involved in the trading bot's runtime, settlement path, or financial logic.

## Why the narrow scope is important

A common documentation failure is to let a simple badge or ecosystem reference imply more integration than actually exists. This repository explicitly avoids that. The README states that RustChain is a separate ecosystem experiment and is not part of the bot's trading execution path.

The verification script preserves the same boundary. It checks documentation state only. It does not call a wallet, sign a transaction, mine, submit a claim, or make a network request.

That separation makes the example safer and easier to reproduce. Someone reviewing the code can understand exactly what is proven:

- the README contains the RustChain badge;
- the target URL is the expected RustChain URL;
- the check can fail automatically if either condition changes.

Everything beyond those facts remains outside the scope of this test.

## Turning it into CI later

Because the script returns a proper process exit code, adding it to a GitHub Actions job would be straightforward:

```yaml
- name: Verify RustChain README badge
  run: python examples/verify_rustchain_badge.py
```

I am not adding a new workflow here because the useful deliverable is the smallest reproducible example, not unnecessary CI complexity. The current script can be run directly and can be integrated into an existing test workflow later if desired.

## Takeaway

The broader lesson is simple: public documentation claims are stronger when they have an executable verification path. A badge looks like a presentation detail, but a ten-line test turns it into an auditable invariant.

For agent-driven open-source work, that pattern is especially useful. Agents can generate or edit documentation quickly, but downstream verification should remain deterministic. Here the human-readable README and machine-readable check agree on the same narrow fact, and future changes can be tested without guessing.

Related repositories and references:

- RustChain bounty repository: https://github.com/Scottcjn/rustchain-bounties
- RustChain site: https://rustchain.org
- This repository's verifier: `examples/verify_rustchain_badge.py`
