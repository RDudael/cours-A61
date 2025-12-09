# tests/test_controller.py

from regression_model.config.core import config
from regression_model.processing.data_manager import load_dataset

from ml_api import __version__ as api_version
from regression_model import __version__ as model_version


def test_root_endpoint_returns_ok(client):
    
    # Test de l'endpoint racine (/) qui sert de point de santé simple.
    
    # Vérifications :
    # - L'API répond avec un code HTTP 200 (succès)
    # - Le message retourné est bien "ok" (format texte brut)
    
    # Simulation d'une requête GET sur l'URL racine
    response = client.get("/")
    
    # Vérification du code de statut HTTP
    assert response.status_code == 200
    
    # Vérification du contenu (on décode les bytes en texte)
    assert response.data.decode("utf-8") == "ok"


def test_prediction_endpoint(client):
    
    # Test complet de l'endpoint de prédiction.
    # Ce test simule un scénario réel d'utilisation :
    # 1. Chargement de données de test valides
    # 2. Envoi au format attendu par l'API
    # 3. Vérification de la réponse complète
    
    # 1) Chargement des données de test depuis le fichier configuré
    #    Même source que pour les tests du modèle lui-même
    test_data = load_dataset(file_name=config.app_config.test_data_file)

    # 2) Préparation du payload : conversion des 5 premières maisons
    #    en liste de dictionnaires (format standard pour les APIs REST)
    payload = test_data[0:5].to_dict(orient="records")

    # 3) Envoi de la requête POST à l'endpoint de prédiction
    #    On utilise le format structuré {"inputs": [...]}
    response = client.post("/v1/predict/regression",json={"inputs": payload},)

    # Vérification que la requête a réussi (code 200)
    assert response.status_code == 200

    # Extraction des données JSON de la réponse
    response_json = response.get_json()

    # Vérification de la structure de base de la réponse
    # L'API doit toujours retourner ces trois champs
    assert "predictions" in response_json  # Les prix estimés
    assert "version" in response_json      # Version du modèle pour la traçabilité
    assert "errors" in response_json       # Liste des problèmes détectés

    # Vérification optionnelle : la version doit correspondre
    # (garantit qu'on utilise bien le modèle qu'on pense utiliser)
    assert response_json["version"] == model_version

    # Vérification du nombre de prédictions
    # Doit correspondre au nombre d'observations envoyées (5)
    assert len(response_json["predictions"]) == 5

    # Point important : gestion flexible des erreurs
    # Selon l'implémentation, "errors" peut être :
    # - None (aucune erreur)
    # - {} (dictionnaire vide, aucune erreur)
    # - [] (liste vide, aucune erreur)
    # Tous ces cas signifient "pas d'erreur"
    assert response_json["errors"] in (None, {}, [])


def test_version_endpoint_returns_correct_versions(client):
    
    # Test de l'endpoint /version qui expose les numéros de version.
    # Utile pour :
    # - Vérifier quelle version est déployée
    # - Diagnostiquer des problèmes de compatibilité
    
    # Simulation d'une requête GET vers /version
    response = client.get("/version")
    
    # Vérification du statut HTTP
    assert response.status_code == 200

    # Extraction des données JSON
    response_json = response.get_json()

    # Vérification de la structure de la réponse
    # Doit contenir les deux types de version
    assert "api_version" in response_json    # Version de l'API elle-même
    assert "model_version" in response_json  # Version du modèle ML

    # Vérification que les valeurs correspondent aux constantes importées
    # (garantit la cohérence entre ce qu'on déclare et ce qu'on expose)
    assert response_json["api_version"] == api_version
    assert response_json["model_version"] == model_version