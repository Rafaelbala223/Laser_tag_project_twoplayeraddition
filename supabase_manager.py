from dotenv import load_dotenv
import os
from supabase import create_client
from postgrest.exceptions import APIError

# Load environment variables from .env file
load_dotenv()

# Retrieve Supabase URL and key from environment variables
url = "https://pdfbshphnccebqdnhawd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkZmJzaHBobmNjZWJxZG5oYXdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgzNjE4OTMsImV4cCI6MjAyMzkzNzg5M30.ZYfCEZfUHuOVlMqDLIkSEA7_PU4B5OHWD-CUGjwfYI8"

print("URL:", url)
print("Key:", key)

# Check if the URL or key is missing
if url is None or key is None:
    raise ValueError("Supabase URL or key not found in environment variables.")

# Create Supabase client
supabase = create_client(url, key)


def insert_user(username, user_id):
    # Define the data to be inserted
    data = {'username': username, 'user_id': user_id}

    # Insert data into "users" table
    try:
        response = supabase.table('users').insert(data).execute()
        print("User inserted successfully.")
    except APIError as e:
        if e.code == '23505':
            print(f"Failed to insert user: {e.message}")
        else:
            print("Failed to insert user due to an unknown error.")
            print(e)
