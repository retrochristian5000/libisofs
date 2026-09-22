#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
header = (ROOT / "libisofs/libisofs.h").read_text(encoding="utf-8")
messages = (ROOT / "libisofs/messages.c").read_text(encoding="utf-8")
hfs_header = (ROOT / "libisofs/hfsplus.h").read_text(encoding="utf-8")
hfs_decompose = (ROOT / "libisofs/hfsplus_decompose.c").read_text(encoding="utf-8")
hfs_classes = (ROOT / "libisofs/hfsplus_classes.c").read_text(encoding="utf-8")
demo = (ROOT / "demo/demo.c").read_text(encoding="utf-8")

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

for declaration in (
    "void make_hfsplus_decompose_pages(void);",
    "void make_hfsplus_class_pages(void);",
):
    assert declaration in hfs_header, f"missing HFS+ strict prototype: {declaration}"

for old_declaration in (
    "void make_hfsplus_decompose_pages();",
    "void make_hfsplus_class_pages();",
):
    assert old_declaration not in hfs_header, (
        f"old-style HFS+ declaration remains: {old_declaration}"
    )

assert "void make_hfsplus_decompose_pages(void)" in hfs_decompose
assert "void make_hfsplus_decompose_pages()" not in hfs_decompose
assert "void make_hfsplus_class_pages(void)" in hfs_classes
assert "void make_hfsplus_class_pages()" not in hfs_classes
assert "void iso_help(void)" in demo
assert "void iso_help()" not in demo

print("libisofs strict-prototype audit passed")
