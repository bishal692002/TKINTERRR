# todo_app.py - Main To-Do application class

import tkinter as tk
from tkinter import ttk, messagebox, font

from ui_components import SidebarComponent, TaskInputComponent, TaskListComponent
from task_manager import TaskManager
from theme_manager import ThemeManager

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Master - Your Personal To-Do Manager")
        self.root.geometry("800x600")
        self.root.minsize(650, 500)
        
        # Initialize the theme manager
        self.theme_manager = ThemeManager()
        
        # Initialize the task manager
        self.task_manager = TaskManager("tasks.json")
        self.task_manager.load_tasks()
        
        # Setup the UI
        self.setup_ui()
        
        # Configure the row and column weights to make the UI responsive
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    
    def setup_ui(self):
        # App header
        self.header_frame = ttk.Frame(self.root, style="TFrame", padding=(10, 10))
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Task Master", 
            style="Title.TLabel", 
            font=self.theme_manager.title_font
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Current date display
        from datetime import datetime
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.date_label = ttk.Label(
            self.header_frame, 
            text=current_date, 
            font=self.theme_manager.text_font
        )
        self.date_label.pack(side=tk.RIGHT, padx=10)
        
        # Create the sidebar component
        self.sidebar = SidebarComponent(
            self.root, 
            self.theme_manager, 
            self.task_manager,
            self.update_statistics
        )
        self.sidebar.frame.grid(row=1, column=0, sticky="ns")
        
        # Main content area
        self.main_frame = ttk.Frame(self.root, style="TFrame", padding=(20, 10))
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        
        # Task input component
        self.task_input = TaskInputComponent(
            self.main_frame, 
            self.theme_manager, 
            self.task_manager,
            self.refresh_ui
        )
        self.task_input.frame.pack(fill=tk.X, pady=(0, 10))
        
        # Task list component
        self.task_list = TaskListComponent(
            self.main_frame, 
            self.theme_manager, 
            self.task_manager,
            self.refresh_ui
        )
        self.task_list.frame.pack(fill=tk.BOTH, expand=True)
        
        # Initial UI refresh
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh all UI components when tasks change"""
        self.task_list.refresh_task_list()
        self.update_statistics()
    
    def update_statistics(self):
        """Update the statistics in the sidebar"""
        self.sidebar.update_statistics()