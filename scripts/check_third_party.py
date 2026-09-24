#!/usr/bin/env python3
"""Lists the third_party libraries bundled into libwebrtc.a and checks NOTICE covers them.

Run from the WebRTC checkout (webrtc/src) after `gn gen`; nothing needs to be built.
"""

import argparse
import re
import subprocess
import sys

# Matches the first third_party directory of an object path,
# e.g. obj/common_audio/third_party/ooura/... -> common_audio/third_party/ooura.
LIB_RE = re.compile(r"^obj/((?:[\w\-+.]+/)*?third_party/[\w\-+.]+)/")


def bundled_libraries(build_dir):
    # The archive step's explicit inputs are exactly the objects merged into libwebrtc.a, so
    # shared libraries (FFmpeg with is_component_ffmpeg) and header-only targets drop out.
    out = subprocess.check_output(
        ["ninja", "-C", build_dir, "-t", "query", "obj/libwebrtc.a"], text=True
    )
    libs = set()
    for line in out.splitlines():
        line = line.strip()
        if line == "outputs:":
            break
        if line.startswith("|"):  # implicit and order-only inputs are not archived
            continue
        match = LIB_RE.match(line)
        if match:
            libs.add(match.group(1))
    return sorted(libs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir", help="GN build directory, e.g. out/Release")
    parser.add_argument("--notice", required=True, help="Path to the NOTICE file")
    parser.add_argument("--output", required=True, help="Where to write the library list")
    args = parser.parse_args()

    libs = bundled_libraries(args.build_dir)
    if not libs:
        print("Found no third_party objects in libwebrtc.a; is the build directory right?",
              file=sys.stderr)
        return 1
    with open(args.output, "w") as f:
        f.write("\n".join(libs) + "\n")

    with open(args.notice) as f:
        notice = f.read()
    missing = [lib for lib in libs if f"({lib})" not in notice]
    if missing:
        print("NOTICE does not list these bundled libraries:", file=sys.stderr)
        for lib in missing:
            print(f"  {lib}", file=sys.stderr)
        return 1

    print(f"NOTICE covers all {len(libs)} bundled third_party libraries:")
    print("\n".join(f"  {lib}" for lib in libs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
