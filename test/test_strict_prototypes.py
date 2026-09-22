#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
header = (ROOT / "libisofs/libisofs.h").read_text(encoding="utf-8")
messages = (ROOT / "libisofs/messages.c").read_text(encoding="utf-8")

expected = (
    "int iso_init(void);",
    "void iso_finish(void);",
    "void *iso_get_messenger(void);",
)
for declaration in expected:
    assert declaration in header, f"missing strict prototype: {declaration}"

for definition in (
    "int iso_init(void)",
    "void iso_finish(void)",
    "void *iso_get_messenger(void)",
):
    assert definition in messages, f"missing strict definition: {definition}"

old_style = re.compile(
    r"\b(?:iso_init|iso_finish|iso_get_messenger)\s*\(\s*\)"
)
for path, text in (
    ("libisofs/libisofs.h", header),
    ("libisofs/messages.c", messages),
):
    match = old_style.search(text)
    assert match is None, f"old-style empty parameter list remains in {path}"

print("libisofs strict-prototype audit passed")
