@echo off
setlocal enabledelayedexpansion

echo =================================================================
echo   PLANET HUNTERS -- MISSION CONTROL DASHBOARD LAUNCHER
echo =================================================================

:: Resolve project root directory
cd /d "%~dp0"
set "PROJECT_ROOT=%CD%"
echo Project Root: %PROJECT_ROOT%

:: Check Virtual Environment Python
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Virtual environment Python not found at: %PYTHON_EXE%
    echo Please ensure .venv is installed.
    pause
    exit /b 1
)

:: Prefer running the PowerShell launcher if PowerShell is available
where powershell >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Delegating to START_DASHBOARD.ps1...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\START_DASHBOARD.ps1"
    goto :end
)

:: Fallback direct execution if PowerShell is unavailable
echo PowerShell not found. Launching via Python directly...
"%PYTHON_EXE%" -c "import importlib.util, sys; missing = [p for p in ['streamlit', 'plotly', 'pandas', 'numpy'] if importlib.util.find_spec(p) is None]; sys.exit(1 if missing else 0)"
if errorlevel 1 (
    echo [ERROR] Missing required dashboard packages.
    echo Please run: .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo Starting dashboard on http://localhost:8501 ...
"%PYTHON_EXE%" -m streamlit run "%PROJECT_ROOT%\dashboard\app.py" --server.port 8501 --server.headless false --browser.gatherUsageStats false

:end
if errorlevel 1 pause
