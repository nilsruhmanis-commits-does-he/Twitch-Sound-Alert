# Quick Start Guide

Get up and running with Twitch Sound Alert in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- A Twitch account
- An audio file (MP3, WAV, or OGG)

## Setup (5 Steps)

### 1. Install Dependencies

**Windows:**
```powershell
.\setup.bat
```

**Linux/Mac:**
```bash
bash setup.sh
```

### 2. Get OAuth Token

1. Visit: https://twitchtokengenerator.com/
2. Click "Bot Chat Token"
3. Authorize with your Twitch account
4. Copy the token (starts with `oauth:`)

### 3. Set Environment Variable

**Windows PowerShell:**
```powershell
$env:TWITCH_OAUTH_TOKEN = "oauth:YOUR_TOKEN_HERE"
```

**Linux/Mac:**
```bash
export TWITCH_OAUTH_TOKEN="oauth:YOUR_TOKEN_HERE"
```

### 4. Configure Settings

**Option A - GUI (Recommended):**
```bash
python twitch-alert-gui.py
```
Then fill in the form:
- Username: Your bot's Twitch username
- Channel: Channel to monitor (e.g., `streamer_name`)
- Trigger: Phrase to detect (e.g., `!alert`)
- Sound File: Path to your audio file

**Option B - CLI:**
Edit `twitch-sound-alert.py` lines 16-19:
```python
USERNAME = "your_bot_username"
CHANNEL = "channel_to_join"
TRIGGER_CODE = "!alert"
SOUND_FILE = "path/to/sound.mp3"
```

### 5. Run!

**GUI:**
Click "Start Listening" in the application

**CLI:**
```bash
python twitch-sound-alert.py
```

## Testing

1. Open the Twitch channel in a browser
2. Type your trigger phrase in chat
3. Hear the sound play! 🎵

## Troubleshooting

### "OAuth token not set"
- Make sure you set the environment variable
- Token must start with `oauth:`
- Check for typos

### "Connection failed"
- Verify your internet connection
- Check username is lowercase
- Don't include `#` in channel name

### "Sound file not found"
- Use absolute path to audio file
- Verify file exists and is accessible
- Check file format is supported

### No sound plays
- Install pygame: `pip install pygame`
- Check audio file isn't corrupted
- Verify system volume isn't muted

## Next Steps

- See [README.md](README.md) for full documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Read [.github/copilot-instructions.md](.github/copilot-instructions.md) for architecture

## Tips

- Use unique trigger phrases to avoid false positives
- Test in a quiet channel first
- Keep sound files under 5 seconds for best UX
- Check the activity log for debugging

---

Need more help? Check the full [README.md](README.md) or open an issue!
