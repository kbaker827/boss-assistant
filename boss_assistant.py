#!/usr/bin/env python3
"""
Boss Assistant - AI Assistant for handling boss emails

Monitors emails from boss, completes tasks, learns new skills,
and presents work for approval.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path


class BossAssistant:
    """Main Boss Assistant class"""
    
    def __init__(self):
        self.config = self.load_config()
        self.is_running = False
        self.learned_skills_dir = Path.home() / '.boss_assistant' / 'skills'
        self.learned_skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.root = tk.Tk()
        self.root.title("Boss Assistant 🤖")
        self.root.geometry("900x700")
        
        self.setup_ui()
        
    def load_config(self):
        """Load configuration"""
        config_path = Path.home() / '.boss_assistant_config.json'
        default_config = {
            'boss_email': 'dbergman@onwasa.com',
            'check_interval_minutes': 5,
            'require_approval': True,
            'auto_reply': False
        }
        
        if config_path.exists():
            with open(config_path) as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def setup_ui(self):
        """Setup the user interface"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header,
            text="🤖 Boss Assistant",
            font=('Segoe UI', 18, 'bold')
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            header,
            text=f"Monitoring: {self.config['boss_email']}",
            font=('Segoe UI', 10)
        ).pack(side=tk.RIGHT)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Ready to start")
        ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor=tk.W)
        
        # Control buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_btn = tk.Button(
            btn_frame,
            text="▶️ Start Monitoring",
            command=self.start_monitoring,
            bg='#28a745',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=10
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹️ Stop",
            command=self.stop_monitoring,
            bg='#dc3545',
            fg='white',
            font=('Segoe UI', 11),
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="📚 View Learned Skills",
            command=self.view_skills,
            bg='#007bff',
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Pending approvals
        self.pending_frame = ttk.LabelFrame(main_frame, text="Pending Approvals", padding="10")
        self.pending_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.pending_list = tk.Listbox(
            self.pending_frame,
            font=('Segoe UI', 10),
            height=5
        )
        self.pending_list.pack(fill=tk.BOTH, expand=True)
        self.pending_list.bind('<Double-Button-1>', self.view_pending_task)
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log("Boss Assistant initialized.")
        self.log(f"Configured to monitor: {self.config['boss_email']}")
        self.log("Click 'Start Monitoring' to begin.")
    
    def log(self, message):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def start_monitoring(self):
        """Start email monitoring"""
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("🔍 Monitoring for boss emails...")
        self.log("Started monitoring for boss emails")
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop email monitoring"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("⏹️ Stopped")
        self.log("Stopped monitoring")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                self.check_emails()
                # Sleep for check interval
                for _ in range(self.config['check_interval_minutes'] * 60):
                    if not self.is_running:
                        break
                    time.sleep(1)
            except Exception as e:
                self.log(f"Error in monitor loop: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def check_emails(self):
        """Check for new emails from boss"""
        # This would connect to your email system
        # For now, simulating with example
        self.log("Checking for new emails...")
        
        # Example: In real implementation, this would:
        # 1. Connect to Exchange/Outlook/IMAP
        # 2. Search for unread emails from boss_email
        # 3. For each new email, call process_email()
        
        pass  # Placeholder for email checking logic
    
    def process_email(self, email_data):
        """Process an email from boss"""
        self.log(f"📧 New email from boss: {email_data['subject']}")
        
        # Parse the request
        task = self.parse_task(email_data['body'])
        
        # Check if we have a skill for this
        skill = self.find_skill(task['type'])
        
        if skill:
            self.log(f"🤖 Found existing skill: {skill['name']}")
            result = self.execute_skill(skill, task)
        else:
            self.log(f"📚 No skill found. Learning how to: {task['type']}")
            skill = self.learn_skill(task)
            result = self.execute_skill(skill, task)
        
        # Present for approval
        self.present_for_approval(email_data, task, result)
    
    def parse_task(self, email_body):
        """Parse what task needs to be done"""
        # Use AI/OpenClaw to understand the request
        # This is a simplified version
        
        task_types = {
            r'report|spreadsheet|excel': 'generate_report',
            r'email|send|message': 'send_email',
            r'schedule|meeting|calendar': 'schedule_meeting',
            r'research|find|lookup': 'research',
            r'file|document|draft': 'create_document',
            r'analyze|data|numbers': 'analyze_data'
        }
        
        email_lower = email_body.lower()
        task_type = 'general_task'  # default
        
        for pattern, ttype in task_types.items():
            if re.search(pattern, email_lower):
                task_type = ttype
                break
        
        return {
            'type': task_type,
            'description': email_body,
            'extracted_request': self.extract_request(email_body)
        }
    
    def extract_request(self, email_body):
        """Extract the specific request from email"""
        # Simplified extraction
        lines = email_body.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:
                return line
        return email_body[:200]
    
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
            'steps': self.generate_steps(task),
            'examples': [task['description']]
        }
        
        # Save skill
        skill_file = self.learned_skills_dir / f"{task['type']}.json"
        with open(skill_file, 'w') as f:
            json.dump(skill, f, indent=2)
        
        self.log(f"📚 Created new skill: {skill['name']}")
        return skill
    
    def generate_steps(self, task):
        """Generate steps to complete the task"""
        # This would use AI to generate appropriate steps
        # For now, returning generic steps
        return [
            f"Understand request: {task['extracted_request']}",
            "Gather necessary information",
            "Complete the task",
            "Prepare response/output",
            "Present for approval"
        ]
    
    def execute_skill(self, skill, task):
        """Execute a skill to complete the task"""
        self.log(f"🤖 Executing skill: {skill['name']}")
        
        # In real implementation, this would:
        # 1. Follow the skill steps
        # 2. Use OpenClaw/tools to complete the work
        # 3. Generate the output
        
        return {
            'success': True,
            'output': f"Completed: {task['extracted_request']}",
            'files': [],
            'details': f"Executed {len(skill['steps'])} steps from skill"
        }
    
    def present_for_approval(self, email_data, task, result):
        """Present completed work for user approval"""
        # Add to pending list
        pending_id = f"{datetime.now().strftime('%H%M%S')}_{task['type']}"
        self.pending_list.insert(tk.END, f"📧 {email_data['subject']} - {task['type']}")
        
        # Show approval dialog
        ApprovalDialog(self.root, email_data, task, result, self.on_approval_decision)
        
        self.log("⏳ Waiting for your approval...")
    
    def on_approval_decision(self, decision, feedback=None):
        """Handle approval decision"""
        if decision == 'approve':
            self.log("✅ Approved! Sending response...")
            # Send the response/output
        elif decision == 'edit':
            self.log("✏️ Edit requested. Opening editor...")
            # Open editor
        elif decision == 'reject':
            self.log("❌ Rejected. Discarding work...")
        elif decision == 'defer':
            self.log("⏳ Deferred. Will review later...")
    
    def view_pending_task(self, event):
        """View a pending task"""
        selection = self.pending_list.curselection()
        if selection:
            task = self.pending_list.get(selection[0])
            messagebox.showinfo("Pending Task", f"Review: {task}")
    
    def view_skills(self):
        """View learned skills"""
        skills_window = tk.Toplevel(self.root)
        skills_window.title("Learned Skills 📚")
        skills_window.geometry("600x400")
        
        ttk.Label(
            skills_window,
            text="Skills I've Learned",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        skills_list = tk.Listbox(skills_window, font=('Segoe UI', 10))
        skills_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Load skills
        for skill_file in self.learned_skills_dir.glob('*.json'):
            with open(skill_file) as f:
                skill = json.load(f)
                skills_list.insert(tk.END, f"📚 {skill['name']} - {skill['description']}")


class ApprovalDialog:
    """Dialog for approving work"""
    
    def __init__(self, parent, email_data, task, result, callback):
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🤖 Boss Assistant - Approve Work")
        self.dialog.geometry("700x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Email info
        ttk.Label(
            self.dialog,
            text=f"📧 From: {email_data.get('from', 'Boss')}",
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Label(
            self.dialog,
            text=f"Subject: {email_data.get('subject', 'No Subject')}",
            font=('Segoe UI', 10)
        ).pack(anchor=tk.W, padx=10)
        
        ttk.Separator(self.dialog, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)
        
        # Task info
        ttk.Label(
            self.dialog,
            text=f"🎯 Task: {task['type']}",
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Label(
            self.dialog,
            text=f"Request: {task['extracted_request']}",
            font=('Segoe UI', 10),
            wraplength=650
        ).pack(anchor=tk.W, padx=10)
        
        # Result
        result_frame = ttk.LabelFrame(self.dialog, text="🤖 What I Did", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            height=10
        )
        result_text.pack(fill=tk.BOTH, expand=True)
        result_text.insert(tk.END, result['output'])
        result_text.config(state=tk.DISABLED)
        
        # Feedback
        ttk.Label(self.dialog, text="💬 Your Feedback (optional):").pack(anchor=tk.W, padx=10, pady=(10,0))
        self.feedback_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.feedback_var, width=80).pack(padx=10, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="✅ Approve & Send",
            command=self.approve,
            bg='#28a745',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="✏️ Edit First",
            command=self.edit,
            bg='#007bff',
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="⏳ Defer",
            command=self.defer,
            bg='#6c757d',
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Reject",
            command=self.reject,
            bg='#dc3545',
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
    
    def approve(self):
        self.callback('approve', self.feedback_var.get())
        self.dialog.destroy()
    
    def edit(self):
        self.callback('edit', self.feedback_var.get())
        self.dialog.destroy()
    
    def defer(self):
        self.callback('defer', self.feedback_var.get())
        self.dialog.destroy()
    
    def reject(self):
        self.callback('reject', self.feedback_var.get())
        self.dialog.destroy()


def main():
    app = BossAssistant()
    app.run()


if __name__ == '__main__':
    main()
