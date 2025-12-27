# Changelog

All notable changes to Twitch Sound Alert will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-27

### Added
- Initial release of Twitch Sound Alert
- CLI version (`twitch-sound-alert.py`) for command-line operation
- GUI version (`twitch-alert-gui.py`) with Tkinter interface
- Core `TwitchListener` class for reusable functionality
- Multi-backend audio support (pygame, winsound, simpleaudio)
- Automatic reconnection with exponential backoff
- Case-insensitive trigger phrase matching
- Persistent configuration via `config.json`
- Real-time activity logging in GUI
- OAuth token management with hide/show toggle
- Windows and Linux/Mac setup scripts
- Comprehensive documentation and README
- `.gitignore` for clean version control
- MIT License

### Features
- Raw TCP socket connection to Twitch IRC
- Non-blocking sound playback using daemon threads
- `PING`/`PONG` keepalive handling
- Config validation before starting listener
- Browser integration for OAuth token generation
- Sound file format detection and validation

### Documentation
- Detailed README with quick start guide
- Architecture documentation in `.github/copilot-instructions.md`
- Inline code comments and docstrings
- Troubleshooting section for common issues

[1.0.0]: https://github.com/yourusername/twitwitch-sound-alert/releases/tag/v1.0.0
