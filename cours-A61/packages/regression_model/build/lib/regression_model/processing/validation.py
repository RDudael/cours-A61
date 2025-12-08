## regression_model/processing/validation.py ##

from typing import Dict, Any, Tuple

import pandas as pd

from regression_model.train_pipeline import FEATURES


def validate_inputs(input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    
    ## Vérifie que les données qu'on reçoit sont prêtes à être utilisées par le modèle.
    
    ## La seule vérification vraiment critique :
      ## - Est-ce que toutes les colonnes que le modèle connaît sont bien présentes ?
    
    ## Ce qu'on laisse passer volontairement :
      ## - Les valeurs manquantes (NaN) → le pipeline les gérera tout seul
      ## - Les colonnes en trop (comme 'Id') → on les ignorera simplement
    
    ## L'idée est d'être strict sur l'essentiel, mais flexible sur le reste.
    
    # On commence par faire une copie pour travailler sur des données indépendantes
    data = input_data.copy()
    errors: Dict[str, Any] = {}

    # Vérification centrale : les colonnes indispensables sont-elles toutes là ?
    # On compare la liste des colonnes reçues avec celle que le modèle attend
    missing_cols = [col for col in FEATURES if col not in data.columns]
    if missing_cols:
        # Si des colonnes manquent, on note lesquelles dans le rapport d'erreur
        errors["missing_columns"] = missing_cols

    # Note : on a retiré la vérification des colonnes en trop
    # Pourquoi ? Parce que si les données contiennent une colonne 'Id' ou autre,
    # ça ne gêne pas le modèle. On se contentera de l'ignorer plus tard.
    # (Le code commenté ci-dessous montre ce qu'on faisait avant)
    # extra_cols = [col for col in data.columns if col not in FEATURES]
    # if extra_cols:
    #     errors["extra_columns"] = extra_cols

    # On retourne les données (peut-être avec des colonnes supplémentaires)
    # et la liste des problèmes (vide si tout est OK)
    return data, errors