#!/usr/bin/env python3
"""Quick password setup - just enter and test"""

import getpass
import json
from pathlib import Path
import imaplib

print("="*60)
print("📧 Quick Email Setup")
print("="*60)
print()
print("Enter your email password to test IMAP connection:")
print("(If it fails, we'll try OAuth instead)")
print()

password = getpass.getpass("Password: ")

if not password:
    print("❌ No password entered")
    exit()

print("\n🔄 Testing connection...")

try:
    # Try to connect
    mail = imaplib.IMAP4_SSL('outlook.office365.com', 993)
    mail.login('youremail@example.com', password)
    
    # Try to access inbox
    mail.select('INBOX')
    status, data = mail.search(None, 'UNSEEN')
    unread_count = len(data[0].split())
    
    mail.close()
    mail.logout()
    
    print(f"✅ SUCCESS! Connected and found {unread_count} unread emails")
    print()
    
    # Save password
    config_path = Path.home() / '.email_assistant_config.json'
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {}
    
    config['email'] = 'youremail@example.com'
    config['imap_server'] = 'outlook.office365.com'
    config['imap_port'] = 993
    config['imap_password'] = password
    config['use_imap'] = True
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Password saved!")
    print()
    print("You can now run: python3 email_imap.py")
    print("Or double-click the EmailAssistant desktop shortcut!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print()
    print("This usually means:")
    print("- Your organization requires MFA/App Passwords")
    print("- IMAP is disabled for your account")
    print()
    print("Let's try OAuth instead (opens browser to sign in)")
    print("Want me to set that up?")
