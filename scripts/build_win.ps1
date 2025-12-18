$ErrorActionPreference = "Stop"
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path dist)  { Remove-Item -Recurse -Force dist }
py -m venv build-env
& .\build-env\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

pyinstaller packaging/windows.spec
