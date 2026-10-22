# ==============================================================================
# Planet Hunters -- Mission Control Dashboard Launcher (PowerShell)
# Hack4Hack 2026 Round 1
# ==============================================================================

# 1. Automatically identify project root using script's directory and change directory
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $ProjectRoot) {
    $ProjectRoot = $PSScriptRoot
}
if (-not $ProjectRoot) {
    $ProjectRoot = (Get-Item -Path ".\").FullName
}
Set-Location -Path $ProjectRoot

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  PLANET HUNTERS -- MISSION CONTROL DASHBOARD LAUNCHER" -ForegroundColor White
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Project Root: $ProjectRoot" -ForegroundColor Gray

# 2. Detect existing virtual environment Python
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -Path $PythonExe)) {
    Write-Host "[ERROR] Virtual environment Python not found at: $PythonExe" -ForegroundColor Red
    Write-Host "Please ensure the project virtual environment (.venv) is properly set up." -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Detected virtual environment Python: $PythonExe" -ForegroundColor Green

# 3. Verify dashboard application exists
$AppPath = Join-Path $ProjectRoot "dashboard\app.py"
if (-not (Test-Path -Path $AppPath)) {
    Write-Host "[ERROR] Dashboard entry point not found at: $AppPath" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Dashboard entry point verified: $AppPath" -ForegroundColor Green

# 4. Check dependencies using Python importlib without raw multiline Python code
Write-Host "Checking runtime packages (Streamlit, Plotly, Pandas, NumPy)..." -ForegroundColor Gray

$CheckCmd = "import importlib.util, sys; missing = [p for p in sys.argv[1:] if importlib.util.find_spec(p) is None]; print(','.join(missing)); sys.exit(1 if missing else 0)"
$MissingOutput = & $PythonExe -c $CheckCmd streamlit plotly pandas numpy 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Missing required dashboard packages: $MissingOutput" -ForegroundColor Red
    Write-Host "Install all required packages with the following command:" -ForegroundColor Yellow
    Write-Host "  & .\.venv\Scripts\python.exe -m pip install -r requirements.txt" -ForegroundColor White
    exit 1
}

Write-Host "[OK] Required dependencies verified (streamlit, plotly, pandas, numpy)." -ForegroundColor Green

# 5. Check Final Submission File Status (Read-Only Verification)
$SubmissionFile = Join-Path $ProjectRoot "submissions\submission_FINAL.csv"
if (Test-Path -Path $SubmissionFile) {
    Write-Host "[OK] Final submission verified: submissions\submission_FINAL.csv" -ForegroundColor Green
} else {
    Write-Host "[WARNING] submissions\submission_FINAL.csv not found." -ForegroundColor Yellow
}

# 6. Port occupancy detection (handles 8501 -> 8502 fallback)
function Test-PortOccupied ([int]$PortToCheck) {
    try {
        $conn = Get-NetTCPConnection -LocalPort $PortToCheck -ErrorAction Stop
        if ($conn) { return $true }
    } catch {}

    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $iar = $client.BeginConnect("127.0.0.1", $PortToCheck, $null, $null)
        $success = $iar.AsyncWaitHandle.WaitOne(200, $false)
        if ($success -and $client.Connected) {
            $client.EndConnect($iar)
            $client.Close()
            return $true
        }
        $client.Close()
    } catch {}

    return $false
}

$Port = 8501
if (Test-PortOccupied -PortToCheck $Port) {
    Write-Host "[WARNING] Port $Port is currently in use." -ForegroundColor Yellow
    $Port = 8502
    Write-Host "Switching to alternative port: $Port" -ForegroundColor Cyan
}

Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "Launching Mission Control Dashboard on port $Port..." -ForegroundColor White
Write-Host "Dashboard Local URL: http://localhost:$Port" -ForegroundColor Cyan
Write-Host "Press Ctrl+C in this terminal window to stop the dashboard server." -ForegroundColor Gray
Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan

# 7. Launch dashboard using python -m streamlit run dashboard/app.py --server.port $Port
& $PythonExe -m streamlit run "$AppPath" --server.port $Port --server.headless false --browser.gatherUsageStats false
