# (Main Launcher) Bahar rahega, yahan se app start hoga

import sys
import os
import tkinter as tk

# 'src' folder ko system path mein daal rahe hain
# Is se Python ko pata chal jayega ke files kahan hain
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

# Ab hum direct import kar sakte hain (bina src. lagaye)
from cli_main import main as run_cli
from gui_app import main as run_gui

def main():
    print("=============================================")
    print("      Smart Waste Management System          ")
    print("=============================================")
    print("1. Text Mode ")  
    print("2. Graphical Mode ")
    
    choice = input("Enter Choice (1 or 2): ").strip()
    
    if choice == '1':
        run_cli()
    elif choice == '2':
        run_gui()  # This will show login window
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()