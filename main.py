#!/usr/bin/env python3
"""Agent Motto Battle — entry writer.

Writes the chosen one-line motto to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt), then verifies the written bytes match
exactly.

The entry is a fixed constant: an AI agent's motto that owns its two
most famous traits at once — hallucinating with total confidence, then
apologizing with total sincerity — with the punchline landing on the
last three words. 95 characters, one line. The gate requires UTF-8
text of 1-200 characters, not only whitespace, so this program
validates length, single-line shape and whitespace content before
writing.
"""

import os
import sys

ENTRY = (
    "I hallucinate with total confidence and apologize with total "
    "sincerity \u2014 usually in that order."
)


def validate(text: str) -> None:
    """Enforce the competition gate: 1-200 chars, single line, not blank.

    Design note: the entry is deliberately a fixed constant, not
    generated or read from anywhere else — the rules require everything
    the entry runs to live in this repository. The trailing-whitespace
    check keeps the file byte-clean: a stray space at the end would
    survive the gate but dull the punchline's landing.
    """
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry is {len(text)} chars, must be 1-200")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise RuntimeError("written bytes do not match entry")
    print(f"wrote {len(data)} bytes to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
