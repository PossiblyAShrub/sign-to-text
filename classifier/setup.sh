#!/usr/bin/env bash

set -o errexit

setup-venv() {
  if [[ -d venv ]]; then
    echo "venv/ already exists, skipping venv initialization"
    return 0
  fi

  python3 -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt

  echo "/venv setup. Run 'source ./venv/bin/activate' to activate it."
}

setup-venv
