#!/usr/bin/env bash
# Shared interpreter discovery. Keep downloads inside this checkout.
set -euo pipefail
SITE_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
SITE_RUNTIME="$SITE_ROOT/.runtime"

find_site_python() {
  local candidate
  for candidate in "$SITE_RUNTIME/bin/python3" python3.12 python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(sys.version_info < (3, 12))' 2>/dev/null; then
      SITE_PYTHON="$(command -v "$candidate")"
      return 0
    fi
  done
  return 1
}

require_site_python() {
  if ! find_site_python; then
    echo 'Execute ./setup primeiro para preparar o Python.' >&2
    exit 1
  fi
}
