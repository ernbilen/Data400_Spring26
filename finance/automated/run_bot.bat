@echo off
echo ==================================================
echo      STARTING QUANTITATIVE ETL PIPELINE
echo ==================================================

echo.
echo [SYSTEM] Booting up Ollama AI Server...
start "" ollama serve
echo Waiting 5 seconds for the AI engine to warm up...
timeout /t 5 /nobreak >nul

cd "C:\Users\popop\Desktop\finance\automated"

echo.
echo [PHASE 1] Vacuuming Raw Reddit Data...
"C:\Users\popop\anaconda3\python.exe" reddit_scraper.py
if %errorlevel% neq 0 (
    echo.
    echo [FATAL ERROR] Phase 1 failed. Stopping pipeline to protect data.
    pause
    exit /b %errorlevel%
)

echo.
echo [PHASE 2] Running LLM Sentiment Engine...
"C:\Users\popop\anaconda3\python.exe" llm_engine.py
if %errorlevel% neq 0 (
    echo.
    echo [FATAL ERROR] Phase 2 failed. Stopping pipeline to protect data.
    pause
    exit /b %errorlevel%
)

echo.
echo [PHASE 3] Calculating Historical Alpha...
"C:\Users\popop\anaconda3\python.exe" yahoo_alpha.py
if %errorlevel% neq 0 (
    echo.
    echo [FATAL ERROR] Phase 3 failed. Stopping pipeline.
    pause
    exit /b %errorlevel%
)

echo.
echo ==================================================
echo      PIPELINE COMPLETE! DATA READY FOR BACKTEST
echo ==================================================
pause