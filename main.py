from dotenv import load_dotenv
import tkinter as tk
import os
import splashscreen
import userinterface
from users import User
import supabase_manager
from supabase_manager import supabase,create_client, insert_user, print_database_content

# Create the Supabase client
supabase_client = supabase_manager.supabase


def build_root() -> tk.Tk:
    # Build main window, set title, make fullscreen
    root: tk.Tk = tk.Tk()
    root.title("PhotonLaserTag")
    root.configure(background="white")

    # If platform is not Linux, set to zoomed and include icon
    if os.name != "zoomed":
        root.state("zoomed")
        # Load logo! change to ico extension
        try:
            root.iconbitmap("/Users/rafaelbalassiano/Desktop/LASER_TAG/Project/images/logo.jpg")
        except:
            root.iconbitmap("/Users/rafaelbalassiano/Desktop/LASER_TAG/Project/images/logo.jpg")

            # Force window to fill screen, place at top left
    width: int = root.winfo_screenwidth()
    height: int = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")

    # Disable resizing
    # User will have to play full screen
    root.resizable(False, False)
    return root

# --------------------------------
# MAIN!
# --------------------------------

# build the root of the screen
root: tk.Tk = build_root()

# build the splash screen that dissapears in 3 seconds
splash: splashscreen = splashscreen.build(root)
root.after(3000, splash.destroy)

root.after(3000, userinterface.build_ui, root, User)

root.mainloop()
