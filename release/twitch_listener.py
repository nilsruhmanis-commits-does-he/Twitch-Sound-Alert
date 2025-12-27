"""Twitch Listener - Core Module

Reusable TwitchListener class for connecting to Twitch IRC, monitoring chat messages,
and triggering actions when specific phrases are detected. Designed for both CLI and
GUI integration with callback-based logging and event handling.

Features:
    - Raw TCP socket connection to Twitch IRC
    - Automatic reconnection with exponential backoff
    - Multi-backend audio playback (pygame, winsound, simpleaudio)
    - Thread-safe non-blocking sound playback
    - Callback-based logging and trigger events

Version: 1.0.0
Author: NipSlipFTW
License: MIT
"""

import socket
import threading
import re
import time
import sys
from pathlib import Path

PRIVMSG_RE = re.compile(r"^:([^!]+)!.* PRIVMSG #[^\s]+ :(.+)$")

class TwitchListener:
    def __init__(self, username, channel, oauth_token, sound_file, trigger_code, on_trigger=None, on_log=None):
        self.username = username
        self.channel = channel
        self.oauth_token = oauth_token
        self.sound_file = sound_file
        self.trigger_code = trigger_code
        self.on_trigger = on_trigger or (lambda user, msg: None)
        self.on_log = on_log or (lambda msg: None)
        
        self.running = False
        self.sock = None
        self.thread = None
        self.backoff = 1
        
        self.SERVER = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.RECV_BUF = 4096

    def log(self, msg):
        self.on_log(msg)

    def _make_player(self):
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
            self.log("No audio backend available. Install 'pygame' or 'simpleaudio'.")
        return _noop

    def play_sound(self):
        path = Path(self.sound_file)
        if not path.exists():
            self.log(f"Sound file not found: {path}")
            return
        try:
            player = self._make_player()
            player(str(path))
        except Exception as e:
            self.log(f"Failed to play sound: {e}")

    def connect(self):
        while self.running:
            try:
                sock = socket.socket()
                sock.settimeout(120)
                sock.connect((self.SERVER, self.PORT))
                token = self.oauth_token
                if not token.startswith("oauth:"):
                    token = "oauth:" + token
                sock.sendall(f"PASS {token}\r\n".encode("utf-8"))
                sock.sendall(f"NICK {self.username}\r\n".encode("utf-8"))
                sock.sendall(f"JOIN #{self.channel}\r\n".encode("utf-8"))
                self.log(f"Connected to #{self.channel} as {self.username}")
                return sock
            except Exception as e:
                self.log(f"Connect failed: {e}. Retrying in {self.backoff}s...")
                time.sleep(self.backoff)
                self.backoff = min(self.backoff * 2, 60)
        return None

    def run(self):
        if not self.oauth_token:
            self.log("ERROR: OAuth token not set")
            return

        self.running = True
        self.backoff = 1
        sock = self.connect()
        if not sock:
            self.log("Failed to connect. Aborting.")
            return

        buffer = ""
        backoff = 1

        try:
            while self.running:
                try:
                    data = sock.recv(self.RECV_BUF)
                    if not data:
                        self.log("Connection closed by server. Reconnecting...")
                        sock = self.connect()
                        if not sock:
                            break
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
                                sock = self.connect()
                                if not sock:
                                    break
                            continue

                        if "PRIVMSG" in line:
                            m = PRIVMSG_RE.match(line)
                            if m:
                                user, message = m.group(1), m.group(2)
                                self.log(f"{user}: {message}")
                                if self.trigger_code.lower() in message.lower():
                                    self.log(f"*** TRIGGER DETECTED from {user}! Playing sound... ***")
                                    self.on_trigger(user, message)
                                    threading.Thread(target=self.play_sound, daemon=True).start()

                    backoff = 1

                except (socket.timeout, OSError) as e:
                    self.log(f"Socket error: {e}. Reconnecting...")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 60)
                    sock = self.connect()
                    if not sock:
                        break
                except Exception as e:
                    self.log(f"Unexpected error: {e}. Reconnecting...")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 60)
                    sock = self.connect()
                    if not sock:
                        break
        finally:
            try:
                sock.close()
            except Exception:
                pass
            self.log("Listener stopped.")
            self.running = False

    def start(self):
        if self.thread and self.thread.is_alive():
            self.log("Listener already running.")
            return
        self.thread = threading.Thread(target=self.run, daemon=False)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
