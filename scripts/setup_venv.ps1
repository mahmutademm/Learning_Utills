#    Create and activate a virtual environment, upgrade pip, and install requirements
param(
    [string]$VenvName = '.venv'
)

Write-Output "Creating virtual environment '$VenvName'..."
python -m venv $VenvName

$activate = "./$VenvName/Scripts/Activate.ps1"
if (Test-Path $activate) {
    Write-Output "Activating virtual environment..."
    & $activate
} else {
    Write-Output "Activation script not found at $activate"
}

Write-Output 'Upgrading pip...'
python -m pip install --upgrade pip

if (Test-Path 'requirements.txt') {
    Write-Output 'Installing requirements.txt...'
    python -m pip install -r requirements.txt
} else {
    Write-Output 'requirements.txt not found in repository root.'
}

Write-Output 'Setup complete. To activate the venv in PowerShell run:'
Write-Output "    ./$VenvName/Scripts/Activate.ps1"
