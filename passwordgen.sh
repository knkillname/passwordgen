#!/bin/bash
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/src"
PYTHONPATH="$PROJECT_DIR" python -m passwordgen "$@"
