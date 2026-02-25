#!/usr/bin/env python3
"""
Setup script for Email Assistant
"""

import json
from pathlib import Path


def setup():
    """Initial setup"""
    config_dir = Path.home() / '.email_assistant'
    config_dir.mkdir(exist_ok=True)
    
    # Create default config
    config = {
        'email': 'kbaker@onwasa.com',
        'check_interval_seconds': 30,
        'require_approval': True,
        'spam_detection': True,
        'auto_unsubscribe': False,
        'mail_app': 'outlook',
        'whitelist_domains': ['onwasa.com', 'microsoft.com', 'apple.com', 'google.com'],
        'blocked_senders': [],
        'unsubscribed': []
    }
    
    config_file = Path.home() / '.email_assistant_config.json'
    if not config_file.exists():
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Created config: {config_file}")
    
    # Create directories
    (config_dir / 'skills').mkdir(exist_ok=True)
    (config_dir / 'workspace').mkdir(exist_ok=True)
    (config_dir / 'pending').mkdir(exist_ok=True)
    
    print("✅ Email Assistant setup complete!")
    print(f"Config: {config_file}")
    print("\nNext steps:")
    print("1. Edit the config file if needed")
    print("2. Run: python email_assistant.py")


if __name__ == '__main__':
    setup()
