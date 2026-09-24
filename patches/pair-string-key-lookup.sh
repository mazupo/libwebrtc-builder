#!/usr/bin/env bash
# WebRTC >= 7778 looks up flat_map<pair<string, bool>, ...> with a pair<string_view, bool>.
# That needs heterogeneous std::pair comparison (LWG 3865), which libstdc++ < 14 lacks.
set -euo pipefail

{ git grep -lF 'uri_to_id_.find(std::pair{uri, encrypt})' -- '*.cc' || true; } |
    xargs -r perl -pi -e 's/uri_to_id_\.find\(std::pair\{uri, encrypt\}\)/uri_to_id_.find(std::pair{std::string(uri), encrypt})/g'
