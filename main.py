#!/usr/bin/env python3
"""Funniest Cat Voicemail Greeting.

Reads the one-line greeting from entry.txt next to this file, checks it
against the bounty gate (UTF-8 text, 1 to 120 characters, not only
whitespace), writes it to /output/entry.txt for the sealed scorer, and
prints it.
"""

from pathlib import Path

MAX_CHARS = 120


def load_greeting() -> str:
    """Read the greeting from entry.txt beside this entrypoint."""
    path = Path(__file__).with_name("entry.txt")
    return normalise_greeting(path.read_text(encoding="utf-8"))


def normalise_greeting(text: str) -> str:
    """Collapse any line breaks or runs of whitespace to single spaces."""
    return " ".join(text.split())


def validate_greeting(text: str) -> str:
    """Enforce the gate: non-blank, 1 to 120 characters, no control chars."""
    if not text.strip():
        raise ValueError("entry.txt is empty or only whitespace")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("greeting holds a control character")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"greeting is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    return text


def write_output(text: str) -> Path:
    """Write the exact greeting (no trailing newline) for the scorer."""
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


def main() -> None:
    greeting = validate_greeting(load_greeting())
    write_output(greeting)
    print(greeting)


if __name__ == "__main__":
    main()
