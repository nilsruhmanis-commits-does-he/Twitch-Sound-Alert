@echo off
REM Quick setup script for Twitch Sound Alert
echo Setting up Twitch Sound Alert...

IF "%SKIP_VENV%"=="1" (
	echo Skipping virtual environment (SKIP_VENV=1). Using system Python.
	set PIP_CMD=python -m pip
) ELSE (
	REM Create venv
	python -m venv venv
	call venv\Scripts\Activate.bat
	set PIP_CMD=pip
)

REM Install dependencies
%PIP_CMD% install --upgrade pip
%PIP_CMD% install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. (Optional) Activate venv later if you created one: venv\Scripts\Activate.bat
echo 2. Get your OAuth token from: https://twitchapps.com/tmi/
echo 3. Set the token (replace YOUR_TOKEN):
echo    set TWITCH_OAUTH_TOKEN=oauth:YOUR_TOKEN
echo 4. Run the app:
echo    python twitch-alert-gui.py   (GUI)
echo    python twitch-sound-alert.py (CLI)
echo.
pause
