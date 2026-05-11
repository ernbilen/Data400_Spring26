@echo off
echo Starting Ollama Server in the background...
start /b ollama serve

echo Waiting 5 seconds for AI to boot...
timeout /t 5 /nobreak > NUL

echo Launching the Live Trading Bot...
cd "C:\Users\popop\Desktop\finance\automated"
python live_bot.py

echo Run Complete!