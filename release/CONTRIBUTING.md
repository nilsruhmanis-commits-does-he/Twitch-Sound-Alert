# Contributing to Twitch Sound Alert

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Include detailed steps to reproduce
3. Provide system information (OS, Python version)
4. Include error messages and logs

### Suggesting Features

1. Check if the feature has already been suggested
2. Explain the use case and benefits
3. Consider implementation complexity
4. Be open to discussion and alternatives

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the code style
4. Test your changes thoroughly
5. Update documentation as needed
6. Commit with clear messages (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/twitwitch-sound-alert.git
cd twitwitch-sound-alert

# Run setup script
./setup.sh  # or setup.bat on Windows

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\Activate.ps1 on Windows
```

## Code Style

- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Comment complex logic

## Testing

Before submitting:

1. Test both GUI and CLI versions
2. Verify reconnection logic works
3. Test with different audio formats
4. Ensure error handling works correctly
5. Check that configuration persists properly

## Architecture Guidelines

### Threading Model
- Main thread handles IRC socket I/O
- Use daemon threads for sound playback
- Never block the main thread with long operations

### Error Handling
- Network errors: Auto-reconnect with backoff
- Audio errors: Log and continue (don't crash)
- Config errors: Validate before processing

### Adding Features

#### New Trigger Types
Modify `twitch_listener.py` message detection (lines ~148-154)

#### New Audio Backends
Add to `_make_player()` fallback chain (lines ~38-76)

#### Connection Logic
Update `connect()` or main `run()` loop (lines ~86-180)

See `.github/copilot-instructions.md` for detailed architecture documentation.

## Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format
- Update copilot-instructions.md for architectural changes
- Add inline comments for complex logic

## Questions?

Feel free to open an issue for:
- Clarification on documentation
- Help with development setup
- Discussion of potential contributions

Thank you for contributing! 🎉
