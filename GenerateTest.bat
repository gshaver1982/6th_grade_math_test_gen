@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo =========================================
echo  Math Test Generator
echo =========================================
echo.


set "DIFFICULTY=medium"

echo.
set "COUNT="
set /p "COUNT=Number of questions: "
if not defined COUNT set "COUNT=25"

REM Basic numeric validation
for /f "delims=0123456789" %%A in ("%COUNT%") do (
    echo Invalid number of questions.
    pause
    exit /b
)

if %COUNT% LSS 1 (
    echo Number of questions must be at least 1.
    pause
    exit /b
)

echo.
set "SEED="
set /p "SEED=Seed for repeatable test (press Enter for random): "

echo.
set "NAME="
set /p "NAME=Base filename (press Enter for PracticeTest): "
if not defined NAME set "NAME=PracticeTest"

echo.
if "%SEED%"=="" (
    python main.py --difficulty %DIFFICULTY% --num-questions %COUNT% --output-dir output --base-name "%NAME%"
) else (
    python main.py --difficulty %DIFFICULTY% --num-questions %COUNT% --seed %SEED% --output-dir output --base-name "%NAME%"
)

echo.
echo Done.
pause