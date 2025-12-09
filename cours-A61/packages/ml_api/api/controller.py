# ml_api/api/controller.py

from flask import Blueprint, request, jsonify
from regression_model.predict import make_prediction  # Notre fonction de prédiction

import logging

# Import "safe" de la version et du logger du modèle
try:
    from regression_model import __version__ as model_version, logger  # Version et logger du modèle
except ImportError:
    # Fallback si __version__ ou logger ne sont pas dispo (ex: lancement via run.py)
    model_version = "0.1.0"
    logger = logging.getLogger("regression_model")

# Import "safe" de la version de l'API
try:
    from ml_api import __version__ as api_version
except ImportError:
    # Fallback quand on lance `python run.py` depuis le dossier ml_api
    api_version = "0.1.0"

# Création d'un blueprint pour organiser nos routes API
api_blueprint = Blueprint("api", __name__)



@api_blueprint.route("/", methods=["GET"])
def health():
    """Endpoint de santé simple pour vérifier que l'API est opérationnelle."""
    logger.info("Health check called")
    return "ok", 200


@api_blueprint.route("/v1/predict/regression", methods=["POST"])
def predict():
    """
    Endpoint principal pour obtenir des prédictions de prix.

    Format JSON attendu :
    {
        "inputs": [
            {...},  # caractéristiques d'une première maison
            {...}   # caractéristiques d'une deuxième maison
        ]
    }

    On accepte aussi directement une liste de dictionnaires pour plus de flexibilité.
    """
    # Récupération des données JSON envoyées par le client
    json_data = request.get_json()

    # Vérification basique : le client a-t-il envoyé des données ?
    if json_data is None:
        # Retour d'une erreur 400 (Bad Request) si pas de données
        return jsonify(
            {
                "errors": "No input data provided",
                "predictions": None,
                "version": model_version,
            }
        ), 400

    # On essaie de récupérer la clé "inputs" (format structuré recommandé)
    inputs = json_data.get("inputs", None)

    # Si "inputs" n'existe pas, on suppose que l'utilisateur a envoyé
    # directement une liste de dictionnaires ou un dict unique
    # (pour la compatibilité avec d'anciens clients)
    if inputs is None:
        inputs = json_data

    # Log des données reçues pour la traçabilité
    logger.info(f"Inputs received for prediction: {inputs}")
    logger.info(f"Using model version: {model_version}")

    # Appel à notre fonction de prédiction principale
    # Celle-ci se charge de valider les données et de faire la prédiction
    result = make_prediction(input_data=inputs)

    # Log des résultats pour le monitoring
    logger.info(f"Prediction result: {result}")

    # Le résultat est déjà un dictionnaire bien formaté avec :
    # - "predictions" : les prix estimés
    # - "errors" : les problèmes éventuels
    # - "version" : la version du modèle utilisé
    return jsonify(result), 200


@api_blueprint.route("/version", methods=["GET"])
def version():
    """
    Endpoint pour récupérer les versions de l'API et du modèle.

    Très utile pour :
    - Déboguer des problèmes de version
    - Vérifier quelle version est déployée
    - S'assurer de la compatibilité API/modèle
    """
    response = {
        "api_version": api_version,      # Version de l'API (gérée dans ml_api)
        "model_version": model_version,  # Version du modèle (gérée dans regression_model)
    }
    return jsonify(response), 200