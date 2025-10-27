# Helper script to create venv, install requirements and run the application app
param(
    [switch]$RecreateVenv = $false,
    [int]$Port = 5000
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if ($RecreateVenv -or -not (Test-Path .venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
. .\.venv\Scripts\Activate.ps1

Write-Host "Installing requirements..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Starting application on http://127.0.0.1:$Port/"
# Run the application app
python .\application\app.py
