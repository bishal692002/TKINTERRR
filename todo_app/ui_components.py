# ui_components.py - Reusable UI components for the To-Do application

import tkinter as tk
from tkinter import ttk, messagebox
import random

class SidebarComponent:
    def __init__(self, parent, theme_manager, task_manager, update_callback):
        self.theme_manager = theme_manager
        self.task_manager = task_manager
        self.update_callback = update_callback
        
        # Create the sidebar frame
        self.frame = ttk.Frame(parent, style="Sidebar.TFrame", padding=(15, 15))
        
        # Statistics section
        self.stats_label = ttk.Label(
            self.frame, 
            text="STATISTICS", 
            style="Sidebar.TLabel", 
            font=self.theme_manager.subtitle_font
        )
        self.stats_label.pack(anchor="w", pady=(0, 10))
        
        self.total_tasks_label = ttk.Label(self.frame, text="Total Tasks: 0", style="Stats.TLabel")
        self.total_tasks_label.pack(anchor="w", pady=2)
        
        self.completed_tasks_label = ttk.Label(self.frame, text="Completed: 0", style="Stats.TLabel")
        self.completed_tasks_label.pack(anchor="w", pady=2)
        
        self.pending_tasks_label = ttk.Label(self.frame, text="Pending: 0", style="Stats.TLabel")
        self.pending_tasks_label.pack(anchor="w", pady=2)
        
        self.high_priority_label = ttk.Label(self.frame, text="High Priority: 0", style="Stats.TLabel")
        self.high_priority_label.pack(anchor="w", pady=2)
        
        # Motivational quotes
        self.quotes = [
            "The secret of getting ahead is getting started.",
            "Don't wait. The time will never be just right.",
            "Start where you are. Use what you have. Do what you can.",
            "It always seems impossible until it's done.",
            "The way to get started is to quit talking and begin doing."
        ]
        
        # Motivation section
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        self.motivation_label = ttk.Label(
            self.frame, 
            text="MOTIVATION", 
            style="Sidebar.TLabel", 
            font=self.theme_manager.subtitle_font
        )
        self.motivation_label.pack(anchor="w", pady=(0, 10))
        
        self.quote_label = ttk.Label(
            self.frame, 
            text=random.choice(self.quotes), 
            style="Stats.TLabel", 
            wraplength=150
        )
        self.quote_label.pack(anchor="w", pady=2)
        
        # Clear all button
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        self.clear_all_button = ttk.Button(
            self.frame, 
            text="Clear Completed", 
            command=self.clear_completed_tasks, 
            style="Clear.TButton"
        )
        self.clear_all_button.pack(pady=10, fill=tk.X)
    
    def clear_completed_tasks(self):
        """Clear completed tasks and update the UI"""
        if messagebox.askyesno("Confirm", "Are you sure you want to remove all completed tasks?"):
            if self.task_manager.clear_completed_tasks():
                self.update_callback()
    
    def update_statistics(self):
        """Update the statistics labels with current data"""
        stats = self.task_manager.get_statistics()
        
        self.total_tasks_label.config(text=f"Total Tasks: {stats['total']}")
        self.completed_tasks_label.config(text=f"Completed: {stats['completed']}")
        self.pending_tasks_label.config(text=f"Pending: {stats['pending']}")
        self.high_priority_label.config(text=f"High Priority: {stats['high_priority']}")


class TaskInputComponent:
    def __init__(self, parent, theme_manager, task_manager, update_callback):
        self.theme_manager = theme_manager
        self.task_manager = task_manager
        self.update_callback = update_callback
        
        # Create the input frame
        self.frame = ttk.Frame(parent, style="TFrame")
        
        # Task entry field
        self.task_entry = ttk.Entry(self.frame, font=self.theme_manager.text_font, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        # Priority selection
        priority_frame = ttk.Frame(self.frame, style="TFrame")
        priority_frame.pack(side=tk.LEFT, padx=5)
        
        self.priority_var = tk.StringVar(value="medium")
        ttk.Label(priority_frame, text="Priority:", style="TLabel").pack(side=tk.LEFT)
        
        ttk.Radiobutton(priority_frame, text="High", variable=self.priority_var, value="high").pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Medium", variable=self.priority_var, value="medium").pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Low", variable=self.priority_var, value="low").pack(side=tk.LEFT)
        
        # Add task button
        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        """Add a new task and update the UI"""
        task_text = self.task_entry.get()
        if self.task_manager.add_task(task_text, self.priority_var.get()):
            # Clear the entry field
            self.task_entry.delete(0, tk.END)
            # Update the UI
            self.update_callback()


