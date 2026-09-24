#!/usr/bin/env bash
# WebRTC >= 7977 uses unqualified nullptr_t, which clang + libstdc++ does not declare.
set -euo pipefail

{ git grep -lP '(?<![\w:])nullptr_t\b' -- '*.h' '*.cc' || true; } |
    xargs -r perl -pi -e 's/(?<![\w:])nullptr_t\b/std::nullptr_t/g'
