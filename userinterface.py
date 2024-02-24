import tkinter as tk
import pygubu
from tkinter import messagebox
from typing import Dict, List
from supabase_manager import supabase, insert_user

# Make build_ui_instance a global variable to hold the pygubu.Builder instance
build_ui_instance: pygubu.Builder = pygubu.Builder()


def on_continue_clicked(root: tk.Tk, users, input_ids) -> None:
    # Initialize lists to store user data
    user_data = []

    # Iterate over input IDs to retrieve user information
    for input_id, field_name in input_ids.items():
        if "_user_id_" in input_id:  # Check if the input ID corresponds to user ID
            entry = build_ui_instance.get_object(input_id)
            username_field = input_id.replace("user_id", "username")  # Get corresponding username field ID
            username_entry = build_ui_instance.get_object(username_field)
            user_id = entry.get().strip()
            username = username_entry.get().strip()
            if user_id and username:  # Only append if both user ID and username are not empty
                user_data.append((user_id, username))

    # Insert user data into Supabase table
    for user_id, username in user_data:
        # Convert user_id to int (assuming user_id should be an integer)
        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Error", "User ID must be a valid number.")
            return

        # Check if user_id already exists in the users table
        query = supabase.table("users").select("user_id").eq("username", username)
        response = query.execute()

        # If user_id already exists, show error message and skip insertion
        if response.data:
            messagebox.showerror("Error", f"User ID {user_id} already exists.")
            continue
        else:
            # If user_id doesn't exist, add the user to the Supabase table
            insert_user(username, user_id)
            messagebox.showinfo("Info", f"User ID {user_id} not found, adding to the database.")

    # Notify user of successful insertion
    messagebox.showinfo("Success", "User information inserted successfully.")


def build_ui(root: tk.Tk, users: dict) -> None:
    global build_ui_instance  # Make sure to use the global instance

    try:
        build_ui_instance.add_from_file("ui/player_interface.ui")
    except:
        build_ui_instance.add_from_file("../ui/player_interface.ui")

    main_frame: tk.Frame = build_ui_instance.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    red_frame: tk.Frame = build_ui_instance.get_object("red_team", main_frame)
    blue_frame: tk.Frame = build_ui_instance.get_object("blue_team", main_frame)

    input_ids: Dict[int, str] = {}
    fields: List[str] = {
        "red_equipment_id_",
        "red_user_id_",
        "red_username_",
        "blue_equipment_id_",
        "blue_user_id_",
        "blue_username_"
    }

    for i in range(1, 16):
        for field in fields:
            entry_id = f"{field}{i}"  # Use the ID from XML directly
            entry = build_ui_instance.get_object(entry_id,
                                                 red_frame if "red" in field else blue_frame)
            input_ids[entry_id] = entry_id  # Use the same ID for input_ids
            entry.bind("<Return>", lambda event, entry=entry: autofill_username(entry))

    submit_button = build_ui_instance.get_object("submit")
    submit_button.configure(command=lambda: on_continue_clicked(root, users, input_ids))


def autofill_username(entry):
    username = entry.get().strip()
    if username:
        try:
            # Get the parent frame
            parent_frame = entry.master
            while parent_frame.winfo_name() not in {"red_team", "blue_team"}:
                parent_frame = parent_frame.master

            # Get the corresponding username entry widget
            username_entry = parent_frame.nametowidget(entry.winfo_name().replace("user_id", "username"))
            if username_entry:
                # Query Supabase to find username based on user ID
                query = supabase.table("users").select("username").eq("user_id", username)
                response = query.execute()
                print("Response from Supabase:", response)  # Debugging statement

                # Check if response contains data and retrieve username
                if hasattr(response, "data") and len(response.data) > 0:
                    retrieved_username = response.data[0]["username"]
                    print("Retrieved username:", retrieved_username)  # Debugging statement
                    username_entry.delete(0, tk.END)  # Clear existing content
                    username_entry.insert(0, str(retrieved_username))
                else:
                    print("No username data found in response.")  # Debugging statement
            else:
                print("Username entry widget not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

