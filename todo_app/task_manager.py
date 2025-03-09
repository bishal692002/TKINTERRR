# task_manager.py - Manages task data and persistence

import json
import os
import random
from datetime import datetime
from tkinter import messagebox

class TaskManager:
    def __init__(self, tasks_file):
        """Initialize the task manager with a file for persistence"""
        self.tasks_file = tasks_file
        self.tasks = []
        
        # Create the task data file if it doesn't exist
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, "w") as f:
                json.dump([], f)
    
    def load_tasks(self):
        """Load tasks from the JSON file"""
        try:
            with open(self.tasks_file, "r") as f:
                self.tasks = json.load(f)
                
                # Add IDs, default priority, description, and date_created to old tasks if they don't have them
                for task in self.tasks:
                    if "id" not in task:
                        task["id"] = str(random.randint(10000, 99999))
                    if "priority" not in task:
                        task["priority"] = "medium"
                    if "description" not in task:
                        task["description"] = "No description"
                    if "date_created" not in task:
                        task["date_created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            self.tasks = []
            return False
    
    def save_tasks(self):
        """Save tasks to the JSON file"""
        try:
            with open(self.tasks_file, "w") as f:
                json.dump(self.tasks, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
            return False
    
    def add_task(self, description, priority):
        """Add a new task to the task list"""
        if not description.strip():
            messagebox.showwarning("Warning", "Task description cannot be empty!")
            return False
        
        # Create new task
        new_task = {
            "description": description.strip(),
            "priority": priority,
            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed": False,
            "id": str(random.randint(10000, 99999))
        }
        
        # Add to task list
        self.tasks.append(new_task)
        self.save_tasks()
        return True
    
    def delete_task(self, task_id):
        """Delete a task by its ID"""
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
    
    def update_task(self, task_id, description=None, priority=None, completed=None):
        """Update a task's properties"""
        for task in self.tasks:
            if task["id"] == task_id:
                if description is not None:
                    task["description"] = description.strip()
                if priority is not None:
                    task["priority"] = priority
                if completed is not None:
                    task["completed"] = completed
                self.save_tasks()
                return True
        return False
    
    def toggle_task_status(self, task_id):
        """Toggle a task's completion status"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                self.save_tasks()
                return True
        return False
    
    def clear_completed_tasks(self):
        """Remove all completed tasks"""
        if not any(task["completed"] for task in self.tasks):
            messagebox.showinfo("Info", "No completed tasks to clear.")
            return False
        
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.save_tasks()
        return True
    
    def get_sorted_tasks(self):
        """Get tasks sorted by completion status and priority"""
        return sorted(self.tasks, 
                      key=lambda x: (x["completed"], {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "medium"), 1)))
    
    def get_statistics(self):
        """Get statistics about the current tasks"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        pending = total - completed
        high_priority = sum(1 for task in self.tasks if task["priority"] == "high" and not task["completed"])
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "high_priority": high_priority
        }