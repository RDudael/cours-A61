# packages/ml_api/tests/test_validation.py

from regression_model.config.core import config
from regression_model.processing.data_manager import load_dataset

from api.validation import PredictionResultSchema


def test_prediction_response_matches_schema(client):
    """
    Test d'intégration qui vérifie que les réponses de l'API
    respectent bien le format défini par notre schéma.
    
    Étapes :
    1. Chargement de données réelles de test
    2. Envoi d'une requête de prédiction à l'API
    3. Validation de la réponse avec le schéma Marshmallow
    """

    # 1. Chargement des données de test
    # On utilise les mêmes données que pour les autres tests
    test_data = load_dataset(file_name=config.app_config.test_data_file)
    payload = test_data[0:5].to_dict(orient="records")

    # 2. Appel de l'endpoint de prédiction
    response = client.post(
        "/v1/predict/regression",
        json={"inputs": payload},
    )

    # Vérification que l'API a répondu avec succès
    assert response.status_code == 200
    
    # Extraction des données JSON de la réponse
    response_json = response.get_json()

    # 3. Validation de la structure de la réponse
    schema = PredictionResultSchema()
    errors = schema.validate(response_json)

    # Si le schéma ne détecte aucune erreur, cela signifie que :
    # - Le format JSON est correct
    # - Tous les champs requis sont présents
    # - Les types de données sont valides
    assert errors == {}


def test_prediction_schema_detects_invalid_payload():
    """
    Test unitaire qui vérifie que notre schéma de validation
    détecte correctement les réponses mal formées.
    
    On teste ici la capacité du schéma à :
    - Rejeter les payloads avec des clés incorrectes
    - Exiger la présence des champs obligatoires
    """
    
    # Création d'une instance du schéma
    schema = PredictionResultSchema()

    # Payload volontairement invalide :
    # - "predictionz" au lieu de "predictions" (faute de frappe)
    # - Champ "errors" manquant (alors qu'il est requis)
    invalid_payload = {
        "predictionz": [1.23, 4.56],  # Mauvaise clé
        "version": "0.1.0",           # Bonne clé mais...
        # "errors" manquant intentionnellement
    }

    # Validation du payload invalide
    errors = schema.validate(invalid_payload)

    # Le schéma DOIT détecter des erreurs :
    # - Soit parce que "predictions" est manquant
    # - Soit parce que "errors" est manquant
    # - Soit les deux
    assert "predictions" in errors or "errors" in errors
    # (ou les deux, selon l'implémentation de Marshmallow)