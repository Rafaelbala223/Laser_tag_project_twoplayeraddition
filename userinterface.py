import tkinter as tk
import pygubu
from tkinter import messagebox
from typing import Dict, List
from supabase_manager import supabase, print_database_content, insert_user

# Make build_ui_instance a global variable to hold the pygubu.Builder instance
build_ui_instance: pygubu.Builder = pygubu.Builder()


def on_continue_clicked(root: tk.Tk, users, input_ids, build_ui) -> None:
    # Initialize lists to store user data
    user_data = []

    # Iterate over input IDs to retrieve user information
    for input_id, field_name in input_ids.items():
        entry = build_ui.get_object(input_id)
        if entry:
            # Get the username from the field name
            username = field_name.split("_")[-1]

            # Get the user ID from the entry field and remove leading/trailing spaces
            user_id_str = entry.get().strip()

            # Skip processing if both user ID and username are empty
            if not user_id_str and not username:
                continue

            # If user_id_str is not empty and consists only of digits, treat it as user_id
            if user_id_str and user_id_str.isdigit():
                user_id = int(user_id_str)
                user_data.append((username, user_id))
            else:
                # If user_id_str is not empty but not all digits, treat it as username
                user_data.append((user_id_str, None))

    # Validate user data here if needed
    if len(user_data) < 6:
        messagebox.showerror("Error", "Not enough user information provided.")
        return

    # Check each user to see if it already exists in Supabase
    for username, user_id in user_data:
        # Query Supabase to check if the user exists
        query = supabase.table("users").select("user_id").eq("username", username)
        if user_id is not None:
            query = query.eq("user_id", user_id)
        response = query.execute()

        # If the user doesn't exist, add them to Supabase
        if "data" not in response or len(response.data) == 0:
            insert_user(username, user_id)
        else:
            print(f"User {username} with ID {user_id} already exists in Supabase.")

    # Notify user of successful insertion
    messagebox.showinfo("Success", "User information inserted successfully.")
    

def build_ui(root: tk.Tk, users: dict) -> None:
    build_ui: pygubu.Builder = pygubu.Builder()
    try:
        build_ui.add_from_file("/Users/rafaelbalassiano/Desktop/LASER_TAG/Project/ui/player_interface.ui")
    except:
        build_ui.add_from_file("/Users/rafaelbalassiano/Desktop/LASER_TAG/Project/ui/player_interface.ui")
    
    # Place the main frame in the center of the root window
    # make unresizable
    main_frame: tk.Frame = build_ui.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create frames for the teams
    teams_frame: tk.Frame = build_ui.get_object("teams", main_frame)
    red_frame: tk.Frame = build_ui.get_object("red_team", teams_frame)
    blue_frame: tk.Frame = build_ui.get_object("blue_team", teams_frame)

    # Create a dictionary of IDs and corresponding entry field IDs
    input_ids: Dict[str, str] = {}
    fields: List[str] = {
        "red_equipment_id_",
        "red_user_id_",
        "red_username_",
        "blue_equipment_id_",
        "blue_user_id_",
        "blue_username_"
    }

    # Add each entry field ID to the dictionary of entry field IDs
    for field_name in fields:
        for i in range(1, 16):
            entry = build_ui.get_object(f"{field_name}{i}",
                                       red_frame if "red" in field_name else blue_frame)
            input_ids[f"{field_name}{i}"] = f"{field_name}{i}"  # Store the field name itself
            entry.bind("<Return>", lambda event, entry=entry: autofill_user_name(entry))
    
    print(input_ids)

    # Testing submit button
    build_ui.get_object("submit").configure(command=lambda: on_continue_clicked(root, users, input_ids, build_ui))


def autofill_user_name(entry):
    user_id = entry.get().strip()
    print("User ID:", user_id)  # Debugging statement
    if user_id:
        try:
            # Get the parent frame
            parent_frame = entry.master
            while parent_frame.winfo_name() not in {"red_team", "blue_team"}:
                parent_frame = parent_frame.master
            print("Parent frame name:", parent_frame.winfo_name())  # Debugging statement

            # Get the corresponding user name entry widget
            user_name_entry = parent_frame.nametowidget(entry.winfo_name().replace("user_id", "username"))
            print("Username entry widget name:", user_name_entry)  # Debugging statement
            if user_name_entry:
                # Query Supabase to find username based on user ID
                query = supabase.table("users").select("username").eq("user_id", user_id)
                print("Query:", query)  # Debugging statement
                response = query.execute()
                print("Response from Supabase:", response)  # Debugging statement

                # Check if response contains data and retrieve username
                if response and response.data:
                    username = response.data[0].get("username")
                    print("Retrieved username:", username)  # Debugging statement
                    user_name_entry.delete(0, tk.END)  # Clear existing content
                    user_name_entry.insert(0, username)
                else:
                    print("No username data found in response.")  # Debugging statement
            else:
                print("Username entry widget not found.")
        except Exception as e:
            print(f"An error occurred: {e}")