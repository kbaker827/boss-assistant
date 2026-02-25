#!/bin/bash
# Email Assistant Launcher
# Double-click to start monitoring your emails

cd "$HOME/.openclaw/workspace/skills/boss-assistant"
clear
echo "📧 Starting Email Assistant..."
echo ""
python3 email_assistant_cli.py
