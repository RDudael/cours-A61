## predict.py ##
from typing import Union, Dict, Any

import joblib
import numpy as np
import pandas as pd

from regression_model.train_pipeline import (
    TRAINED_MODEL_DIR,        # Où on a rangé notre modèle
    TESTING_DATA_FILE,        # Les données de test si on veut vérifier
    FEATURES,                 # La liste des caractéristiques attendues
)
from regression_model.pipeline import PIPELINE_NAME  # Le nom du fichier du modèle


def _load_pipeline():
    ## On Va chercher le modèle entraîné qu'on a sauvegardé précédemment.##
    # On reconstitue le chemin exact du fichier .pkl
    file_name = f"{PIPELINE_NAME}.pkl"
    pipeline_path = TRAINED_MODEL_DIR / file_name
    
    # On charge le modèle depuis le disque
    trained_model = joblib.load(pipeline_path)
    return trained_model


def make_prediction(input_data: Union[pd.DataFrame, Dict[str, Any]]) -> Dict[str, np.ndarray]:
    
    ## La fonction qu'on appelle pour obtenir des prédictions de prix.
    
    ## Par exemple : Combien vaut cette maison ? ##
    
    ## Ce qu'on peut lui donner en entrée :
    ##- Un DataFrame pandas complet
    ##- Ou simplement un dictionnaire avec les caractéristiques d'une maison
    
    ##Ce qu'elle nous renvoie :
    ##- Un dictionnaire avec la clé "predictions" contenant les prix estimés ###
    

    # Si on reçoit un dictionnaire (données d'une seule maison), on le transforme en DataFrame
    if isinstance(input_data, dict):
        data = pd.DataFrame(input_data)
    else:
        # Sinon, on travaille directement sur une copie du DataFrame
        data = input_data.copy()

    # Important : on ne garde que les colonnes que le modèle connaît
    # (celles avec lesquelles il a été entraîné)
    data = data[FEATURES]

    # On charge le modèle (s'il n'est pas déjà en mémoire)
    pipeline = _load_pipeline()
    
    # On demande au modèle de prédire les prix
    preds = pipeline.predict(data)

    # On retourne les résultats dans un format clair
    return {"predictions": preds}