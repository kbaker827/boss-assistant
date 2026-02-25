#!/usr/bin/env python3
"""
Setup script for Boss Assistant
"""

import json
from pathlib import Path


def setup():
    """Initial setup"""
    config_dir = Path.home() / '.boss_assistant'
    config_dir.mkdir(exist_ok=True)
    
    # Create default config
    config = {
        'boss_email': 'dbergman@onwasa.com',
        'check_interval_minutes': 5,
        'require_approval': True,
        'auto_reply': False,
        'email_provider': 'outlook',  # or gmail, imap, etc
        'notification_sound': True
    }
    
    config_file = Path.home() / '.boss_assistant_config.json'
    if not config_file.exists():
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Created config: {config_file}")
    
    # Create directories
    (config_dir / 'skills').mkdir(exist_ok=True)
    (config_dir / 'workspace').mkdir(exist_ok=True)
    (config_dir / 'pending').mkdir(exist_ok=True)
    
    print("✅ Boss Assistant setup complete!")
    print(f"Config location: {config_file}")
    print("\nNext steps:")
    print("1. Edit the config file to add your email credentials")
    print("2. Run: python boss_assistant.py")


if __name__ == '__main__':
    setup()
