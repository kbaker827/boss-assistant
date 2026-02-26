#!/usr/bin/env python3
"""
OAuth Setup for Email Assistant
Uses Microsoft Modern Authentication
"""

import json
import subprocess
import sys
from pathlib import Path


def check_msal():
    """Check if MSAL is installed"""
    try:
        import msal
        return True
    except ImportError:
        return False


def install_msal():
    """Install MSAL library"""
    print("Installing Microsoft Authentication Library...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'msal'], 
                      check=True, capture_output=True)
        print("✅ MSAL installed")
        return True
    except:
        print("❌ Failed to install MSAL")
        print("Try running: pip3 install msal")
        return False


def setup_oauth():
    """Set up OAuth authentication"""
    print("="*60)
    print("📧 OAuth Setup for Email Assistant")
    print("="*60)
    print()
    
    # Check MSAL
    if not check_msal():
        print("MSAL library not found.")
        response = input("Install it now? (y/n): ").strip().lower()
        if response == 'y':
            if not install_msal():
                return
        else:
            print("Please install MSAL: pip3 install msal")
            return
    
    print()
    print("This will open a browser for you to sign in with Microsoft.")
    print("Your password is NEVER stored - it's handled securely by Microsoft.")
    print()
    
    # Create the OAuth flow script
    oauth_script = Path.home() / '.email_assistant' / 'oauth_flow.py'
    
    oauth_code = '''
import msal
import json
import webbrowser
from pathlib import Path

# Microsoft Graph API settings
CLIENT_ID = "your-client-id-here"  # Would need to register app
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPE = ["Mail.Read", "Mail.ReadWrite"]

cache = msal.SerializableTokenCache()

token_path = Path.home() / '.email_assistant' / 'oauth_token.json'
if token_path.exists():
    cache.deserialize(token_path.read_text())

app = msal.PublicClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    token_cache=cache
)

# Try to get token silently first
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(SCOPE, account=accounts[0])
    if result:
        print("✅ Already signed in!")
        token_path.write_text(cache.serialize())
        exit(0)

# Otherwise, do interactive login
flow = app.initiate_device_flow(scopes=SCOPE)
if "user_code" not in flow:
    raise ValueError("Failed to create device flow")

print("="*60)
print("📧 Sign in to Microsoft")
print("="*60)
print()
print(flow['message'])
print()
print("Or visit:", flow['verification_uri'])
print("Code:", flow['user_code'])
print()

webbrowser.open(flow['verification_uri'])

result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
    token_path.write_text(cache.serialize())
    print("✅ Sign-in successful!")
else:
    print("❌ Sign-in failed:", result.get('error_description'))
'''
    
    oauth_script.parent.mkdir(parents=True, exist_ok=True)
    oauth_script.write_text(oauth_code)
    
    print("⚠️  NOTE: Full OAuth requires registering an Azure AD app.")
    print()
    print("For now, I recommend:")
    print("1. Try your regular password first (python3 quick_setup.py)")
    print("2. If that fails, we can set up Azure app registration")
    print()
    print("Azure app registration steps:")
    print("1. Go to https://portal.azure.com")
    print("2. Azure Active Directory → App registrations")
    print("3. New registration")
    print("4. Name: Email Assistant")
    print("5. Supported account types: Accounts in any org directory")
    print("6. Redirect URI: Public client/native")
    print("7. Copy the Application (client) ID")
    print("8. API permissions → Add → Microsoft Graph → Mail.Read")
    print()


if __name__ == '__main__':
    setup_oauth()
