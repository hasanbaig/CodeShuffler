#!/usr/bin/env bash
set -e

rm -rf build dist build-env

python3 -m venv build-env
source build-env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

pyinstaller packaging/codeshuffler.spec

echo "Build complete."
