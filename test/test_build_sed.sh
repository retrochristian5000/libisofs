#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
#
# Exercise the two handwritten sed transformations used by the build system.
# Set SED=/path/to/sed to test a specific implementation.

set -eu

SED=${SED:-sed}

fail()
{
    echo "libisofs build sed test failed: $*" >&2
    exit 1
}

# configure.ac: only Autoconf's exact default pair is removable.  A caller's
# longer CFLAGS string must not be partially rewritten.
got=$(printf '%s\n' '-g -O2' | "$SED" -e 's/^-g -O2$//')
test -z "$got" || fail "default CFLAGS pair was not removed"

input='-g -O2 -fno-omit-frame-pointer'
got=$(printf '%s\n' "$input" | "$SED" -e 's/^-g -O2$//')
test "x$got" = "x$input" || fail "caller CFLAGS were partially rewritten"

input='-O2 -g'
got=$(printf '%s\n' "$input" | "$SED" -e 's/^-g -O2$//')
test "x$got" = "x$input" || fail "reordered caller CFLAGS were rewritten"

# acinclude.m4: FreeBSD's default .../lib pkg-config base becomes .../libdata.
input='${exec_prefix}/lib'
got=$(printf '%s\n' "$input" | "$SED" 's,/lib$,/libdata,')
test "x$got" = 'x${exec_prefix}/libdata' || fail "lib -> libdata rewrite failed"

# Do not flatten other library directory names.
for input in '${exec_prefix}/lib64' '/opt/lib/lib' '/usr/local/library'
do
    got=$(printf '%s\n' "$input" | "$SED" 's,/lib$,/libdata,')
    case "$input" in
        */lib)
            expected=${input%/lib}/libdata
            ;;
        *)
            expected=$input
            ;;
    esac
    test "x$got" = "x$expected" || fail "unexpected pkg-config rewrite: $input -> $got"
done

echo "libisofs build sed audit passed with $SED"
