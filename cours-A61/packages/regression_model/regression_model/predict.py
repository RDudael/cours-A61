## predict.py ##
from typing import Union, Dict, Any

import joblib
import numpy as np
import pandas as pd

from regression_model.train_pipeline import (
    TRAINED_MODEL_DIR,  # Où est rangé notre modèle
    FEATURES,           # La liste des caractéristiques que le modèle connaît
)
from regression_model.pipeline import PIPELINE_NAME  # Comment s'appelle notre fichier modèle
from regression_model.processing.validation import validate_inputs  # Pour vérifier les données


def _load_pipeline():
    
    ## Récupère notre modèle depuis le fichier où on l'a sauvegardé.##
    ## C'est comme aller chercher un livre dans une bibliothèque.##
    
    # On reconstitue le nom du fichier exact ##
    file_name = f"{PIPELINE_NAME}.pkl"
    pipeline_path = TRAINED_MODEL_DIR / file_name
    # On charge le modèle depuis le disque #
    trained_model = joblib.load(pipeline_path)
    return trained_model


def make_prediction(input_data: Union[pd.DataFrame, Dict[str, Any]]) -> Dict[str, Any]:
    
    ## C'est la fonction qu'on appelle quand on veut estimer le prix d'une maison.##
    
    ## On peut lui donner :
    ## - Soit un DataFrame complet (plusieurs maisons)
   ##  - Soit juste un dictionnaire (une seule maison)
    
    ## Elle nous retourne toujours deux choses :
    ## - Les prédictions (les prix estimés)
    ## - La liste des problèmes trouvés dans les données (s'il y en a) ##
    
    # Étape 0 : On s'assure d'avoir un DataFrame pandas, quel que soit le format d'entrée ##
    if isinstance(input_data, dict):
        # Si c'est un dictionnaire (une seule maison), on le transforme en DataFrame d'une ligne
        data = pd.DataFrame([input_data])
    else:
        # Sinon, on travaille sur une copie pour ne pas modifier les données originales
        data = input_data.copy()

    # Étape 1 : Vérification de la qualité des données
    # Est-ce qu'il manque des colonnes ? Y a-t-il des valeurs vides ?
    data, errors = validate_inputs(data)

    # Étape 2 : Si on a trouvé des problèmes, on s'arrête là
    # Pas la peine de donner des données incorrectes au modèle
    if errors:
        return {"predictions": None, "errors": errors}

    # Étape 3 : On ne garde que les colonnes que le modèle attend
    # C'est important pour éviter des erreurs et assurer que le modèle reçoit exactement
    # ce qu'il a appris à traiter
    data = data[FEATURES]

    # Étape 4 : Chargement du modèle et prédiction
    # On va chercher le modèle (il est chargé une seule fois puis mis en cache)
    pipeline = _load_pipeline()
    # On demande au modèle de nous donner ses estimations
    preds: np.ndarray = pipeline.predict(data)

    # Étape 5 : On retourne les résultats
    # Si tout s'est bien passé, "errors" sera un dictionnaire vide
    return {"predictions": preds, "errors": errors}