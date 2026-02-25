#!/usr/bin/env python3
"""
Email Connector - Connects to various email systems
"""

import imaplib
import email
from email.header import decode_header
import json
from pathlib import Path


class EmailConnector:
    """Connect to email and check for boss emails"""
    
    def __init__(self, config):
        self.config = config
        self.last_check = None
        
    def connect_outlook_exchange(self):
        """Connect to Outlook/Exchange"""
        # Would use exchangelib or Microsoft Graph API
        pass
    
    def connect_imap(self, server, username, password):
        """Connect via IMAP"""
        try:
            mail = imaplib.IMAP4_SSL(server)
            mail.login(username, password)
            return mail
        except Exception as e:
            print(f"IMAP connection error: {e}")
            return None
    
    def check_for_emails(self, boss_email):
        """Check for new emails from boss"""
        new_emails = []
        
        # This is a placeholder - real implementation would:
        # 1. Connect to email server
        # 2. Search for unread emails from boss_email
        # 3. Return list of email data
        
        return new_emails
    
    def parse_email(self, raw_email):
        """Parse raw email into dict"""
        msg = email.message_from_bytes(raw_email)
        
        subject = self.decode_header(msg["Subject"])
        from_addr = self.decode_header(msg["From"])
        
        # Get body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        
        return {
            'subject': subject,
            'from': from_addr,
            'body': body,
            'date': msg["Date"]
        }
    
    def decode_header(self, header):
        """Decode email header"""
        if header is None:
            return ""
        decoded = decode_header(header)
        return decoded[0][0].decode(decoded[0][1]) if decoded[0][1] else decoded[0][0]
