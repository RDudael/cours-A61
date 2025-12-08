# regression_model/predict.py

from typing import Union, Dict, Any

import joblib
import numpy as np
import pandas as pd

from regression_model.train_pipeline import (
    TRAINED_MODEL_DIR,  # Dossier où le modèle entraîné est sauvegardé
    FEATURES,           # Liste des variables utilisées par le modèle
)
from regression_model.pipeline import PIPELINE_NAME
from regression_model.processing.validation import validate_inputs
from regression_model import logger, __version__


# Nom du fichier du pipeline sauvegardé (ex: lasso_regression.pkl)
PIPELINE_FILE_NAME = f"{PIPELINE_NAME}.pkl"


def _load_pipeline():
    
    ## Charge le pipeline entraîné depuis le disque.
    
    pipeline_path = TRAINED_MODEL_DIR / PIPELINE_FILE_NAME
    logger.info(f"Loading pipeline from: {pipeline_path}")
    trained_model = joblib.load(pipeline_path)
    return trained_model


def make_prediction(
    input_data: Union[pd.DataFrame, Dict[str, Any], list]
) -> Dict[str, Any]:
    
    ## Fonction principale pour obtenir des prédictions de prix.

    ## Elle accepte :
      ## - un DataFrame pandas
      ## - une liste de dictionnaires (format typique d'API)
      ## - un dictionnaire (une seule observation)

    ## Retourne :
      ## - predictions : liste de valeurs prédites ou None en cas d'erreur
      ## - errors      : dictionnaire des erreurs de validation ({} si OK)
      ## - version     : version du modèle utilisé
    

    logger.info(f"Inputs received for prediction: {input_data}")

    # Normalisation de l'entrée → toujours un DataFrame
    if isinstance(input_data, pd.DataFrame):
        data = input_data.copy()
    elif isinstance(input_data, dict):
        data = pd.DataFrame([input_data])
    else:
        # liste de dicts (cas de l'API) ou autre itérable
        data = pd.DataFrame(input_data)

    # Si jamais la variable cible est présente, on la retire
    if "SalePrice" in data.columns:
        data = data.drop(columns=["SalePrice"])

    # Validation & nettoyage
    data, errors = validate_inputs(data)

    logger.info(
        f"Making predictions with model version: {__version__} "
        f"Input shape: {data.shape}"
    )

    # Si des erreurs de validation sont détectées, on s'arrête là
    if errors:
        logger.info(f"Validation errors detected: {errors}")
        return {
            "predictions": None,
            "errors": errors,
            "version": __version__,
        }

    # On ne garde que les colonnes que le modèle connaît
    feature_cols = [col for col in FEATURES if col in data.columns]
    data = data[feature_cols]

    # Chargement du pipeline et prédiction
    pipeline = _load_pipeline()
    preds: np.ndarray = pipeline.predict(data)

    logger.info(f"Predictions done. Number of rows: {len(preds)}")

    # Retour du résultat au format JSON-sérialisable
    # Si aucun problème n'a été détecté, on renvoie errors = None
    
    if not errors:
        errors = None

    return {
        "predictions": preds.tolist(),  # liste → JSON friendly
        "errors": errors,               # None si tout va bien
        "version": __version__,}