# regression_model/predict.py

from typing import Union, Dict, Any
import logging

import joblib
import numpy as np
import pandas as pd

from regression_model.train_pipeline import (
    TRAINED_MODEL_DIR,  # Dossier où le modèle entraîné est sauvegardé
    FEATURES,           # Liste des variables utilisées par le modèle
)
from regression_model.pipeline import PIPELINE_NAME
from regression_model.processing.validation import validate_inputs

# Import "sécurisé" de la version du modèle
# (pour éviter les erreurs si l'import standard échoue)
try:
    from regression_model import __version__
except ImportError:
    # Fallback si jamais l'import direct échoue
    # (cas rare, par exemple si le package n'est pas installé)
    __version__ = "0.1.0"

# Logger spécifique à ce module
# Utilise le même nom que le logger principal pour une configuration cohérente
logger = logging.getLogger("regression_model")


# Nom du fichier du pipeline sauvegardé (ex: lasso_regression.pkl)
PIPELINE_FILE_NAME = f"{PIPELINE_NAME}.pkl"


def _load_pipeline():
    """Charge le modèle entraîné depuis le fichier où on l'a sauvegardé."""
    pipeline_path = TRAINED_MODEL_DIR / PIPELINE_FILE_NAME
    logger.info(f"Loading pipeline from: {pipeline_path}")
    trained_model = joblib.load(pipeline_path)
    return trained_model


def make_prediction(input_data: Union[pd.DataFrame, Dict[str, Any], list]) -> Dict[str, Any]:
    
    # Fonction principale pour obtenir des prédictions de prix.
    # Conçue pour être flexible, elle accepte :
      # - Un DataFrame pandas (usage interne)
      # - Une liste de dictionnaires (format standard des APIs)
      # - Un dictionnaire simple (une seule maison)
    # Retourne toujours un dictionnaire structuré avec :
      # - predictions : les prix estimés (ou None en cas d'erreur)
      # - errors      : les problèmes détectés (None si tout va bien)
      # - version     : la version exacte du modèle utilisé
    

    logger.info(f"Inputs received for prediction: {input_data}")
    logger.info(f"Using model version: {__version__}")

    # Étape 1 : Normalisation du format d'entrée
    # On s'assure d'avoir toujours un DataFrame, quel que soit le format initial
    if isinstance(input_data, pd.DataFrame):
        data = input_data.copy()  # On travaille sur une copie pour ne pas modifier l'original
    elif isinstance(input_data, dict):
        # Un dictionnaire = une seule maison → on crée un DataFrame d'une ligne
        data = pd.DataFrame([input_data])
    else:
        # Par défaut, on suppose une liste de dictionnaires
        # (le format le plus courant depuis l'API)
        data = pd.DataFrame(input_data)

    # Étape 2 : Suppression préventive de la variable cible
    # Si "SalePrice" est présent par erreur, on le retire
    # (le modèle n'a pas besoin de connaître le vrai prix pour prédire)
    if "SalePrice" in data.columns:
        data = data.drop(columns=["SalePrice"])

    # Étape 3 : Validation et nettoyage des données
    # Vérifie le format, les colonnes manquantes, etc.
    data, errors = validate_inputs(data)

    logger.info(f"Making predictions with model version: {__version__} "
        f"Input shape: {data.shape}")

    # Étape 4 : Gestion des erreurs de validation
    # Si on a détecté des problèmes, on s'arrête ici
    if errors:
        logger.info(f"Validation errors detected: {errors}")
        return {
            "predictions": None,   # Pas de prédictions possibles
            "errors": errors,      # Détail des problèmes
            "version": __version__, # Version utilisée quand même
        }

    # Étape 5 : Sélection des colonnes pertinentes
    # On ne garde que les colonnes que le modèle connaît
    # (et qui sont présentes dans les données)
    feature_cols = [col for col in FEATURES if col in data.columns]
    data = data[feature_cols]

    # Étape 6 : Chargement du modèle et prédiction
    pipeline = _load_pipeline()
    preds: np.ndarray = pipeline.predict(data)

    logger.info(f"Predictions done. Number of rows: {len(preds)}")

    # Étape 7 : Formatage final des erreurs
    # Si la validation n'a trouvé aucun problème, on utilise None
    # (plus clair qu'un dictionnaire vide pour signifier "aucune erreur")
    if not errors:
        errors = None

    # Étape 8 : Retour du résultat
    # Si aucune erreur n’a été remontée par la validation,
    # on renvoie un dict vide plutôt que None (pour satisfaire les tests)
    if errors is None:
        errors = {}

    result = {
        "predictions": predictions,
        "version": _version,
        "errors": errors,
    }
    return result
