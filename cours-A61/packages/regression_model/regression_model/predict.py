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
try:
    from regression_model import __version__
except ImportError:
    __version__ = "0.1.0"

# Logger principal du package
logger = logging.getLogger("regression_model")

# Nom du fichier du pipeline sauvegardé (ex: lasso_regression.pkl)
PIPELINE_FILE_NAME = f"{PIPELINE_NAME}.pkl"


def _load_pipeline():
    """Charge le modèle entraîné depuis le fichier où on l'a sauvegardé."""
    pipeline_path = TRAINED_MODEL_DIR / PIPELINE_FILE_NAME
    logger.info(f"Loading pipeline from: {pipeline_path}")
    trained_model = joblib.load(pipeline_path)
    return trained_model


def make_prediction(
    input_data: Union[pd.DataFrame, Dict[str, Any], list]
) -> Dict[str, Any]:
    """
    Fonction principale pour obtenir des prédictions de prix.

    Accepte :
      - Un DataFrame pandas
      - Un dictionnaire (une seule maison)
      - Une liste de dictionnaires (format API)

    Retourne toujours un dictionnaire structuré avec :
      - predictions : liste de prix prédits (ou None en cas d'erreur)
      - errors      : dict décrivant les problèmes éventuels ({} si tout va bien)
      - version     : version du package regression_model utilisé
    """

    logger.info(f"Inputs received for prediction: {input_data}")
    logger.info(f"Using model version: {__version__}")

    # Étape 1 : Normalisation du format d'entrée
    if isinstance(input_data, pd.DataFrame):
        data = input_data.copy()
    elif isinstance(input_data, dict):
        data = pd.DataFrame([input_data])
    else:
        # On suppose une liste de dictionnaires
        data = pd.DataFrame(input_data)

    # Étape 2 : Suppression préventive de la variable cible si présente
    if "SalePrice" in data.columns:
        data = data.drop(columns=["SalePrice"])

    # Étape 3 : Validation et nettoyage des données
    data, errors = validate_inputs(data)

    logger.info(
        f"Making predictions with model version: {__version__} "
        f"Input shape: {data.shape}"
    )

    # Étape 4 : Gestion des erreurs de validation
    if errors:
        logger.info(f"Validation errors detected: {errors}")
        return {
            "predictions": None,
            "errors": errors,
            "version": __version__,
        }

    # Étape 5 : Sélection des colonnes pertinentes
    feature_cols = [col for col in FEATURES if col in data.columns]
    data = data[feature_cols]

    # Étape 6 : Chargement du modèle et prédiction
    pipeline = _load_pipeline()
    preds: np.ndarray = pipeline.predict(data)

    logger.info(f"Predictions done. Number of rows: {len(preds)}")

    # Étape 7 : Construction du résultat (aucune erreur à ce stade)
    result: Dict[str, Any] = {
        "predictions": list(preds),  # np.ndarray -> liste pour JSON
        "version": __version__,
        "errors": {},  # dict vide attendu par les tests lorsque tout va bien
    }

    return result