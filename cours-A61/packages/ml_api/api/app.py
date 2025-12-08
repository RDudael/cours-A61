## app.py ##
# ml_api/api/app.py
from flask import Flask
from .controller import api_bp  # Notre blueprint avec les routes API


def create_app() -> Flask:
    
    ## Fonction principale pour créer et configurer notre application Flask.
    
    ## Cette approche (factory function) est recommandée car elle permet de :
    ## - Créer plusieurs instances de l'app avec des configurations différentes
    ## - Faciliter les tests unitaires
    ## - Configurer l'app dynamiquement selon l'environnement
    
    # Création de l'application Flask
    app = Flask(__name__)

    # Enregistrement de notre blueprint principal
    # Celui-ci contient toutes nos routes API définies dans controller.py
    app.register_blueprint(api_bp)

    # On retourne l'application configurée
    return app