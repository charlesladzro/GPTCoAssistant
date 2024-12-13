@echo off
rem Start ngrok in a separate window
start "ngrok" cmd /k ".\ngrok\ngrok http --url=oriented-bunny-totally.ngrok-free.app 5000"

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
