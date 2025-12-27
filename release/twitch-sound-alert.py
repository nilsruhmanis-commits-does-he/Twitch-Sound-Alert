"""Twitch Sound Alert - CLI Version

Standalone command-line interface for monitoring Twitch chat and playing sounds
when specific trigger phrases are detected.

Usage:
    1. Set TWITCH_OAUTH_TOKEN environment variable
    2. Configure USERNAME, CHANNEL, TRIGGER_CODE, and SOUND_FILE constants below
    3. Run: python twitch-sound-alert.py

Version: 1.0.0
Author: Twitch Sound Alert Contributors
License: MIT
"""

import os
import socket
import threading
import re
import time
import sys
from pathlib import Path

# --------------------- CONFIGURATION ---------------------
USERNAME = "nipslipftw"          # Your Twitch username (lowercase)
CHANNEL = "clarawrrxd"           # Channel to join (without #)
TRIGGER_CODE = "!pokecatch"      # Trigger phrase (case-insensitive)
SOUND_FILE = "sound.mp3"         # Path to your sound file
SERVER = "irc.chat.twitch.tv"
PORT = 6667
RECV_BUF = 4096
# ---------------------------------------------------------

# Playback: prefer pygame (MP3/OGG), fallback to winsound/simpleaudio for WAV, else noop
def _make_player():
    try:
        import pygame
        def _pygame_play(path):
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        return _pygame_play
    except Exception:
        pass

    if sys.platform.startswith("win"):
        try:
            import winsound
            def _winsound_play(path):
                if Path(path).suffix.lower() != ".wav":
                    raise RuntimeError("winsound supports only .wav files")
                winsound.PlaySound(str(path), winsound.SND_FILENAME)
            return _winsound_play
        except Exception:
            pass

    try:
        import simpleaudio as sa
        def _simpleaudio_play(path):
            if Path(path).suffix.lower() != ".wav":
                raise RuntimeError("simpleaudio supports only .wav files")
            wave_obj = sa.WaveObject.from_wave_file(str(path))
            wave_obj.play()
        return _simpleaudio_play
    except Exception:
        pass

    def _noop(path):
        print("No audio backend available. Install 'pygame' or 'simpleaudio'.")
    return _noop

_play_sound_impl = _make_player()

def play_sound_file(path):
    path = Path(path)
    if not path.exists():
        print(f"Sound file not found: {path}")
        return
    try:
        _play_sound_impl(str(path))
    except Exception as e:
        print(f"Failed to play sound: {e}")

def get_oauth_token():
    token = os.getenv("TWITCH_OAUTH_TOKEN")
    if not token:
        print("ERROR: TWITCH_OAUTH_TOKEN not set.")
        print("Create an OAuth token at https://twitchapps.com/tmi/, then set:")
        print('  PowerShell: $env:TWITCH_OAUTH_TOKEN = "oauth:YOUR_TOKEN"')
        print('  cmd: set TWITCH_OAUTH_TOKEN=oauth:YOUR_TOKEN')
        raise SystemExit(1)
    token = token.strip()
    if not token.startswith("oauth:"):
        token = "oauth:" + token
    return token

def connect_to_twitch(oauth_token, backoff=1):
    while True:
        try:
            sock = socket.socket()
            sock.settimeout(120)
            sock.connect((SERVER, PORT))
            sock.sendall(f"PASS {oauth_token}\r\n".encode("utf-8"))
            sock.sendall(f"NICK {USERNAME}\r\n".encode("utf-8"))
            sock.sendall(f"JOIN #{CHANNEL}\r\n".encode("utf-8"))
            print(f"Connected to #{CHANNEL} as {USERNAME}")
            return sock
        except Exception as e:
            print(f"Connect failed: {e}. Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)

PRIVMSG_RE = re.compile(r"^:([^!]+)!.* PRIVMSG #[^\s]+ :(.+)$")

def parse_privmsg(line):
    m = PRIVMSG_RE.match(line)
    if m:
        return m.group(1), m.group(2)
    return None, None

def run_listener():
    oauth_token = get_oauth_token()
    sock = connect_to_twitch(oauth_token)
    buffer = ""
    backoff = 1

    try:
        while True:
            try:
                data = sock.recv(RECV_BUF)
                if not data:
                    print("Connection closed by server. Reconnecting...")
                    sock = connect_to_twitch(oauth_token)
                    continue

                buffer += data.decode("utf-8", errors="ignore")
                while "\r\n" in buffer:
                    line, buffer = buffer.split("\r\n", 1)
                    if not line:
                        continue

                    if line.startswith("PING"):
                        try:
                            sock.sendall("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                        except Exception:
                            sock = connect_to_twitch(oauth_token)
                        continue

                    if "PRIVMSG" in line:
                        user, message = parse_privmsg(line)
                        if user:
                            print(f"{user}: {message}")
                            if TRIGGER_CODE.lower() in message.lower():
                                print(f"*** TRIGGER DETECTED from {user}! Playing sound... ***")
                                threading.Thread(target=play_sound_file, args=(SOUND_FILE,), daemon=True).start()

                backoff = 1

            except (socket.timeout, OSError) as e:
                print(f"Socket error: {e}. Reconnecting...")
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)
                sock = connect_to_twitch(oauth_token)
            except Exception as e:
                print(f"Unexpected error: {e}. Reconnecting...")
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)
                sock = connect_to_twitch(oauth_token)
    except KeyboardInterrupt:
        print("\nInterrupted by user — exiting.")
    finally:
        try:
            sock.close()
        except Exception:
            pass

if __name__ == "__main__":
    run_listener()
