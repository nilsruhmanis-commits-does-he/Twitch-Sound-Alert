# Twitch Sound Alert - Quick Start Guide

Get your Twitch Sound Alert bot running in 5 minutes! 🚀

## Step 1: Prerequisites (1 minute)

Make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ A Twitch account for your bot (can be your main account or a separate bot account)
- ✅ Some audio files (MP3, WAV, or OGG format)

Check Python version:
```bash
python --version
# or
python3 --version
```

## Step 2: Installation (1 minute)

1. Clone and navigate to the repository:
```bash
git clone https://github.com/nilsruhmanis-commits-does-he/Twitch-Sound-Alert.git
cd Twitch-Sound-Alert
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install as a package:
```bash
pip install -e .
```

> **Note**: If you get permission errors, try using `pip install --user -r requirements.txt`

## Step 3: Get Your OAuth Token (1 minute)

1. Go to [https://twitchapps.com/tmi/](https://twitchapps.com/tmi/)
2. Click "Connect" and authorize the application
3. Copy the OAuth token (it will look like `oauth:xxxxxxxxxxxxxxxxxxxx`)

⚠️ **Important**: Keep this token private! Don't share it or commit it to version control.

## Step 4: Prepare Audio Files (1 minute)

1. Create a `sounds` directory:
```bash
mkdir sounds
```

2. Add your audio files to the `sounds/` directory:
```
sounds/
├── hello.wav
├── welcome.mp3
└── gg.ogg
```

> **Tip**: You can find free sound effects at:
> - [Freesound.org](https://freesound.org/)
> - [Zapsplat.com](https://www.zapsplat.com/)
> - [Mixkit.co](https://mixkit.co/free-sound-effects/)

## Step 5: Configure the Bot (1 minute)

### Option A: Using GUI (Easiest)

1. Launch the GUI:
```bash
python gui.py
```

2. Fill in the Configuration tab:
   - **Twitch Channel**: Your channel name (without the # symbol)
   - **Bot Username**: Your bot account username
   - **OAuth Token**: Paste the token from Step 3

3. Go to the Triggers tab and click "Add Trigger":
   - **Trigger Phrase**: `!hello`
   - **Sound File**: Browse to `sounds/hello.wav`
   - Click "Add"

4. Repeat for other triggers

5. Click "Save Config"

### Option B: Using Config File

1. Copy the example config:
```bash
cp config.example.json config.json
```

2. Edit `config.json`:
```json
{
    "twitch_channel": "your_channel_name",
    "oauth_token": "oauth:your_token_here",
    "bot_username": "your_bot_username",
    "triggers": {
        "!hello": "sounds/hello.wav",
        "!welcome": "sounds/welcome.mp3",
        "!gg": "sounds/gg.ogg"
    },
    "reconnect_delay": 5,
    "max_reconnect_delay": 300
}
```

Replace:
- `your_channel_name` with your Twitch channel name
- `oauth:your_token_here` with your OAuth token from Step 3
- `your_bot_username` with your bot account username

## Step 6: Run the Bot (30 seconds)

### GUI Mode (Recommended for beginners):
```bash
python gui.py
```

Click "Start Bot" button. You should see "Status: Running" in green.

### CLI Mode (For advanced users):
```bash
python twitch_sound_alert.py
```

You should see output like:
```
=== Twitch Sound Alert Bot ===
v1.0.0

Channel: #your_channel
Bot: your_bot_username
Triggers: 3

Connecting to Twitch...
```

## Step 7: Test It! (30 seconds)

1. Open your Twitch chat in a browser
2. Type one of your trigger phrases (e.g., `!hello`)
3. You should hear the associated sound play! 🎵

## 🎉 Success!

Your bot is now running! Keep the application open to continue monitoring chat.

## Next Steps

### Add More Triggers

**GUI**: Click "Add Trigger" in the Triggers tab

**CLI**: Edit `config.json` and add more entries to the `triggers` section:
```json
"triggers": {
    "!hello": "sounds/hello.wav",
    "!bye": "sounds/goodbye.wav",
    "!hype": "sounds/hype.mp3",
    "gg": "sounds/gg.ogg"
}
```

### Run on Startup

**Windows**: Create a shortcut to `gui.py` in your Startup folder

**Linux/Mac**: Add to your startup applications or create a systemd service

### Keep Bot Running 24/7

Consider running on:
- A dedicated computer/laptop
- Raspberry Pi
- Cloud server (AWS, DigitalOcean, etc.)
- Local server

## Common Issues

### ❌ "pygame not installed"
```bash
pip install pygame
```

### ❌ "Connection failed"
- Double-check your OAuth token
- Verify channel name is correct (no # symbol)
- Make sure bot username matches OAuth account

### ❌ "Sound file not found"
- Check file paths in config.json
- Verify files exist in the sounds/ directory
- Use absolute paths if needed: `/full/path/to/sounds/hello.wav`

### ❌ No sound plays
- Test the audio file in a media player
- Check system volume isn't muted
- Verify pygame installed correctly: `python -c "import pygame"`

## Getting Help

If you encounter issues:
1. Check the [README.md](README.md) for detailed documentation
2. Review the Log tab in GUI mode for error messages
3. Open an issue on [GitHub](https://github.com/nilsruhmanis-commits-does-he/Twitch-Sound-Alert/issues)

## Tips for Best Results

✨ **Use clear, unique triggers** - Avoid common words that appear in normal chat

✨ **Keep sounds short** - 1-3 second clips work best

✨ **Test before going live** - Make sure everything works in your test stream

✨ **Monitor the logs** - Check for connection issues or errors

✨ **Keep OAuth token secure** - Never share it or commit to version control

---

**Enjoy your Twitch Sound Alert bot!** 🎮🔊

For more information, see the full [README.md](README.md)
