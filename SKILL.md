---
name: boss-assistant
description: AI assistant that monitors emails from your boss, automatically completes tasks, learns new skills on the fly, and presents work for approval. Use when you want to automate responses to your boss's requests.
triggers:
  - boss assistant
  - handle boss email
  - automate boss tasks
  - dbergman@onwasa.com
---

# Boss Assistant

**An AI assistant that monitors your boss's emails, completes tasks automatically, learns new skills, and gets your approval.**

## What It Does

1. 📧 **Monitors Email** - Watches for emails from dbergman@onwasa.com
2. 🧠 **Understands Requests** - Parses what your boss is asking for
3. 🤖 **Executes Tasks** - Tries to complete the work automatically
4. 📚 **Learns New Skills** - If it doesn't know how, it figures it out
5. ✅ **Gets Approval** - Shows you the work before sending/finalizing

## Features

### Email Monitoring
- Checks for new emails every 5 minutes
- Filters by sender (dbergman@onwasa.com)
- Extracts the request/task from email body

### Task Execution
- Analyzes what needs to be done
- Uses existing skills when available
- Creates new skills for unknown tasks

### Learning System
- When encountering a new type of request, it:
  - Analyzes the task
  - Creates a skill to handle it
  - Saves the skill for future use

### Approval Workflow
- Presents completed work in a GUI
- Shows what was done and why
- You approve, edit, or reject
- Only sends after your approval

## Usage

### Start the Assistant

```bash
python boss_assistant.py --start
```

The assistant will:
1. Connect to your email
2. Monitor for boss emails
3. Process new requests automatically
4. Present results for your approval

### Configuration

Create `.boss_assistant_config.json`:
```json
{
  "email": "your.email@onwasa.com",
  "boss_email": "dbergman@onwasa.com",
  "check_interval_minutes": 5,
  "auto_reply": false,
  "require_approval": true
}
```

### How It Works

```
📧 Boss Email Arrives
        ↓
📖 Parse Request
        ↓
🤖 Check if skill exists
        ↓
   ┌───────────────────────┐
   │  Skill exists?        │
   └───────────────────────┘
       Yes ↓        ↓ No
    ┌─────┐     ┌──────────┐
    │Use  │     │Learn new │
    │skill│     │skill     │
    └─────┘     └──────────┘
        ↓
✅ Present to you
        ↓
   ┌───────────────────────┐
   │  Your decision:       │
   │  [Approve] [Edit]     │
   │  [Reject] [Defer]     │
   └───────────────────────┘
```

## Task Categories

The assistant can handle:
- 📊 Reports and data analysis
- 📧 Email drafting and responses
- 📅 Calendar scheduling
- 📁 File organization
- 🔍 Research tasks
- 💻 Technical troubleshooting
- 📝 Documentation
- And learns more over time!

## Safety

- ✅ Never sends anything without approval
- ✅ Shows you exactly what it did
- ✅ Logs all actions
- ✅ You can always override

## Example

**Boss Email:**
> "Can you pull the Q3 sales report and email it to the team?"

**Assistant Response:**
```
📧 New Task from Boss
─────────────────────
Task: Pull Q3 sales report and email to team

🤖 What I did:
   • Accessed sales system
   • Generated Q3 report (sales_q3_2025.xlsx)
   • Drafted email to team@onwasa.com

📎 Attachments:
   • sales_q3_2025.xlsx

📝 Draft Email:
   "Team, Please find attached the Q3 sales report..."

What would you like to do?
[Send] [Edit] [Add Comments] [Reject]
```

## Files

- `boss_assistant.py` - Main assistant script
- `email_monitor.py` - Email checking module
- `task_parser.py` - Request understanding
- `skill_learner.py` - Creates new skills
- `approval_gui.py` - Approval interface
- `learned_skills/` - Folder for auto-generated skills

## License

MIT - Use at your own risk. Always review before sending! 😊
