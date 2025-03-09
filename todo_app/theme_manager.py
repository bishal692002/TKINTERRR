# theme_manager.py - Manages application themes and styling

from tkinter import font, ttk

class ThemeManager:
    def __init__(self):
        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.text_font = font.Font(family="Helvetica", size=10)
        
        # Set custom colors
        self.colors = {
            "bg_main": "#f5f5f5",
            "bg_sidebar": "#3a4750",
            "accent": "#00adb5",
            "text_light": "#ffffff",
            "text_dark": "#303841",
            "high_priority": "#ff5252",
            "medium_priority": "#ffb142",
            "low_priority": "#2ed573"
        }
        
        # Configure the styles
        self.configure_styles()
    
    def configure_styles(self):
        """Configure the ttk styles with the theme colors"""
        self.style = ttk.Style()
        
        # Frame styles
        self.style.configure("TFrame", background=self.colors["bg_main"])
        self.style.configure("Sidebar.TFrame", background=self.colors["bg_sidebar"])
        
        # Button styles
        self.style.configure("Accent.TButton", background=self.colors["accent"], foreground=self.colors["text_light"])
        self.style.configure("Clear.TButton", background="#ff5252", foreground=self.colors["text_light"])
        
        # Label styles
        self.style.configure("TLabel", background=self.colors["bg_main"], foreground=self.colors["text_dark"])
        self.style.configure("Sidebar.TLabel", background=self.colors["bg_sidebar"], foreground=self.colors["text_light"])
        self.style.configure("Stats.TLabel", background=self.colors["bg_sidebar"], foreground=self.colors["text_light"], font=self.text_font)
        self.style.configure("Title.TLabel", font=self.title_font, background=self.colors["bg_main"], foreground=self.colors["text_dark"])
        
        # Treeview styles
        self.style.configure("Treeview", 
                            background=self.colors["bg_main"],
                            foreground=self.colors["text_dark"],
                            rowheight=40,
                            fieldbackground=self.colors["bg_main"],
                            font=self.text_font)
        
        self.style.map('Treeview', background=[('selected', self.colors["accent"])])