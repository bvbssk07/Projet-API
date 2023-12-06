# backend.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Remplacez 'YOUR_GITHUB_API_KEY' par votre clé d'API GitHub
GITHUB_API_KEY = 'YOUR_GITHUB_API_KEY'

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
