#!/bin/bash
pkg update -y
pkg upgrade -y
pkg install python -y
pkg install clang rust -y
pip install -r requirements.txt
echo "✅ Installation complete! Run the bot with: python bot.py"
