import sys
import os
import traceback
from tkinter import Tk
from gui.dashboard import IntelligentApp

# Optional: Log the error to a file in case of failure
def log_error(exception_info):
    with open("error_log.txt", "a") as log_file:
        log_file.write(exception_info + "\n")

if __name__ == "__main__":
    try:
        print("Main.py starting...")
        print("Launching GUI...")
        root = Tk()
        app = IntelligentApp(root)
        root.mainloop()

    except Exception as e:
        # Print the full traceback in the terminal
        error_message = "An error occurred:\n" + traceback.format_exc()
        print(error_message)
        
        # Optionally log the error to a file for future debugging
        log_error(error_message)
