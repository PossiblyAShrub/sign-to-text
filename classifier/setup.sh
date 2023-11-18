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

download-dataset() {
  while [[ ! -f $HOME/.kaggle/kaggle.json ]]; do
    echo 'You do not have a ~/.kaggle file. Please follow the "Authentication"'
    echo 'portion of: https://www.kaggle.com/docs/api'
    read -p 'Press enter when you are done'
  done

  if [[ ! -f data/asl-alphabet.zip ]]; then
    echo 'Downloading dataset'
    kaggle datasets download -d grassknoted/asl-alphabet -p data
  else
    echo 'Dataset already downloaded'
  fi

  if [[ ! -r data/asl_alphabet_train ]]; then
    echo 'Extracting dataset'
    (cd data && unzip asl-alphabet.zip)
  else
    echo 'Dataset already extracted'
  fi
}

setup-venv
download-dataset

echo 'Setup Complete'