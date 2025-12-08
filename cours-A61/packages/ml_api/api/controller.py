# ml_api/api/controller.py

from flask import Blueprint, request, jsonify

from regression_model.predict import make_prediction  # Notre fonction de prédiction
from regression_model import __version__ as _model_version, logger  # Version et logger du modèle

# Création d'un blueprint pour organiser nos routes API
api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/", methods=["GET"])
def health():
    ## Endpoint de santé simple pour vérifier que l'API est opérationnelle.##
    logger.info("Health check called")
    return "ok", 200


@api_blueprint.route("/v1/predict/regression", methods=["POST"])
def predict():
    
    ## Endpoint principal pour obtenir des prédictions de prix.
    
    ## Format attendu pour les données d'entrée :{"inputs": [{ ... },  # caractéristiques de la première maison
            # { ... }   # caractéristiques de la deuxième maison
        # ]}
    
    ## Alternative : on accepte aussi directement une liste de dictionnaires
    
    # Récupération des données JSON envoyées par le client
    json_data = request.get_json()

    # Vérification basique : le client a-t-il envoyé des données ?
    if json_data is None:
        return jsonify({"errors": "No input data provided", "predictions": None, "version": _model_version}), 400

    # Tentative de récupération de la liste des observations
    # On s'attend à ce qu'elles soient sous la clé "inputs"
    inputs = json_data.get("inputs", None)
    
    # Si la clé "inputs" n'existe pas, on suppose que l'utilisateur
    # a envoyé directement la liste de dictionnaires
    if inputs is None:
        inputs = json_data

    # Log des données reçues pour la traçabilité
    logger.info(f"Inputs received for prediction: {inputs}")
    logger.info(f"Using model version: {_model_version}")

    # Appel à notre fonction de prédiction principale
    result = make_prediction(input_data=inputs)

    # Log des résultats pour le monitoring
    logger.info(f"Prediction result: {result}")

    # Le résultat est déjà un dictionnaire bien formaté avec :
    # - "predictions" : les prix estimés
    # - "errors" : les problèmes éventuels
    # - "version" : la version du modèle utilisé
    return jsonify(result), 200