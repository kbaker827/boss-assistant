# Email Assistant for macOS 📧

**AI assistant that manages your entire work inbox on macOS.**

## What It Does

1. 📧 **Monitors ALL Emails** - Watches youremail@example.com inbox
2. 🚫 **Spam Detection** - Identifies spam and junk mail
3. 🧠 **Smart Task Handling** - Handles legitimate work emails
4. 📚 **Learns Skills** - Learns how to handle new types of requests
5. ✅ **Approval Required** - Shows you everything before acting

## Features

### For Spam Emails
- Detects spam automatically
- Finds unsubscribe links
- Offers to unsubscribe & block
- Moves to junk folder
- **Always asks before doing anything**

### For Work Emails
- Parses requests
- Executes tasks using learned skills
- Learns new skills when needed
- **Always asks before sending/replying**

## Quick Start

### 1. Setup
```bash
python setup.py
```

### 2. Configure
Edit `~/.email_assistant_config.json`:
```json
{
  "email": "youremail@example.com",
  "mail_app": "outlook",
  "check_interval_seconds": 30,
  "require_approval": true,
  "spam_detection": true
}
```

### 3. Run
```bash
python email_assistant.py
```

## How It Works

```
📧 New Email Arrives
        ↓
   ┌─────────────────────┐
   │ Is it spam?         │
   └─────────────────────┘
      Yes ↓       ↓ No
   ┌─────────┐  ┌──────────────────┐
   │Unsubscribe│ │Parse task        │
   │Block      │ │Execute skill     │
   │sender     │ │                  │
   └─────────┘  └──────────────────┘
        ↓              ↓
   ┌───────────────────────────────┐
   │  Show you for approval        │
   │  [Approve] [Edit] [Block]     │
   └───────────────────────────────┘
```

## Safety

- 🔒 **Never acts without your approval**
- 🔒 **Shows you exactly what it will do**
- 🔒 **Whitelist protection** for important domains
- 🔒 **Easy to block/unblock senders**

## Files

| File | Purpose |
|------|---------|
| `email_assistant.py` | Main GUI application |
| `setup.py` | Configuration setup |
| `SKILL.md` | Documentation |

## Requirements

- macOS
- Python 3.8+
- Outlook for Mac or Apple Mail

## Disclaimer

⚠️ This tool requires your approval for every action. Never runs automatically.
