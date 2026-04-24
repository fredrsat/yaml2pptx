#!/usr/bin/env bash
# Quick run: ./run.sh example.yaml [--open]
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/.venv/bin/activate"
python -m yaml2pptx build "$@"
