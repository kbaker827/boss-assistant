#!/usr/bin/env python3
"""
Setup Helper - Choose your authentication method
"""

print("="*60)
print("📧 Email Assistant - Setup Helper")
print("="*60)
print()
print("Choose authentication method:")
print()
print("1. PASSWORD (Quick)")
print("   - Try your regular email password")
print("   - Fastest option")
print("   - Run: python3 quick_setup.py")
print()
print("2. OAUTH (Secure)")
print("   - Browser sign-in (no password stored)")
print("   - Most secure")
print("   - Requires Azure app registration")
print("   - Run: python3 setup_oauth.py")
print()
print("3. TEST CURRENT SETUP")
print("   - Test whatever is currently configured")
print("   - Run: python3 email_imap.py")
print()

choice = input("Enter 1, 2, or 3: ").strip()

if choice == "1":
    import subprocess
    subprocess.run(['python3', 'quick_setup.py'])
elif choice == "2":
    import subprocess
    subprocess.run(['python3', 'setup_oauth.py'])
elif choice == "3":
    import subprocess
    subprocess.run(['python3', 'email_imap.py'])
else:
    print("Invalid choice. Run this again and enter 1, 2, or 3.")
