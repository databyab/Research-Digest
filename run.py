from __future__ import annotations

import argparse
import sys

from src.main import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch, summarize, and email a research digest.")
    parser.add_argument("--no-send", action="store_true", help="Print the digest without sending email.")
    args = parser.parse_args()

    try:
        digest = main(send=not args.no_send)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(digest)
