#!/bin/bash

# Check for Python 3
if ! which python3 >/dev/null; then
  echo "Error: Python 3 not found."
  exit 1
fi

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONPATH="$PROJECT_DIR"/src python3 -m passwordgen "$@"
