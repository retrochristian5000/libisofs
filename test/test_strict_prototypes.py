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

old_header_declarations = (
    "int iso_init();",
    "void iso_finish();",
    "void *iso_get_messenger();",
)
for declaration in old_header_declarations:
    assert declaration not in header, f"old-style declaration remains: {declaration}"

old_definitions = (
    "int iso_init()",
    "void iso_finish()",
    "void *iso_get_messenger()",
)
for definition in old_definitions:
    assert definition not in messages, f"old-style definition remains: {definition}"

print("libisofs strict-prototype audit passed")
