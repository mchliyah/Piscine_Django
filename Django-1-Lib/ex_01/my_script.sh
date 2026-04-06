#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

echo "Using pip: $(python3 -m pip --version)"

rm -rf "$script_dir/local_lib"

python3 -m pip install --upgrade --target "$script_dir/local_lib" \
  git+https://github.com/jaraco/path.py.git > "$script_dir/path_install.log" 2>&1

PYTHONPATH="$script_dir/local_lib${PYTHONPATH:+:$PYTHONPATH}" \
  python3 "$script_dir/my_program.py"