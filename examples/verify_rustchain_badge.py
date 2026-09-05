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


if __name__ == "__main__":
    raise SystemExit(main())
