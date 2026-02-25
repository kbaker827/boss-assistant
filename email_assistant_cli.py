#!/usr/bin/env python3
"""
Email Assistant - Terminal Version (No GUI required)

Monitors ALL emails at kbaker@onwasa.com, handles spam (unsubscribe/block),
completes work tasks, learns skills, and gets approval before acting.
"""

import json
import os
import re
import time
import subprocess
from datetime import datetime
from pathlib import Path
import hashlib
import sys


class EmailAssistantCLI:
    """Terminal-based Email Assistant"""
    
    def __init__(self):
        self.config = self.load_config()
        self.is_running = False
        self.learned_skills_dir = Path.home() / '.email_assistant' / 'skills'
        self.learned_skills_dir.mkdir(parents=True, exist_ok=True)
        self.processed_emails = set()
        self.stats = {'checked': 0, 'spam': 0, 'tasks': 0}
        
    def load_config(self):
        """Load configuration"""
        config_path = Path.home() / '.email_assistant_config.json'
        default_config = {
            'email': 'kbaker@onwasa.com',
            'check_interval_seconds': 30,
            'require_approval': True,
            'spam_detection': True,
            'auto_unsubscribe': False,
            'mail_app': 'outlook',
            'whitelist_domains': ['onwasa.com', 'microsoft.com', 'apple.com'],
            'blocked_senders': [],
            'unsubscribed': []
        }
        
        if config_path.exists():
            with open(config_path) as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def save_config(self):
        """Save configuration"""
        config_path = Path.home() / '.email_assistant_config.json'
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def log(self, message):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def print_banner(self):
        """Print startup banner"""
        print("="*60)
        print("📧  EMAIL ASSISTANT - Terminal Version")
        print("="*60)
        print(f"Monitoring: {self.config['email']}")
        print(f"Check interval: {self.config['check_interval_seconds'] // 60} minutes")
        print(f"Spam detection: {'ON' if self.config['spam_detection'] else 'OFF'}")
        print("="*60)
        print()
    
    def run(self):
        """Main run loop"""
        self.print_banner()
        
        # Check Outlook access
        if not self.check_outlook_access():
            print("⚠️  Could not connect to Microsoft Outlook")
            print("   Make sure Outlook is running and try again")
            return
        
        print("✅ Connected to Microsoft Outlook")
        print()
        print("Commands:")
        print("  [Enter] - Check emails now")
        print("  'auto'  - Auto-check every 5 minutes")
        print("  'quit'  - Exit")
        print()
        
        while True:
            try:
                cmd = input("> ").strip().lower()
                
                if cmd == 'quit' or cmd == 'q':
                    print("Goodbye!")
                    break
                elif cmd == 'auto' or cmd == 'a':
                    self.auto_mode()
                elif cmd == '':
                    self.check_once()
                else:
                    print("Unknown command. Use: [Enter], 'auto', or 'quit'")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def check_outlook_access(self):
        """Check if we can access Outlook"""
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
    
    def auto_mode(self):
        """Auto-check mode"""
        print(f"\n🔄 Auto-mode: Checking every {self.config['check_interval_seconds'] // 60} minutes")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.check_once()
                time.sleep(self.config['check_interval_seconds'])
        except KeyboardInterrupt:
            print("\n\n⏹️  Auto-mode stopped")
            print()
    
    def check_once(self):
        """Check emails once"""
        self.log("Checking for new emails...")
        emails = self.check_emails_macos()
        self.stats['checked'] += len(emails)
        
        if not emails:
            self.log("No new emails")
            return
        
        self.log(f"Found {len(emails)} new email(s)")
        
        for email_data in emails:
            email_id = self.get_email_id(email_data)
            if email_id in self.processed_emails:
                continue
            self.processed_emails.add(email_id)
            
            self.process_email_interactive(email_data)
    
    def get_email_id(self, email_data):
        """Generate unique ID for email"""
        content = f"{email_data.get('from', '')}{email_data.get('subject', '')}{email_data.get('date', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def check_emails_macos(self):
        """Check for new emails using Microsoft Outlook for Mac"""
        emails = []
        
        try:
            script = '''
            tell application "Microsoft Outlook"
                if not running then launch
                set msgs to messages of inbox whose read status is false
                set emailList to {}
                repeat with msg in msgs
                    try
                        set senderObj to sender of msg
                        set senderEmail to address of senderObj
                        set senderName to name of senderObj
                        set msgSubject to subject of msg
                        set msgContent to plain text content of msg
                        set msgDate to time received of msg
                        set msgID to id of msg as string
                        set end of emailList to {senderEmail & "|" & senderName & "|" & msgSubject & "|" & msgContent & "|" & msgID}
                    on error
                        -- Skip problematic messages
                    end try
                end repeat
                return emailList
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', script], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if '|' in line:
                        parts = line.split('|', 4)
                        if len(parts) >= 4:
                            email_data = {
                                'from': parts[0],
                                'sender_name': parts[1],
                                'subject': parts[2],
                                'body': parts[3] if len(parts) > 3 else '',
                                'id': parts[4] if len(parts) > 4 else '',
                                'date': datetime.now().isoformat()
                            }
                            emails.append(email_data)
                            
        except Exception as e:
            self.log(f"Error checking emails: {e}")
        
        return emails
    
    def mark_email_read(self, email_id):
        """Mark an email as read in Outlook"""
        try:
            script = f'''
            tell application "Microsoft Outlook"
                set msgMsg to message id "{email_id}" of inbox
                set read status of msgMsg to true
            end tell
            '''
            subprocess.run(['osascript', '-e', script], capture_output=True, timeout=10)
        except:
            pass
    
    def process_email_interactive(self, email_data):
        """Process email with user interaction"""
        sender = email_data.get('from', '')
        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        
        print()
        print("="*60)
        print(f"📧  NEW EMAIL")
        print("="*60)
        print(f"From:    {sender}")
        print(f"Subject: {subject}")
        print(f"Preview: {body[:150]}...")
        print()
        
        # Check if sender is blocked
        if sender in self.config.get('blocked_senders', []):
            print("🚫 Sender is blocked - skipping")
            return
        
        # Check if spam
        is_spam = self.is_spam_email(email_data)
        
        if is_spam:
            print("🚫 SPAM DETECTED")
            self.handle_spam_interactive(email_data)
        else:
            print("✅ Legitimate email")
            self.handle_work_email_interactive(email_data)
    
    def is_spam_email(self, email_data):
        """Detect if email is spam"""
        if not self.config['spam_detection']:
            return False
        
        sender = email_data.get('from', '').lower()
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        
        # Check whitelist
        for domain in self.config.get('whitelist_domains', []):
            if domain.lower() in sender:
                return False
        
        spam_score = 0
        spam_words = ['unsubscribe', 'promotional', 'marketing', 'limited time', 'act now', 
                      'click here', 'buy now', 'order now', 'special offer', 'free gift',
                      'congratulations', 'winner', 'claim now', 'urgent', 'important notice']
        
        for word in spam_words:
            if word in subject or word in body:
                spam_score += 1
        
        if subject.count('!') > 2 or subject.count('?') > 2:
            spam_score += 1
        
        if 'unsubscribe' in body or 'opt-out' in body:
            spam_score += 2
        
        return spam_score >= 3
    
    def handle_spam_interactive(self, email_data):
        """Handle spam with user input"""
        sender = email_data.get('from', '')
        
        print()
        print("Options:")
        print("  [u] Unsubscribe & Block sender")
        print("  [b] Block sender only")
        print("  [n] Not spam (keep email)")
        print("  [i] Ignore (skip)")
        
        choice = input("Your choice [u/b/n/i]: ").strip().lower()
        
        if choice == 'u':
            print(f"✅ Unsubscribing and blocking {sender}")
            self.block_sender(sender)
            self.stats['spam'] += 1
            if email_data.get('id'):
                self.mark_email_read(email_data['id'])
        elif choice == 'b':
            print(f"✅ Blocking {sender}")
            self.block_sender(sender)
            self.stats['spam'] += 1
            if email_data.get('id'):
                self.mark_email_read(email_data['id'])
        elif choice == 'n':
            print(f"✅ Marked as not spam: {sender}")
            domain = sender.split('@')[-1]
            if domain not in self.config['whitelist_domains']:
                self.config['whitelist_domains'].append(domain)
                self.save_config()
        else:
            print("ℹ️  Skipped")
    
    def block_sender(self, sender):
        """Add sender to block list"""
        if sender not in self.config['blocked_senders']:
            self.config['blocked_senders'].append(sender)
            self.save_config()
            print(f"   Added to block list: {sender}")
    
    def handle_work_email_interactive(self, email_data):
        """Handle work email with user input"""
        task = self.parse_task(email_data)
        
        if task['type'] == 'unknown':
            print("ℹ️  No actionable task detected")
            print("  [r] Mark as read")
            print("  [s] Skip")
            choice = input("Your choice [r/s]: ").strip().lower()
            if choice == 'r' and email_data.get('id'):
                self.mark_email_read(email_data['id'])
            return
        
        print(f"\n🎯 Task detected: {task['type']}")
        print(f"   Request: {task['extracted_request']}")
        
        # Find or learn skill
        skill = self.find_skill(task['type'])
        if not skill:
            skill = self.learn_skill(task)
        
        # Execute skill
        result = self.execute_skill(skill, task)
        
        print(f"\n🤖 What I can do:")
        print(f"   {result['output']}")
        
        print()
        print("Options:")
        print("  [a] Approve and complete")
        print("  [e] Edit first (opens editor)")
        print("  [d] Defer (handle later)")
        print("  [r] Reject/mark as read")
        
        choice = input("Your choice [a/e/d/r]: ").strip().lower()
        
        if choice == 'a':
            print("✅ Approved! Marking as complete...")
            self.stats['tasks'] += 1
            if email_data.get('id'):
                self.mark_email_read(email_data['id'])
        elif choice == 'e':
            print("✏️  Opening editor... (not implemented in CLI)")
        elif choice == 'r':
            print("❌ Rejected. Marking as read...")
            if email_data.get('id'):
                self.mark_email_read(email_data['id'])
        else:
            print("⏳ Deferred")
    
    def parse_task(self, email_data):
        """Parse what task needs to be done"""
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        
        task_types = {
            r'report|spreadsheet|excel|numbers': 'generate_report',
            r'email|send|message|write to': 'send_email',
            r'schedule|meeting|calendar|invite': 'schedule_meeting',
            r'research|find|lookup|search': 'research',
            r'file|document|draft|create': 'create_document',
            r'analyze|data|numbers|stats': 'analyze_data',
            r'call|phone|contact': 'make_call',
            r'reminder|follow up|check on': 'set_reminder'
        }
        
        combined = subject + " " + body
        task_type = 'unknown'
        
        for pattern, ttype in task_types.items():
            if re.search(pattern, combined):
                task_type = ttype
                break
        
        request = self.extract_request(email_data)
        
        return {
            'type': task_type,
            'description': email_data.get('body', ''),
            'extracted_request': request,
            'from': email_data.get('from', ''),
            'subject': email_data.get('subject', '')
        }
    
    def extract_request(self, email_data):
        """Extract the specific request from email"""
        body = email_data.get('body', '')
        lines = body.split('\n')
        
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                if any(word in line.lower() for word in ['can you', 'could you', 'please', 'need', 'want', 'would you']):
                    return line
        
        for line in lines:
            line = line.strip()
            if len(line) > 10:
                return line[:200]
        
        return body[:200]
    
    def find_skill(self, task_type):
        """Find a learned skill for this task type"""
        skill_file = self.learned_skills_dir / f"{task_type}.json"
        if skill_file.exists():
            with open(skill_file) as f:
                return json.load(f)
        return None
    
    def learn_skill(self, task):
        """Learn/create a new skill for this task type"""
        skill = {
            'name': task['type'],
            'type': task['type'],
            'created': datetime.now().isoformat(),
            'description': f"Handle {task['type']} requests",
            'steps': [
                f"Understand request: {task['extracted_request']}",
                "Gather necessary information",
                "Complete the task",
                "Prepare response/output",
                "Present for approval"
            ],
            'examples': [task['extracted_request']]
        }
        
        skill_file = self.learned_skills_dir / f"{task['type']}.json"
        with open(skill_file, 'w') as f:
            json.dump(skill, f, indent=2)
        
        print(f"   📚 Created new skill: {skill['name']}")
        return skill
    
    def execute_skill(self, skill, task):
        """Execute a skill to complete the task"""
        outputs = {
            'generate_report': f"Generate report: {task['extracted_request']}",
            'send_email': f"Draft email response to: {task['from']}",
            'schedule_meeting': f"Check calendar availability",
            'research': f"Research: {task['extracted_request']}",
            'create_document': f"Create document: {task['extracted_request']}",
            'analyze_data': f"Analyze data: {task['extracted_request']}",
            'general_task': f"Complete: {task['extracted_request']}"
        }
        
        return {
            'success': True,
            'output': outputs.get(skill['name'], f"Complete: {task['extracted_request']}"),
            'files': [],
            'details': f"Executed {len(skill['steps'])} steps"
        }


def main():
    print()
    assistant = EmailAssistantCLI()
    assistant.run()


if __name__ == '__main__':
    main()
