## app.py ##

from flask import Flask
from api.config import configure_logging  # Notre configuration centralisée des logs
from api.controller import api_blueprint   # Toutes nos routes API regroupées


def create_app() -> Flask:
    
    ## Fonction principale pour créer et configurer notre application Flask.
    
    ## Cette approche "factory" est recommandée car elle permet :
    ## - De configurer l'app différemment selon l'environnement (dev, test, prod)
    ## - De faciliter les tests en créant des instances isolées
    ## - D'appliquer la configuration dans un ordre contrôlé
    
    # 1. Configuration du système de logs (doit être fait en premier)
    configure_logging()

    # 2. Création de l'application Flask
    app = Flask(__name__)

    # 3. Enregistrement de toutes nos routes API
    # Le blueprint permet d'organiser les routes de façon modulaire
    app.register_blueprint(api_blueprint)

    # 4. Retour de l'application configurée
    return app


# Instance globale de l'application
# Cette variable est nécessaire pour que Gunicorn et autres serveurs WSGI
# puissent trouver et démarrer notre application
app = create_app()