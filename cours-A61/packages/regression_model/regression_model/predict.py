## predict.py ##

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


def _load_pipeline():
    
    ## Récupère notre modèle sauvegardé depuis le disque.
    
    # On reconstitue le chemin exact du fichier modèle
    file_name = f"{PIPELINE_NAME}.pkl"
    pipeline_path = TRAINED_MODEL_DIR / file_name

    # On note dans les logs d'où on charge le modèle
    logger.info(f"Loading pipeline from: {pipeline_path}")
    trained_model = joblib.load(pipeline_path)
    return trained_model


def make_prediction(input_data: Union[pd.DataFrame, Dict[str, Any]]) -> Dict[str, Any]:
    
    ## La fonction principale pour obtenir des prédictions de prix.

    ## On peut lui fournir :
    ## - Un dictionnaire : les caractéristiques d'une seule maison
    ## - Un DataFrame : les caractéristiques de plusieurs maisons

    ## Elle retourne toujours trois informations :
    ## - Les prédictions (ou None en cas d'erreur)
    ## - Les problèmes éventuels détectés dans les données
    ## - La version du modèle utilisé (pour la traçabilité)
  

    # Étape 0 : normalisation du format d'entrée
    if isinstance(input_data, dict):
        # Un dictionnaire = une seule maison → on crée un DataFrame d'une ligne
        data = pd.DataFrame([input_data])
    else:
        # Déjà un DataFrame → on travaille sur une copie
        data = input_data.copy()

    # Étape 1 : validation et nettoyage des données
    data, errors = validate_inputs(data)

    # Log d'information sur la prédiction en cours
    logger.info(
        f"Making predictions with model version: {__version__} "
        f"Input shape: {data.shape}"
    )

    # Si la validation a détecté des problèmes, on s'arrête ici
    if errors:
        logger.info(f"Validation errors detected: {errors}")
        return {
            "predictions": None,   # Pas de prédictions possible
            "errors": errors,      # Détail des problèmes
            "version": __version__, # Version utilisée quand même
        }

    # Étape 2 : on sélectionne uniquement les colonnes que le modèle connaît
    # (celles avec lesquelles il a été entraîné)
    data = data[FEATURES]

    # Étape 3 : chargement du modèle et calcul des prédictions
    pipeline = _load_pipeline()
    preds: np.ndarray = pipeline.predict(data)

    # Message de confirmation
    logger.info(f"Predictions done. Number of rows: {len(preds)}")

    # Étape 4 : retour du résultat complet
    return {
        "predictions": preds,      # Les prix estimés
        "errors": errors,          # Normalement vide ({}), donc évalué comme False
        "version": __version__,    # Pour tracer l'origine des prédictions
    }