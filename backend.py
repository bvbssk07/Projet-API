# backend/app.py
from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

GITHUB_API_KEY = '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'
GITHUB_API_URL = 'https://api.github.com/users/'

@app.route('/user/<username>', methods=['GET'])
def get_user_profile(username):
    try:
        # Appel à l'API GitHub avec la clé d'API
        response = requests.get(f'{GITHUB_API_URL}{username}', headers={'Authorization': f'token {GITHUB_API_KEY}'})
        response.raise_for_status()  # Gère les erreurs HTTP

        user_data = response.json()
        # Filtrer les données sensibles si nécessaire
        filtered_data = {
            'username': user_data['login'],
            'avatar_url': user_data['avatar_url'],
            'repos_count': user_data['public_repos'],
            'followers_count': user_data['followers'],
            'following_count': user_data['following']
        }

        return jsonify(filtered_data)

    except requests.exceptions.HTTPError as errh:
        return jsonify({'error': f"HTTP Error: {errh}"})
    except requests.exceptions.ConnectionError as errc:
        return jsonify({'error': f"Error Connecting: {errc}"})
    except requests.exceptions.Timeout as errt:
        return jsonify({'error': f"Timeout Error: {errt}"})
    except requests.exceptions.RequestException as err:
        return jsonify({'error': f"An error occurred: {err}"})

if __name__ == '__main__':
    app.run(debug=True)
