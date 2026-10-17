@echo off
cls
echo ===================================================================
echo             ResuMetric AI - Resume Analyzer & ATS Auditor
echo ===================================================================
echo.
echo Choose how you would like to run the application:
echo.
echo   [1] Streamlit App (100%% Pure Python UI - Recommended for Python Interviews)
echo   [2] Flask Web App (Modern Custom Dark Dashboard + PDF Export)
echo   [3] Exit
echo.
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto run_streamlit
if "%choice%"=="2" goto run_flask
if "%choice%"=="3" goto exit

:run_streamlit
echo.
echo Starting Streamlit App (http://localhost:8501)...
python run_streamlit.py
goto end

:run_flask
echo.
echo Starting Flask App (http://127.0.0.1:5000)...
python app.py
goto end

:exit
echo Exiting.
goto end

:end
pause
