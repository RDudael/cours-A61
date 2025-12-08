# Import de notre application Flask configurée
from api.app import app

if __name__ == "__main__":
    
    ## Point d'entrée pour l'exécution locale du serveur.
    
    ## Cette partie ne s'exécute que si on lance ce fichier directement,
    ## pas quand l'application est servie par un serveur WSGI comme Gunicorn.
    
    ## À utiliser uniquement pour le développement local.
    
    # Démarrage du serveur de développement Flask
    # Configuration pour le développement local :
    app.run(host="127.0.0.1",  # Accessible uniquement depuis la machine locale
        port=5000           # Port standard pour les applications Flask
    )
    # Note : debug=True n'est pas activé ici pour éviter les problèmes en production,
    # mais c'est souvent utile pour le développement (rechargement automatique, etc.)