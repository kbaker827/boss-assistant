#!/usr/bin/env python3
"""
IMAP Email Checker for kbaker@onwasa.com
"""

import imaplib
import email
from email.header import decode_header
import json
from pathlib import Path


def get_config():
    """Load configuration"""
    config_path = Path.home() / '.email_assistant_config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def connect_imap():
    """Connect to IMAP server"""
    config = get_config()
    
    # For Office 365/Exchange
    imap_server = config.get('imap_server', 'outlook.office365.com')
    imap_port = config.get('imap_port', 993)
    email_addr = config.get('email', 'kbaker@onwasa.com')
    password = config.get('imap_password', '')
    
    if not password:
        print("⚠️  IMAP password not configured!")
        print("Please add it to ~/.email_assistant_config.json")
        print("Or run: python3 setup_imap.py")
        return None
    
    try:
        # Connect to server
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(email_addr, password)
        print(f"✅ Connected to {imap_server}")
        return mail
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None


def check_unread():
    """Check for unread emails"""
    mail = connect_imap()
    if not mail:
        return []
    
    emails = []
    
    try:
        # Select inbox
        status, messages = mail.select('INBOX')
        
        if status != 'OK':
            print("Could not access inbox")
            return []
        
        # Search for unread emails
        status, data = mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            print("No unread emails")
            return []
        
        # Get email IDs
        email_ids = data[0].split()
        
        print(f"📧 Found {len(email_ids)} unread email(s)")
        
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, '(RFC822)')
            
            if status != 'OK':
                continue
            
            # Parse email
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Get subject
            subject = decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            # Get sender
            from_addr = msg.get('From', '')
            
            # Get body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    pass
            
            email_data = {
                'id': e_id.decode(),
                'from': from_addr,
                'subject': subject,
                'body': body[:500]  # First 500 chars
            }
            
            emails.append(email_data)
            
            print(f"\n  From: {from_addr}")
            print(f"  Subject: {subject}")
            print(f"  Preview: {body[:100]}...")
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"Error: {e}")
    
    return emails


if __name__ == '__main__':
    print("="*60)
    print("📧 IMAP Email Checker")
    print("="*60)
    print()
    
    emails = check_unread()
    
    if emails:
        print(f"\n✅ Total unread: {len(emails)}")
    else:
        print("\n📭 No unread emails")
