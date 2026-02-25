# Desktop Shortcut Setup

## Quick Start

I've created desktop shortcuts for you! Look on your Desktop for:

### **EmailAssistantApp.app** (Recommended ⭐)
- Double-click this app icon
- Automatically opens Terminal and starts the assistant
- Most user-friendly option

### **EmailAssistant.command**
- Double-click to run in Terminal
- Shows the 📧 Email Assistant directly

## First Time Setup

macOS will show a security warning the first time. To fix:

**Option 1:** Right-click the file → Click "Open"

**Option 2:** 
1. Go to System Preferences → Security & Privacy → General
2. Click "Allow Anyway" next to the blocked app

## What It Does

When you double-click:
1. Opens Terminal
2. Starts the Email Assistant
3. Connects to Microsoft Outlook
4. Ready to check your emails!

## Usage

Once running:
- Press `[Enter]` to check emails now
- Type `auto` to check every 5 minutes automatically
- Type `quit` to exit

## Manual Run (if needed)

If the shortcut doesn't work, you can always run manually:

```bash
cd ~/.openclaw/workspace/skills/boss-assistant
python3 email_assistant_cli.py
```
