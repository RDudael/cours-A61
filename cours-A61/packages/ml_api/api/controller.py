### controller.py ##

import logging

from flask import Blueprint, jsonify, request

from regression_model.predict import make_prediction  # Notre fonction de prédiction
from regression_model import __version__ as _model_version  # Version du modèle

# Logger spécifique pour notre API (différent du logger du modèle)
_logger = logging.getLogger("ml_api")

# Création d'un blueprint pour organiser nos routes API
api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/", methods=["GET"])
def index():
    """Endpoint de test simple pour vérifier que l'API répond."""
    return "ok"


@api_blueprint.route("/health", methods=["GET"])
def health():
    """Endpoint de santé utilisé pour le monitoring et les vérifications automatiques."""
    _logger.info("Health check called")
    return jsonify({"status": "ok", "model_version": _model_version})


@api_blueprint.route("/v1/predictions/regression", methods=["POST"])
def predict():
    """
    Endpoint principal pour obtenir des prédictions de prix.
    
    Accepte des données JSON en POST et retourne les prédictions du modèle.
    """
    # Récupération des données JSON envoyées par le client
    json_data = request.get_json()

    # Vérification basique : est-ce qu'on a bien reçu du JSON ?
    if json_data is None:
        _logger.error("No JSON payload received")
        return jsonify({"errors": "Invalid input, no JSON received"}), 400

    # Gestion des deux formats possibles :
    # - Un dictionnaire simple (une seule maison)
    # - Une liste de dictionnaires (plusieurs maisons)
    if isinstance(json_data, dict):
        input_data = json_data
    else:
        input_data = json_data[0]  # On prend le premier élément pour l'instant

    _logger.info(f"Inputs for prediction: {input_data}")

    # Appel à notre fonction de prédiction (la même que dans le package)
    result = make_prediction(input_data=input_data)

    _logger.info(f"Prediction result: {result}")

    # Retour des résultats au format JSON
    return jsonify(result)