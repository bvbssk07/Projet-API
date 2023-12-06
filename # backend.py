# backend.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Remplacez 'YOUR_GITHUB_API_KEY' par votre clé d'API GitHub
GITHUB_API_KEY = 'https://github.com/bvbssk07/Projet-API.git'

@app.route('/user/<username>', methods=['GET'])
def get_user_profile(username):
    # Construire l'URL de l'API GitHub
    api_url = f'https://api.github.com/users/{username}'
    
    # Ajouter l'en-tête d'authentification avec la clé d'API
    headers = {'Authorization': f'token {GITHUB_API_KEY}'}

    try:
        # Effectuer la requête vers l'API GitHub
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

        # Récupérer les données JSON de la réponse
        user_data = response.json()

        # Filtrer les données à renvoyer au frontend pour éviter d'exposer des informations sensibles
        filtered_data = {
            'username': user_data['login'],
            'avatar_url': user_data['avatar_url'],
            'repositories': user_data['public_repos'],
            'followers': user_data['followers'],
            'following': user_data['following']
        }

        return jsonify(filtered_data)

    except requests.exceptions.HTTPError as err:
        # Gérer les erreurs HTTP et renvoyer un message d'erreur approprié au frontend
        return jsonify({'error': f'Failed to fetch user data: {str(err)}'}), 500

    except Exception as e:
        # Gérer les erreurs non HTTP
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

# frontend.py

import tkinter as tk
from tkinter import messagebox
import requests

def get_github_profile(username):
    backend_url = f'http://localhost:5000/user/{username}'

    try:
        response = requests.get(backend_url)
        response.raise_for_status()  # Gérer les erreurs HTTP

        profile_data = response.json()

        # Afficher les détails du profil récupéré
        messagebox.showinfo(
            'GitHub Profile',
            f"Username: {profile_data['login']}\n"
            f"Avatar: {profile_data['avatar_url']}\n"
            f"Repositories: {profile_data['public_repos']}\n"
            f"Followers: {profile_data['followers']}\n"
            f"Following: {profile_data['following']}"
        )

    except requests.exceptions.RequestException as e:
        # Informer l'utilisateur en cas d'échec de la requête
        messagebox.showerror('Error', f"Failed to retrieve GitHub profile: {str(e)}")

def on_submit():
    username = entry.get()
    if username:
        get_github_profile(username)
    else:
        messagebox.showwarning('Warning', 'Please enter a GitHub username.')

# Interface utilisateur
root = tk.Tk()
root.title('GitHub Profile Viewer')

label = tk.Label(root, text='Enter GitHub username:')
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

submit_button = tk.Button(root, text='Submit', command=on_submit)
submit_button.pack(pady=10)

root.mainloop()
