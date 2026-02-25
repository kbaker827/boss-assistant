#!/usr/bin/env python3
"""
Setup script for Email Assistant
Guides user through configuration and permissions
"""

import json
import subprocess
from pathlib import Path


def check_outlook_access():
    """Check if we can access Outlook via AppleScript"""
    try:
        script = '''
        tell application "Microsoft Outlook"
            return name
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False


def setup():
    """Initial setup"""
    print("="*60)
    print("📧 Email Assistant Setup")
    print("="*60)
    print()
    
    config_dir = Path.home() / '.email_assistant'
    config_dir.mkdir(exist_ok=True)
    
    # Check Outlook
    print("Checking Microsoft Outlook access...")
    if check_outlook_access():
        print("✅ Outlook is accessible")
    else:
        print("⚠️  Could not access Outlook")
        print("   Make sure Microsoft Outlook is installed and running")
        print("   You may need to grant permissions when prompted")
    
    print()
    
    # Create default config
    config = {
        'email': 'kbaker@onwasa.com',
        'check_interval_seconds': 30,
        'require_approval': True,
        'spam_detection': True,
        'auto_unsubscribe': False,
        'mail_app': 'outlook',
        'whitelist_domains': [
            'onwasa.com',
            'microsoft.com', 
            'apple.com',
            'google.com',
            'zoom.us',
            'teams.microsoft.com'
        ],
        'blocked_senders': [],
        'unsubscribed': []
    }
    
    config_file = Path.home() / '.email_assistant_config.json'
    
    if config_file.exists():
        print(f"Config already exists: {config_file}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing config")
            return
    
    # Get user email
    email = input(f"Enter your work email [default: {config['email']}]: ").strip()
    if email:
        config['email'] = email
    
    # Get check interval
    interval = input(f"Check interval in seconds [default: {config['check_interval_seconds']}]: ").strip()
    if interval.isdigit():
        config['check_interval_seconds'] = int(interval)
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Config saved: {config_file}")
    
    # Create directories
    (config_dir / 'skills').mkdir(exist_ok=True)
    (config_dir / 'workspace').mkdir(exist_ok=True)
    (config_dir / 'pending').mkdir(exist_ok=True)
    
    print("✅ Directories created")
    
    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Make sure Microsoft Outlook is running")
    print("2. Grant permissions when prompted (click 'OK')")
    print("3. Run: python email_assistant.py")
    print()
    print("⚠️  IMPORTANT:")
    print("   The first time you run the assistant,")
    print("   macOS will ask for permission to control Outlook.")
    print("   Click 'OK' to allow this.")
    print()
    print("   If you accidentally click 'Don't Allow':")
    print("   1. Go to System Preferences > Security & Privacy > Privacy")
    print("   2. Click 'Automation'")
    print("   3. Check the box for Terminal/Python to control Outlook")
    print()


if __name__ == '__main__':
    setup()
