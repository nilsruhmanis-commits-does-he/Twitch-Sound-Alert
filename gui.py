#!/usr/bin/env python3
"""
GUI interface for Twitch Sound Alert Bot
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import os
from datetime import datetime
from twitch_sound_alert import TwitchBot, ConfigManager, AudioPlayer, PYGAME_AVAILABLE
import logging


class TextHandler(logging.Handler):
    """Custom logging handler that redirects to a text widget."""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)


class TwitchSoundAlertGUI:
    """Main GUI application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Twitch Sound Alert v1.0.0")
        self.root.geometry("800x600")
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.audio_player = AudioPlayer()
        self.bot = None
        self.bot_thread = None
        self.running = False
        
        # Setup UI
        self.setup_ui()
        
        # Load configuration
        self.load_config_to_ui()
        
        # Setup logging to GUI
        self.setup_logging()
    
    def setup_ui(self):
        """Create the GUI layout."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configuration tab
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text='Configuration')
        self.setup_config_tab(config_frame)
        
        # Triggers tab
        triggers_frame = ttk.Frame(notebook)
        notebook.add(triggers_frame, text='Triggers')
        self.setup_triggers_tab(triggers_frame)
        
        # Log tab
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text='Log')
        self.setup_log_tab(log_frame)
        
        # Control buttons at bottom
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Bot", command=self.start_bot)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Bot", command=self.stop_bot, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        self.save_button = ttk.Button(control_frame, text="Save Config", command=self.save_config)
        self.save_button.pack(side='left', padx=5)
        
        self.status_label = ttk.Label(control_frame, text="Status: Stopped", foreground='red')
        self.status_label.pack(side='right', padx=5)
    
    def setup_config_tab(self, parent):
        """Setup configuration tab."""
        # Twitch Channel
        ttk.Label(parent, text="Twitch Channel:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.channel_entry = ttk.Entry(parent, width=40)
        self.channel_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Bot Username
        ttk.Label(parent, text="Bot Username:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.username_entry = ttk.Entry(parent, width=40)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # OAuth Token
        ttk.Label(parent, text="OAuth Token:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.oauth_entry = ttk.Entry(parent, width=40, show='*')
        self.oauth_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Help text
        help_text = (
            "Get your OAuth token from: https://twitchapps.com/tmi/\n"
            "Token format: oauth:xxxxxxxxxxxxxx\n\n"
            "Bot username should match the account used for the OAuth token."
        )
        help_label = ttk.Label(parent, text=help_text, justify='left', foreground='blue')
        help_label.grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=10)
        
        # Reconnection settings
        ttk.Label(parent, text="Reconnect Delay (seconds):").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.reconnect_entry = ttk.Entry(parent, width=40)
        self.reconnect_entry.grid(row=4, column=1, padx=5, pady=5)
        self.reconnect_entry.insert(0, "5")
        
        ttk.Label(parent, text="Max Reconnect Delay (seconds):").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.max_reconnect_entry = ttk.Entry(parent, width=40)
        self.max_reconnect_entry.grid(row=5, column=1, padx=5, pady=5)
        self.max_reconnect_entry.insert(0, "300")
        
        if not PYGAME_AVAILABLE:
            warning = ttk.Label(
                parent, 
                text="⚠ pygame not installed - audio playback disabled",
                foreground='red'
            )
            warning.grid(row=6, column=0, columnspan=2, padx=5, pady=10)
    
    def setup_triggers_tab(self, parent):
        """Setup triggers tab."""
        # Instructions
        ttk.Label(
            parent, 
            text="Add trigger phrases and their associated sound files:",
            font=('TkDefaultFont', 10, 'bold')
        ).pack(padx=5, pady=5, anchor='w')
        
        # Triggers list
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for triggers
        columns = ('Trigger', 'Sound File')
        self.triggers_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        self.triggers_tree.heading('Trigger', text='Trigger Phrase')
        self.triggers_tree.heading('Sound File', text='Sound File Path')
        self.triggers_tree.column('Trigger', width=200)
        self.triggers_tree.column('Sound File', width=400)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.triggers_tree.yview)
        self.triggers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.triggers_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Trigger", command=self.add_trigger).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Remove Trigger", command=self.remove_trigger).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Test Sound", command=self.test_sound).pack(side='left', padx=2)
    
    def setup_log_tab(self, parent):
        """Setup log tab."""
        self.log_text = scrolledtext.ScrolledText(parent, state='disabled', height=20)
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def setup_logging(self):
        """Configure logging to GUI."""
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_handler)
    
    def load_config_to_ui(self):
        """Load configuration values into UI elements."""
        self.channel_entry.delete(0, tk.END)
        self.channel_entry.insert(0, self.config_manager.get("twitch_channel", ""))
        
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, self.config_manager.get("bot_username", ""))
        
        self.oauth_entry.delete(0, tk.END)
        self.oauth_entry.insert(0, self.config_manager.get("oauth_token", ""))
        
        self.reconnect_entry.delete(0, tk.END)
        self.reconnect_entry.insert(0, str(self.config_manager.get("reconnect_delay", 5)))
        
        self.max_reconnect_entry.delete(0, tk.END)
        self.max_reconnect_entry.insert(0, str(self.config_manager.get("max_reconnect_delay", 300)))
        
        # Load triggers
        self.triggers_tree.delete(*self.triggers_tree.get_children())
        triggers = self.config_manager.get("triggers", {})
        for trigger, sound_file in triggers.items():
            self.triggers_tree.insert('', 'end', values=(trigger, sound_file))
    
    def save_config(self):
        """Save configuration from UI to file."""
        try:
            self.config_manager.set("twitch_channel", self.channel_entry.get())
            self.config_manager.set("bot_username", self.username_entry.get())
            self.config_manager.set("oauth_token", self.oauth_entry.get())
            self.config_manager.set("reconnect_delay", int(self.reconnect_entry.get()))
            self.config_manager.set("max_reconnect_delay", int(self.max_reconnect_entry.get()))
            
            # Save triggers
            triggers = {}
            for item in self.triggers_tree.get_children():
                values = self.triggers_tree.item(item, 'values')
                triggers[values[0]] = values[1]
            self.config_manager.set("triggers", triggers)
            
            self.config_manager.save_config()
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def add_trigger(self):
        """Add a new trigger."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Trigger")
        dialog.geometry("400x150")
        
        ttk.Label(dialog, text="Trigger Phrase:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        trigger_entry = ttk.Entry(dialog, width=30)
        trigger_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Sound File:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        sound_entry = ttk.Entry(dialog, width=30)
        sound_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def browse_file():
            filename = filedialog.askopenfilename(
                title="Select Sound File",
                filetypes=[
                    ("Audio Files", "*.mp3 *.wav *.ogg"),
                    ("MP3 Files", "*.mp3"),
                    ("WAV Files", "*.wav"),
                    ("OGG Files", "*.ogg"),
                    ("All Files", "*.*")
                ]
            )
            if filename:
                sound_entry.delete(0, tk.END)
                sound_entry.insert(0, filename)
        
        ttk.Button(dialog, text="Browse", command=browse_file).grid(row=1, column=2, padx=5, pady=5)
        
        def add():
            trigger = trigger_entry.get()
            sound_file = sound_entry.get()
            if trigger and sound_file:
                self.triggers_tree.insert('', 'end', values=(trigger, sound_file))
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill in both fields")
        
        ttk.Button(dialog, text="Add", command=add).grid(row=2, column=1, padx=5, pady=10)
    
    def remove_trigger(self):
        """Remove selected trigger."""
        selected = self.triggers_tree.selection()
        if selected:
            self.triggers_tree.delete(selected)
        else:
            messagebox.showwarning("Warning", "Please select a trigger to remove")
    
    def test_sound(self):
        """Test the selected sound file."""
        selected = self.triggers_tree.selection()
        if selected:
            values = self.triggers_tree.item(selected[0], 'values')
            sound_file = values[1]
            self.audio_player.play_sound(sound_file)
        else:
            messagebox.showwarning("Warning", "Please select a trigger to test")
    
    def start_bot(self):
        """Start the bot in a separate thread."""
        if self.running:
            return
        
        # Validate configuration
        if not self.channel_entry.get() or not self.username_entry.get() or not self.oauth_entry.get():
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        # Save config before starting
        self.save_config()
        
        # Create new bot instance
        self.bot = TwitchBot(self.config_manager, self.audio_player)
        
        # Start bot in thread
        self.bot_thread = threading.Thread(target=self.bot.run, daemon=True)
        self.bot_thread.start()
        
        self.running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="Status: Running", foreground='green')
    
    def stop_bot(self):
        """Stop the bot."""
        if not self.running:
            return
        
        if self.bot:
            self.bot.stop()
        
        self.running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Status: Stopped", foreground='red')


def main():
    """GUI entry point."""
    root = tk.Tk()
    app = TwitchSoundAlertGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
