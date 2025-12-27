#!/usr/bin/env python3
"""
Setup script for Twitch Sound Alert
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="twitch-sound-alert",
    version="1.0.0",
    description="A lightweight Python bot that monitors Twitch chat and plays custom sounds when trigger phrases appear",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Twitch Sound Alert Contributors",
    url="https://github.com/nilsruhmanis-commits-does-he/Twitch-Sound-Alert",
    py_modules=["twitch_sound_alert", "gui"],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "twitch-sound-alert=twitch_sound_alert:main",
            "twitch-sound-alert-gui=gui:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="twitch bot sound alert chat irc",
)
