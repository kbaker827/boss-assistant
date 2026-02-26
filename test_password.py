#!/usr/bin/env python3
"""Quick test - try regular password"""

print("="*60)
print("📧 Quick IMAP Test")
print("="*60)
print()
print("Let's try connecting with your regular email password.")
print("(Some work accounts allow this, others don't)")
print()
print("If this doesn't work, we'll try OAuth instead.")
print()

# Check current config
import json
from pathlib import Path

config_path = Path.home() / '.email_assistant_config.json'
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
    print(f"Email: {config.get('email', 'kbaker@onwasa.com')}")
    print(f"IMAP Server: {config.get('imap_server', 'outlook.office365.com')}")
    
    if config.get('imap_password'):
        print("\n✅ Password already saved!")
        print("Run: python3 email_imap.py")
    else:
        print("\n⚠️  No password configured yet.")
        print("\nOptions:")
        print("1. Run setup: python3 setup_imap.py")
        print("2. Or I can create a simpler version")
