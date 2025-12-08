### controller.py ##
# ml_api/api/controller.py
from flask import Blueprint

# Création d'un Blueprint pour organiser nos routes API
# Cela permet de regrouper logiquement les endpoints liés
api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/", methods=["GET"])
def health():
    
    ## Endpoint de santé très simple.
    ## 
    ## Utile pour :
    ## - Vérifier que l'API est bien en ligne
    ## - Les tests de monitoring et de disponibilité
    ## - Les vérifications des load balancers
    
    ## Retourne toujours "ok" avec un code HTTP 200 si tout fonctionne.
    
    return "ok", 200