class TaskListComponent:
    def __init__(self, parent, theme_manager, task_manager, update_callback):
        self.theme_manager = theme_manager
        self.task_manager = task_manager
        self.update_callback = update_callback
        
        # Create the list frame
        self.frame = ttk.Frame(parent, style="TFrame")
        
        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self.frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the treeview for tasks
        self.task_tree = ttk.Treeview(
            self.frame, 
            columns=("task", "priority", "date", "status"), 
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Set column headings
        self.task_tree.heading("task", text="Task Description")
        self.task_tree.heading("priority", text="Priority")
        self.task_tree.heading("date", text="Created")
        self.task_tree.heading("status", text="Status")
        
        # Configure column widths
        self.task_tree.column("task", width=300)
        self.task_tree.column("priority", width=80)
        self.task_tree.column("date", width=120)
        self.task_tree.column("status", width=100)
        
        # Pack the treeview and configure the scrollbar
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_tree.yview)
        
        # Bind double-click to toggle task status
        self.task_tree.bind("<Double-1>", self.toggle_task_status)
        
        # Bind right-click to show context menu
        self.task_tree.bind("<Button-3>", self.show_context_menu)
    
    def toggle_task_status(self, event):
        """Toggle a task's completion status on double-click"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        # Get the task ID from the first selected item
        task_id = selected_item[0]
        
        # Toggle the status
        if self.task_manager.toggle_task_status(task_id):
            self.update_callback()
    
    def show_context_menu(self, event):
        """Show the context menu on right-click"""
        # Get the item under cursor
        item = self.task_tree.identify_row(event.y)
        if not item:
            return
        
        # Select the item
        self.task_tree.selection_set(item)
        
        # Create a context menu
        context_menu = tk.Menu(self.frame, tearoff=0)
        context_menu.add_command(label="Delete Task", command=self.delete_selected_task)
        context_menu.add_command(label="Edit Task", command=self.edit_selected_task)
        context_menu.add_separator()
        context_menu.add_command(label="Mark as Completed", command=lambda: self.mark_task_as(True))
        context_menu.add_command(label="Mark as Pending", command=lambda: self.mark_task_as(False))
        
        # Display the context menu
        context_menu.tk_popup(event.x_root, event.y_root)
    
    def delete_selected_task(self):
        """Delete the selected task"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            # Get the task ID
            task_id = selected_item[0]
            
            # Delete the task
            self.task_manager.delete_task(task_id)
            self.update_callback()
    
    def edit_selected_task(self):
        """Edit the selected task"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        # Get the task ID
        task_id = selected_item[0]
        
        # Find the task
        for task in self.task_manager.tasks:
            if task["id"] == task_id:
                # Create a dialog for editing
                edit_window = tk.Toplevel(self.frame)
                edit_window.title("Edit Task")
                edit_window.geometry("400x200")
                edit_window.resizable(False, False)
                
                # Make dialog modal
                edit_window.transient(self.frame.winfo_toplevel())
                edit_window.grab_set()
                
                # Set dialog style
                edit_window.configure(bg=self.theme_manager.colors["bg_main"])
                
                # Task description
                ttk.Label(edit_window, text="Task Description:", style="TLabel").pack(pady=(20, 5))
                
                description_entry = ttk.Entry(edit_window, font=self.theme_manager.text_font, width=40)
                description_entry.pack(padx=20, fill=tk.X)
                description_entry.insert(0, task["description"])
                
                # Priority selection
                priority_frame = ttk.Frame(edit_window, style="TFrame")
                priority_frame.pack(pady=10)
                
                priority_var = tk.StringVar(value=task["priority"])
                ttk.Label(priority_frame, text="Priority:", style="TLabel").pack(side=tk.LEFT)
                
                ttk.Radiobutton(priority_frame, text="High", variable=priority_var, value="high").pack(side=tk.LEFT)
                ttk.Radiobutton(priority_frame, text="Medium", variable=priority_var, value="medium").pack(side=tk.LEFT)
                ttk.Radiobutton(priority_frame, text="Low", variable=priority_var, value="low").pack(side=tk.LEFT)
                
                # Button frame
                button_frame = ttk.Frame(edit_window, style="TFrame")
                button_frame.pack(pady=10)
                
                # Save button
                def save_changes():
                    self.task_manager.update_task(
                        task_id,
                        description=description_entry.get(),
                        priority=priority_var.get()
                    )
                    self.update_callback()
                    edit_window.destroy()
                
                ttk.Button(button_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
                ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
                
                # Focus on the entry widget
                description_entry.focus_set()
                
                break
    
    def mark_task_as(self, completed):
        """Mark the selected task as completed or pending"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        # Get the task ID
        task_id = selected_item[0]
        
        # Update the task
        self.task_manager.update_task(task_id, completed=completed)
        self.update_callback()
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        import tkinter.font as font
        
        # Clear the treeview
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Get sorted tasks
        sorted_tasks = self.task_manager.get_sorted_tasks()
        
        # Add tasks to the treeview
        for task in sorted_tasks:
            task_id = task["id"]
            status = "Completed" if task["completed"] else "Pending"
            
            # Set tag based on priority and completion status
            tags = (task["priority"], "completed" if task["completed"] else "pending")
            
            # Insert the task
            self.task_tree.insert("", tk.END, task_id, values=(
                task["description"],
                task["priority"].capitalize(),
                task["date_created"],
                status
            ), tags=tags)
        
        # Configure tag colors
        self.task_tree.tag_configure("high", foreground=self.theme_manager.colors["high_priority"])
        self.task_tree.tag_configure("medium", foreground=self.theme_manager.colors["medium_priority"])
        self.task_tree.tag_configure("low", foreground=self.theme_manager.colors["low_priority"])
        self.task_tree.tag_configure("completed", font=font.Font(family="Helvetica", size=10, overstrike=1))