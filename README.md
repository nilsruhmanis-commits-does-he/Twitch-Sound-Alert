# Twitch Sound Alert

A lightweight Python bot that monitors Twitch chat and plays custom sounds when trigger phrases appear. Features both GUI and CLI interfaces with auto-reconnect and multi-format audio support.

## 🎮 Features

- **Dual Interface**: Choose between graphical (GUI) or command-line (CLI) interface
- **Multi-Format Audio**: Support for MP3, WAV, and OGG audio files
- **Auto-Reconnection**: Automatic reconnection with exponential backoff (5s to 300s)
- **Non-Blocking Playback**: Audio plays in daemon threads without blocking chat monitoring
- **Persistent Configuration**: Save and load settings from JSON config file
- **Easy Setup**: 5-minute quickstart guide included

## 📋 Requirements

- **Python 3.8+**
- **pygame** (recommended for audio playback)
- **Twitch OAuth Token** (get from [https://twitchapps.com/tmi/](https://twitchapps.com/tmi/))

## 🚀 Quick Start

See [QUICKSTART.md](QUICKSTART.md) for a complete 5-minute setup guide.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nilsruhmanis-commits-does-he/Twitch-Sound-Alert.git
cd Twitch-Sound-Alert
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install as a package:
```bash
pip install -e .
```

### Configuration

1. Copy the example config:
```bash
cp config.example.json config.json
```

2. Edit `config.json` with your details:
```json
{
    "twitch_channel": "your_channel_name",
    "oauth_token": "oauth:your_token_here",
    "bot_username": "your_bot_username",
    "triggers": {
        "!hello": "sounds/hello.wav",
        "!welcome": "sounds/welcome.wav"
    },
    "reconnect_delay": 5,
    "max_reconnect_delay": 300
}
```

3. Get your OAuth token from [https://twitchapps.com/tmi/](https://twitchapps.com/tmi/)

### Usage

#### GUI Mode (Recommended)
```bash
python gui.py
```

Or if installed as package:
```bash
twitch-sound-alert-gui
```

The GUI provides:
- Easy configuration editing
- Trigger management with file browser
- Live log viewing
- Sound testing
- Start/Stop controls

#### CLI Mode
```bash
python twitch_sound_alert.py
```

Or if installed as package:
```bash
twitch-sound-alert
```

## 📝 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `twitch_channel` | Your Twitch channel name (without #) | Required |
| `oauth_token` | OAuth token from twitchapps.com/tmi | Required |
| `bot_username` | Bot account username | Required |
| `triggers` | Dictionary of trigger phrases and sound files | {} |
| `reconnect_delay` | Initial reconnection delay in seconds | 5 |
| `max_reconnect_delay` | Maximum reconnection delay in seconds | 300 |

## 🔊 Audio Files

Place your audio files in a `sounds/` directory (or specify full paths in config):

```
Twitch-Sound-Alert/
├── sounds/
│   ├── hello.wav
│   ├── welcome.mp3
│   ├── gg.ogg
│   └── ...
├── config.json
└── twitch_sound_alert.py
```

Supported formats:
- **MP3** - MPEG Audio Layer 3
- **WAV** - Waveform Audio File Format
- **OGG** - Ogg Vorbis

## 🔄 Auto-Reconnection

The bot automatically handles connection issues with exponential backoff:

1. Initial reconnection attempt after 5 seconds
2. Doubles delay on each failed attempt (5s → 10s → 20s → 40s → ...)
3. Caps at maximum delay (default 300 seconds)
4. Resets delay on successful connection

## 🎯 Trigger System

Triggers are case-insensitive substring matches. When a trigger phrase appears in chat, the associated sound plays immediately in a non-blocking daemon thread.

Example triggers:
```json
"triggers": {
    "!hello": "sounds/hello.wav",
    "!welcome": "sounds/welcome.wav",
    "!gg": "sounds/gg.mp3",
    "wow": "sounds/wow.ogg",
    "hype": "sounds/hype.wav"
}
```

## 🛠️ Troubleshooting

### pygame not installed
```bash
pip install pygame
```

### Connection fails
- Verify your OAuth token is correct and starts with `oauth:`
- Check that your channel name is correct (no # symbol)
- Ensure bot username matches the OAuth token account

### Sound doesn't play
- Verify audio files exist at specified paths
- Check file formats are supported (MP3, WAV, OGG)
- Test audio file plays with other media players
- Check pygame is properly installed

### Bot disconnects frequently
- Check your internet connection
- Verify OAuth token hasn't expired
- Check Twitch service status

## 📚 API Reference

### TwitchBot Class

Main bot class that handles Twitch IRC connection and message processing.

**Methods:**
- `connect()` - Connect to Twitch IRC
- `disconnect()` - Disconnect from Twitch
- `run()` - Main bot loop with auto-reconnect
- `stop()` - Stop the bot gracefully

### AudioPlayer Class

Handles audio playback in non-blocking daemon threads.

**Methods:**
- `play_sound(filepath)` - Play audio file asynchronously

### ConfigManager Class

Manages persistent configuration storage.

**Methods:**
- `load_config()` - Load config from JSON file
- `save_config()` - Save config to JSON file
- `get(key, default)` - Get configuration value
- `set(key, value)` - Set configuration value

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python 3.8+
- Uses pygame for audio playback
- Connects to Twitch IRC for chat monitoring

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🔗 Links

- [GitHub Repository](https://github.com/nilsruhmanis-commits-does-he/Twitch-Sound-Alert)
- [Get Twitch OAuth Token](https://twitchapps.com/tmi/)
- [Twitch IRC Documentation](https://dev.twitch.tv/docs/irc)

---

Made with ❤️ for the Twitch community
# Twitch Sound Alert 

A lightweight Twitch IRC bot that plays custom sounds when specific trigger phrases appear in chat. Features both a user-friendly GUI and a standalone CLI version.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features
- Dual interface: GUI and CLI
- Multi-format audio: MP3, WAV, OGG
- Auto-reconnect with exponential backoff
- Non-blocking daemon-thread audio playback
- Case-insensitive trigger matching
- Persistent config via config.json (GUI)

## Quick Start
### Windows
```powershell
./setup.bat
./venv/Scripts/Activate.ps1
$env:TWITCH_OAUTH_TOKEN = "oauth:YOUR_TOKEN_HERE"
python twitch-alert-gui.py   # or python twitch-sound-alert.py
```
### Linux/Mac
```bash
bash setup.sh
source venv/bin/activate
export TWITCH_OAUTH_TOKEN="oauth:YOUR_TOKEN_HERE"
python twitch-alert-gui.py   # or python twitch-sound-alert.py
```

### Run without a virtual environment
If you prefer the system interpreter, set `SKIP_VENV=1` when running setup scripts, or install deps directly:
- Windows (PowerShell): `set SKIP_VENV=1 && ./setup.bat` or `python -m pip install -r requirements.txt`
- Linux/Mac: `SKIP_VENV=1 bash setup.sh` or `python3 -m pip install -r requirements.txt`

## Configuration
- GUI: fill fields in twitch-alert-gui.py and click Save/Start; persists to config.json
- CLI: edit USERNAME, CHANNEL, TRIGGER_CODE, SOUND_FILE at top of twitch-sound-alert.py
- OAuth token: set TWITCH_OAUTH_TOKEN env var; never commit tokens

## Audio Backends
Preferred: pygame (MP3/OGG/WAV)
Fallbacks: winsound (Windows WAV), simpleaudio (WAV), noop

## Architecture
```
config.json → GUI/CLI → TwitchListener → Twitch IRC → Message Parser → Sound Player
```
- IRC via raw sockets to irc.chat.twitch.tv:6667
- `PING`/`PONG` keepalive handled automatically
- Trigger detection in twitch_listener.py message loop; sound plays on daemon thread

## Project Structure
- twitch-sound-alert.py — CLI
- twitch-alert-gui.py — GUI (Tkinter)
- twitch_listener.py — Core listener class
- config.example.json — template config
- setup.bat / setup.sh — setup scripts
- .github/copilot-instructions.md — AI/dev architecture guide

## Troubleshooting
- Token must start with `oauth:`
- Channel name without leading `#`
- Install pygame for MP3/OGG
- Use WAV if fallbacks only
- Check file paths exist and readable

## Creator
- E-mail: nilsruhmanis@gmail.com
- BTC: bc1q6s6697nu4eq9yx9sfgw6t6uguu3pp0r86uxuwt
  
## License
MIT. See LICENSE.
