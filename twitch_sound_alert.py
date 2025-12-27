#!/usr/bin/env python3
"""
Twitch Sound Alert Bot
A lightweight bot that monitors Twitch chat and plays sounds when trigger phrases appear.
"""

import socket
import threading
import time
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional, List
import logging

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AudioPlayer:
    """Handles audio playback in a non-blocking daemon thread."""
    
    def __init__(self):
        self.initialized = False
        self.lock = threading.Lock()
        
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.initialized = True
                logger.info("Audio system initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize pygame mixer: {e}")
                self.initialized = False
        else:
            logger.warning("pygame not available - audio playback disabled")
    
    def play_sound(self, filepath: str):
        """Play a sound file in a daemon thread (non-blocking)."""
        if not self.initialized:
            logger.warning("Audio system not initialized")
            return
        
        if not os.path.exists(filepath):
            logger.error(f"Sound file not found: {filepath}")
            return
        
        thread = threading.Thread(target=self._play_sound_thread, args=(filepath,), daemon=True)
        thread.start()
    
    def _play_sound_thread(self, filepath: str):
        """Internal method to play sound in thread."""
        with self.lock:
            try:
                sound = pygame.mixer.Sound(filepath)
                sound.play()
                # Wait for sound to finish
                while pygame.mixer.get_busy():
                    time.sleep(0.1)
                logger.info(f"Played sound: {filepath}")
            except Exception as e:
                logger.error(f"Error playing sound {filepath}: {e}")


class ConfigManager:
    """Manages persistent configuration."""
    
    DEFAULT_CONFIG = {
        "twitch_channel": "",
        "oauth_token": "",
        "bot_username": "",
        "triggers": {
            "!hello": "sounds/hello.wav",
            "!welcome": "sounds/welcome.wav"
        },
        "reconnect_delay": 5,
        "max_reconnect_delay": 300
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded configuration from {self.config_file}")
                return config
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            logger.info("No config file found, using defaults")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value."""
        self.config[key] = value


class TwitchBot:
    """Main Twitch IRC bot with auto-reconnection."""
    
    IRC_HOST = "irc.chat.twitch.tv"
    IRC_PORT = 6667
    
    def __init__(self, config_manager: ConfigManager, audio_player: AudioPlayer):
        self.config = config_manager
        self.audio = audio_player
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.connected = False
        self.reconnect_delay = config_manager.get("reconnect_delay", 5)
        self.max_reconnect_delay = config_manager.get("max_reconnect_delay", 300)
        self.current_reconnect_delay = self.reconnect_delay
    
    def connect(self) -> bool:
        """Connect to Twitch IRC server."""
        try:
            self.socket = socket.socket()
            self.socket.settimeout(10)
            self.socket.connect((self.IRC_HOST, self.IRC_PORT))
            
            # Authenticate
            oauth_token = self.config.get("oauth_token", "")
            username = self.config.get("bot_username", "")
            channel = self.config.get("twitch_channel", "")
            
            if not oauth_token or not username or not channel:
                logger.error("Missing configuration: oauth_token, bot_username, or twitch_channel")
                return False
            
            self.socket.send(f"PASS {oauth_token}\r\n".encode('utf-8'))
            self.socket.send(f"NICK {username}\r\n".encode('utf-8'))
            self.socket.send(f"JOIN #{channel}\r\n".encode('utf-8'))
            
            self.connected = True
            self.current_reconnect_delay = self.reconnect_delay
            logger.info(f"Connected to #{channel}")
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from Twitch IRC server."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False
        logger.info("Disconnected from Twitch")
    
    def send_message(self, message: str):
        """Send a message to the channel."""
        if not self.connected or not self.socket:
            return
        
        channel = self.config.get("twitch_channel", "")
        try:
            self.socket.send(f"PRIVMSG #{channel} :{message}\r\n".encode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self.connected = False
    
    def handle_message(self, message: str):
        """Process received IRC message."""
        # Handle PING
        if message.startswith("PING"):
            pong = message.replace("PING", "PONG")
            self.socket.send(f"{pong}\r\n".encode('utf-8'))
            return
        
        # Parse chat messages
        if "PRIVMSG" in message:
            try:
                # Extract the chat message
                parts = message.split("PRIVMSG", 1)
                if len(parts) > 1:
                    msg_part = parts[1].split(":", 1)
                    if len(msg_part) > 1:
                        chat_message = msg_part[1].strip()
                        
                        # Check for triggers
                        triggers = self.config.get("triggers", {})
                        for trigger, sound_file in triggers.items():
                            if trigger.lower() in chat_message.lower():
                                logger.info(f"Trigger detected: {trigger}")
                                self.audio.play_sound(sound_file)
                                break
            except Exception as e:
                logger.error(f"Error handling message: {e}")
    
    def run(self):
        """Main bot loop with auto-reconnection."""
        self.running = True
        
        while self.running:
            if not self.connected:
                if not self.connect():
                    logger.info(f"Reconnecting in {self.current_reconnect_delay} seconds...")
                    time.sleep(self.current_reconnect_delay)
                    # Exponential backoff
                    self.current_reconnect_delay = min(
                        self.current_reconnect_delay * 2,
                        self.max_reconnect_delay
                    )
                    continue
            
            try:
                # Receive data
                response = self.socket.recv(2048).decode('utf-8', errors='ignore')
                
                if not response:
                    logger.warning("Empty response, connection lost")
                    self.connected = False
                    continue
                
                # Handle messages
                for message in response.split('\r\n'):
                    if message:
                        self.handle_message(message)
                        
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                self.connected = False
                self.disconnect()
        
        self.disconnect()
    
    def stop(self):
        """Stop the bot."""
        self.running = False
        self.disconnect()


def main():
    """CLI entry point."""
    print("=== Twitch Sound Alert Bot ===")
    print("v1.0.0\n")
    
    if not PYGAME_AVAILABLE:
        print("Warning: pygame not installed. Audio playback will not work.")
        print("Install with: pip install pygame\n")
    
    # Initialize components
    config_manager = ConfigManager()
    audio_player = AudioPlayer()
    bot = TwitchBot(config_manager, audio_player)
    
    # Check configuration
    if not config_manager.get("twitch_channel"):
        print("Error: Configuration required!")
        print("Please edit config.json with your Twitch credentials.")
        config_manager.save_config()
        print(f"Template config file created: {config_manager.config_file}")
        return
    
    print(f"Channel: #{config_manager.get('twitch_channel')}")
    print(f"Bot: {config_manager.get('bot_username')}")
    print(f"Triggers: {len(config_manager.get('triggers', {}))}")
    print("\nConnecting to Twitch...\n")
    
    # Run bot
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        bot.stop()
        print("Goodbye!")


if __name__ == "__main__":
    main()
