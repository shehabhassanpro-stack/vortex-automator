"""
Vortex Automator - Application Entry Point
High-Performance Key Presser & Auto Clicker for Windows
"""

import sys
import customtkinter as ctk
from vortex.ui.main_window import MainWindow

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
