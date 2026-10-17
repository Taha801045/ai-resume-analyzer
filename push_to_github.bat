@echo off
setlocal enabledelayedexpansion
title Push ResuMetric AI to GitHub

echo ========================================================
echo        ResuMetric AI - 1-Click GitHub Pusher
echo ========================================================
echo.

:: Detect git executable
set "GIT_EXE=git"
where git >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Program Files\Git\cmd\git.exe" (
        set "GIT_EXE=C:\Program Files\Git\cmd\git.exe"
    ) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd\git.exe" (
        set "GIT_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd\git.exe"
    ) else (
        echo [ERROR] Git is not found! Please install Git from https://git-scm.com/
        pause
        exit /b 1
    )
)

echo [*] Git detected successfully!
echo.

:: Ensure on main branch
"!GIT_EXE!" branch -M main

:: Add and commit any new changes
"!GIT_EXE!" add .
"!GIT_EXE!" commit -m "feat: AI Resume Analyzer & ATS Auditor with Streamlit UI" >nul 2>&1

:: Ask for the actual GitHub Repository URL
echo --------------------------------------------------------
echo Apne GitHub repository ka actual URL yahan paste karein:
echo (Example: https://github.com/taha-dev/ai-resume-analyzer.git)
echo --------------------------------------------------------
set /p REPO_URL="Repo URL paste karein: "

if "%REPO_URL%"=="" (
    echo [ERROR] Aapne URL enter nahi kiya!
    pause
    exit /b 1
)

:: Set remote origin
"!GIT_EXE!" remote remove origin >nul 2>&1
"!GIT_EXE!" remote add origin %REPO_URL%

echo.
echo [*] Pushing your project to GitHub (branch: main)...
echo [*] Agar GitHub login prompt aye, toh Sign in with browser karein...
echo.

"!GIT_EXE!" push -u origin main --force

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo    SUCCESS! Aapka project GitHub par live ho gaya!
    echo ========================================================
    echo Ab aap Streamlit Cloud (share.streamlit.io) par jaakar
    echo is repo ko 2 clicks me deploy kar sakte hain!
) else (
    echo.
    echo ========================================================
    echo  [!] Push me koi error aya. 
    echo  Check karein ki aapne sahi URL paste kiya hai aur 
    echo  GitHub me logged in hain.
    echo ========================================================
)

echo.
pause
