"""Twitch Sound Alert - GUI Version

Tkinter-based graphical user interface for monitoring Twitch chat and playing
sounds when specific trigger phrases are detected. Features persistent configuration
and real-time activity logging.

Usage:
    python twitch-alert-gui.py

Version: 1.0.0
Author: Twitch Sound Alert Contributors
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import webbrowser
from pathlib import Path
from twitch_listener import TwitchListener

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "username": "nipslipftw",
    "channel": "clarawrrxd",
    "trigger_code": "!pokecatch",
    "sound_file": "sound.mp3"
}

class TwitchAlertGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitch Sound Alert")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.listener = None
        self.config = self.load_config()
        
        # Create UI
        self.create_widgets()
        self.update_status()

    def load_config(self):
        if Path(CONFIG_FILE).exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {e}")
        return DEFAULT_CONFIG.copy()

    def save_config(self, show_popup=True):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=2)
            if show_popup:
                messagebox.showinfo("Success", "Config saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Twitch Sound Alert", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Config Frame
        config_frame = ttk.LabelFrame(self.root, text="Configuration", padding=10)
        config_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        # Username
        tk.Label(config_frame, text="Twitch Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = tk.Entry(config_frame, width=40)
        self.username_entry.insert(0, self.config.get("username", ""))
        self.username_entry.grid(row=0, column=1, sticky=tk.W, padx=5)

        # Channel
        tk.Label(config_frame, text="Channel to Join:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.channel_entry = tk.Entry(config_frame, width=40)
        self.channel_entry.insert(0, self.config.get("channel", ""))
        self.channel_entry.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Trigger Code
        tk.Label(config_frame, text="Trigger Code:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.trigger_entry = tk.Entry(config_frame, width=40)
        self.trigger_entry.insert(0, self.config.get("trigger_code", ""))
        self.trigger_entry.grid(row=2, column=1, sticky=tk.W, padx=5)

        # Sound File
        tk.Label(config_frame, text="Sound File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        sound_frame = tk.Frame(config_frame)
        sound_frame.grid(row=3, column=1, sticky=tk.W, padx=5)
        self.sound_entry = tk.Entry(sound_frame, width=30)
        self.sound_entry.insert(0, self.config.get("sound_file", ""))
        self.sound_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(sound_frame, text="Browse", command=self.browse_sound).pack(side=tk.LEFT)

        # OAuth Token Frame
        token_frame = ttk.LabelFrame(self.root, text="OAuth Token", padding=10)
        token_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        tk.Label(token_frame, text="Token (hidden):", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        token_subframe = tk.Frame(token_frame)
        token_subframe.pack(fill=tk.X, pady=5)
        self.token_entry = tk.Entry(token_subframe, show="*", width=50)
        self.token_entry.insert(0, os.getenv("TWITCH_OAUTH_TOKEN", ""))
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(token_subframe, text="Show", command=self.toggle_token_visibility).pack(side=tk.LEFT, padx=5)

        # OAuth Link Button
        tk.Button(token_frame, text="🔗 Get OAuth Token from Twitch", command=self.open_oauth_link, bg="#9147ff", fg="white", font=("Arial", 10, "bold"), width=35).pack(pady=5)

        # Status Frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        self.status_label = tk.Label(status_frame, text="Stopped", font=("Arial", 12, "bold"), fg="red")
        self.status_label.pack(pady=5)

        # Control Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.start_btn = tk.Button(button_frame, text="Start Listening", command=self.start_listener, bg="green", fg="white", width=20)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(button_frame, text="Stop Listening", command=self.stop_listener, bg="red", fg="white", width=20, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Save Config Button
        tk.Button(self.root, text="Save Configuration", command=self.save_config_and_update, bg="blue", fg="white", width=30).pack(pady=5)

        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(log_frame, height=12, width=70, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)

        # Clear Log Button
        tk.Button(self.root, text="Clear Log", command=lambda: self.log_text.delete("1.0", tk.END), width=30).pack(pady=5)

    def browse_sound(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")])
        if file:
            self.sound_entry.delete(0, tk.END)
            self.sound_entry.insert(0, file)

    def toggle_token_visibility(self):
        if self.token_entry.cget("show") == "*":
            self.token_entry.config(show="")
        else:
            self.token_entry.config(show="*")

    def open_oauth_link(self):
        try:
            webbrowser.open("https://twitchtokengenerator.com/")
            self.log_text.insert(tk.END, "Opening OAuth token generator in browser...\n")
            self.log_text.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open browser: {e}")

    def save_config_and_update(self, show_popup=True):
        self.config = {
            "username": self.username_entry.get().strip(),
            "channel": self.channel_entry.get().strip(),
            "trigger_code": self.trigger_entry.get().strip(),
            "sound_file": self.sound_entry.get().strip()
        }
        self.save_config(show_popup=show_popup)
        if self.listener and self.listener.running:
            self.log_text.insert(tk.END, "Config updated (restart listener to apply).\n")
            self.log_text.see(tk.END)
            self.root.update()

    def start_listener(self):
        # Update config from UI fields
        self.config = {
            "username": self.username_entry.get().strip(),
            "channel": self.channel_entry.get().strip(),
            "trigger_code": self.trigger_entry.get().strip(),
            "sound_file": self.sound_entry.get().strip()
        }
        
        # Validate before saving
        if not self.config["username"]:
            messagebox.showerror("Error", "Username is required")
            return
        if not self.config["channel"]:
            messagebox.showerror("Error", "Channel is required")
            return
        if not self.config["sound_file"]:
            messagebox.showerror("Error", "Sound file is required")
            return

        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Error", "OAuth token is required")
            return

        # Save valid config silently
        self.save_config(show_popup=False)
        
        # Also set env var for the listener
        os.environ["TWITCH_OAUTH_TOKEN"] = token

        self.listener = TwitchListener(
            username=self.config["username"],
            channel=self.config["channel"],
            oauth_token=token,
            sound_file=self.config["sound_file"],
            trigger_code=self.config["trigger_code"],
            on_trigger=lambda user, msg: self.log_text.insert(tk.END, f"[TRIGGER] {user}: {msg}\n") or self.log_text.see(tk.END),
            on_log=self.on_log_message
        )
        self.listener.start()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.update_status()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status()

    def on_log_message(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def update_status(self):
        if self.listener and self.listener.running:
            self.status_label.config(text="Listening...", fg="green")
        else:
            self.status_label.config(text="Stopped", fg="red")
        self.root.after(1000, self.update_status)

    def on_closing(self):
        if self.listener and self.listener.running:
            if messagebox.askokcancel("Quit", "Listener is running. Stop and quit?"):
                self.stop_listener()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = TwitchAlertGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    root.mainloop()
