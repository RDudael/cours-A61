## test_controller.py ##

from regression_model.config.core import config
from regression_model.processing.data_manager import load_dataset


def test_root_endpoint_returns_ok(client):
    
    ## Test que l'endpoint racine (/) fonctionne correctement.
    
    ## Vérifications :
    ## - L'API répond avec un code 200 (succès)
    ## - Le message retourné est bien "ok"
    
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "ok"


def test_prediction_endpoint(client):
    
    ## Test complet de l'endpoint de prédiction.
    ## Étapes :
    ## 1. Chargement de vraies données de test
    ## 2. Conversion en format adapté pour l'API
    ## 3. Envoi d'une requête de prédiction
    ## 4. Vérification de la structure et du contenu de la réponse
    
    # Chargement des données de test depuis le fichier configuré
    test_data = load_dataset(file_name=config.app_config.test_data_file)
    
    # Préparation du payload : 5 premières maisons au format liste de dictionnaires
    payload = test_data[0:5].to_dict(orient="records")

    # Envoi de la requête POST à l'endpoint de prédiction
    response = client.post(
        "/v1/predict/regression",
        json={"inputs": payload},  # Format JSON attendu par l'API
    )

    # Vérification que la requête a réussi
    assert response.status_code == 200
    
    # Extraction des données JSON de la réponse
    response_json = response.get_json()

    # Vérification de la présence des champs obligatoires
    assert "predictions" in response_json  # Les prix estimés
    assert "version" in response_json      # Version du modèle utilisé
    assert "errors" in response_json       # Liste des problèmes (normalement vide)

    # Vérification du contenu
    assert response_json["errors"] is None  # Aucune erreur attendue avec des données valides
    assert len(response_json["predictions"]) == 5  # Une prédiction par maison envoyée