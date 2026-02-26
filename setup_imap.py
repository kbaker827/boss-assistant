#!/usr/bin/env python3
"""
Setup IMAP connection for Email Assistant
"""

import json
from pathlib import Path
import getpass


def setup():
    print("="*60)
    print("📧 IMAP Email Setup")
    print("="*60)
    print()
    print("This will configure IMAP access to your email.")
    print()
    
    # Load existing config
    config_path = Path.home() / '.email_assistant_config.json'
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {}
    
    # Get email
    email = input(f"Email address [default: {config.get('email', 'kbaker@onwasa.com')}]: ").strip()
    if email:
        config['email'] = email
    elif 'email' not in config:
        config['email'] = 'kbaker@onwasa.com'
    
    print()
    print("For Office 365/Exchange (kbaker@onwasa.com):")
    print("  IMAP Server: outlook.office365.com")
    print("  Port: 993")
    print()
    
    # IMAP settings
    imap_server = input("IMAP server [outlook.office365.com]: ").strip()
    config['imap_server'] = imap_server if imap_server else 'outlook.office365.com'
    
    imap_port = input("IMAP port [993]: ").strip()
    config['imap_port'] = int(imap_port) if imap_port.isdigit() else 993
    
    print()
    print("⚠️  IMPORTANT: Use an App Password, not your regular password!")
    print()
    print("To create an App Password for Office 365:")
    print("1. Go to https://account.microsoft.com/security")
    print("2. Click 'Advanced security options'")
    print("3. Click 'Create a new app password'")
    print("4. Use that password here")
    print()
    
    # Get password securely
    password = getpass.getpass("App Password: ")
    
    if password:
        config['imap_password'] = password
        config['use_imap'] = True
        
        # Save config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print()
        print("✅ Configuration saved!")
        print()
        print("Testing connection...")
        print()
        
        # Test the connection
        import subprocess
        result = subprocess.run(
            ['python3', 'email_imap.py'],
            capture_output=True,
            text=True,
            cwd=Path.home() / '.openclaw/workspace/skills/boss-assistant'
        )
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    else:
        print("❌ No password entered. Setup cancelled.")


if __name__ == '__main__':
    setup()
