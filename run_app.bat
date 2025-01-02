@echo off
rem Define the configuration file
set "CONFIG_FILE=config.ini"

rem Initialize variables
set "SERVER_URL="

rem Read the SERVER_URL from the config.ini file
for /f "usebackq tokens=1,2 delims== " %%A in ("%CONFIG_FILE%") do (
    if "%%A"=="SERVER_URL" set "SERVER_URL=%%B"
)

rem Check if SERVER_URL was retrieved
if not defined SERVER_URL (
    echo SERVER_URL not found in config.ini. Exiting...
    pause
    exit /b
)

rem Start ngrok in a separate window with the dynamic SERVER_URL
echo Starting ngrok with SERVER_URL: %SERVER_URL%
start "ngrok" cmd /k ".\ngrok\ngrok http --url=%SERVER_URL% 5000"

rem Start the Python application in a separate window
start "Python App" cmd /k "call venv\Scripts\activate && python -B app.py"

rem Provide instructions
echo ==============================================
echo Running ngrok and Python application...
echo Press any key to stop both ngrok and the Python app.
echo ==============================================
pause

rem Stop the ngrok process
for /f "tokens=2" %%A in ('tasklist /fi "imagename eq ngrok.exe" /v ^| findstr /i "ngrok - .\ngrok\ngrok http --url=oriented-bunny-totally.ngrok-free.app 5000"') do (
    echo Stopping ngrok process with PID %%A...
    taskkill /f /pid %%A
)

rem Stop the Python process
for /f "tokens=2" %%A in ('tasklist /fi "imagename eq python.exe" /v ^| findstr /i "Python App - python app.py"') do (
    echo Stopping Python process with PID %%A...
    taskkill /f /pid %%A
)

rem Close any lingering cmd windows
for /f "tokens=2" %%A in ('tasklist /fi "imagename eq cmd.exe" /v ^| findstr /i "ngrok"') do (
    echo Closing ngrok command window with PID %%A...
    taskkill /f /pid %%A
)

for /f "tokens=2" %%A in ('tasklist /fi "imagename eq cmd.exe" /v ^| findstr /i "Python App"') do (
    echo Closing Python command window with PID %%A...
    taskkill /f /pid %%A
)

echo All processes and windows stopped. Exiting...
exit
