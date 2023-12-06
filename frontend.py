# frontend/app.py
import tkinter as tk
from tkinter import messagebox
import requests

def get_user_profile(username):
    try:
        response = requests.get(f'http://127.0.0.1:5000/user/{username}')
        response.raise_for_status()  # Gère les erreurs HTTP

        user_data = response.json()
        display_user_profile(user_data)

    except requests.exceptions.HTTPError as errh:
        show_error_message(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        show_error_message(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        show_error_message(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        show_error_message(f"An error occurred: {err}")

def display_user_profile(user_data):
    messagebox.showinfo(
        'GitHub Profile',
        f"Username: {user_data['username']}\n"
        f"Repos: {user_data['repos_count']}\n"
        f"Followers: {user_data['followers_count']}\n"
        f"Following: {user_data['following_count']}"
    )

def show_error_message(message):
    messagebox.showerror('Error', message)

def on_submit():
    username = entry.get()
    if username:
        get_user_profile(username)
    else:
        show_error_message('Please enter a GitHub username.')

# Interface utilisateur
root = tk.Tk()
root.title('GitHub Profile Viewer')

label = tk.Label(root, text='Enter GitHub Username:')
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

submit_button = tk.Button(root, text='Submit', command=on_submit)
submit_button.pack(pady=20)

root.mainloop()
