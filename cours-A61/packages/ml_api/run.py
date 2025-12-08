## run.py ##
# ml_api/run.py
from api.app import create_app  # api = dossier ml_api/api


# Création de l'application Flask principale
# Cette variable 'app' est ce que serveurs WSGI comme Gunicorn recherchent
app = create_app()


if __name__ == "__main__":
    
    ## Point d'entrée pour l'exécution locale du serveur.
    
    ## Note : Cette section ne s'exécute que quand on lance le fichier directement,
    ## pas quand l'app est servie par un serveur WSGI comme Gunicorn.
    
    # Lancement du serveur de développement Flask en local
    app.run(
        host="0.0.0.0",   # Accessible depuis toutes les interfaces réseau
        port=5000,        # Port par défaut des applications Flask
        debug=False       # Désactivé en production (mais utile en dev)
    )