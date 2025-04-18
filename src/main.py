print("Main.py starting...")

from gui.dashboard import IntelligentApp
from tkinter import Tk
import traceback  # Import traceback for better debugging

if __name__ == "__main__":
    try:
        print("Launching GUI...")
        root = Tk()
        app = IntelligentApp(root)
        root.mainloop()

    except Exception as e:
        # Print the full traceback in the terminal
        print("An error occurred:")
        print(traceback.format_exc())
