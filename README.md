# Boss Assistant 🤖

**AI assistant that monitors emails from your boss, automatically completes tasks, learns new skills, and presents work for your approval.**

## Quick Start

### 1. Setup
```bash
python setup.py
```

### 2. Configure
Edit `~/.boss_assistant_config.json`:
```json
{
  "boss_email": "dbergman@onwasa.com",
  "email_provider": "outlook",
  "check_interval_minutes": 5,
  "require_approval": true
}
```

### 3. Run
```bash
python boss_assistant.py
```

## How It Works

1. **Monitors Email** - Checks for emails from your boss every 5 minutes
2. **Understands Requests** - Uses AI to parse what needs to be done
3. **Learns Skills** - Creates new skills for task types it hasn't seen before
4. **Does the Work** - Executes tasks using OpenClaw/tools
5. **Gets Approval** - Shows you the work before finalizing

## Example

**Boss emails you:**
> "Can you pull the Q3 sales numbers and send them to the team?"

**Assistant does:**
1. Recognizes this as a "generate_report" task
2. Either uses existing skill or learns how to do it
3. Generates the report
4. Drafts email to team
5. **Shows you for approval before sending**

## Features

- ✅ Never sends anything without your approval
- ✅ Learns from each task to get better
- ✅ Shows exactly what it did and why
- ✅ Works offline with learned skills
- ✅ Secure - stores everything locally

## Files

| File | Purpose |
|------|---------|
| `boss_assistant.py` | Main GUI application |
| `email_connector.py` | Email system connection |
| `task_executor.py` | Task execution engine |
| `setup.py` | Initial setup |

## Safety

- 🔒 Never auto-sends emails
- 🔒 All approval is manual
- 🔒 Local storage only
- 🔒 Logs everything for review

## Disclaimer

This is an automation tool. Always review before sending anything to your boss! 😊
