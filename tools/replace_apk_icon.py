#!/usr/bin/env python3
#
# SPDX-License-Identifier: Apache-2.0
#
"""Replace MiuiCamera's launcher icon bitmaps with round versions.

MiuiCamera's mipmap/f9f is a square bitmap, and the app marks its resources
as not overlayable, so a runtime resource overlay cannot swap it. Launchers
draw a square bitmap small inside a plate, but scale a round one to fill the
icon shape. This copies the APK and replaces only the two icon entries.

Usage: replace_apk_icon.py IN.apk OUT.apk res/name.webp=path ...
"""

import sys
import zipfile


def main():
    src, dst, pairs = sys.argv[1], sys.argv[2], sys.argv[3:]
    repl = dict(p.split("=", 1) for p in pairs)
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info)
            if info.filename in repl:
                with open(repl.pop(info.filename), "rb") as f:
                    data = f.read()
            zout.writestr(info, data)
    if repl:
        sys.exit("missing APK entries: " + ", ".join(repl))


if __name__ == "__main__":
    main()
