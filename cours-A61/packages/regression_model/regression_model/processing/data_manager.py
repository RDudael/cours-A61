# regression_model/processing/data_manager.py

from pathlib import Path
import pandas as pd
import joblib

from regression_model import logger

# Racine du package regression_model
# Utile pour construire des chemins relatifs fiables
PACKAGE_ROOT = Path(__file__).resolve().parent.parent

# Dossiers de données et de modèles
DATASET_DIR = PACKAGE_ROOT / "datasets"         # Contient les fichiers CSV de données
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"  # Contient les modèles sauvegardés


def load_dataset(*, file_name: str) -> pd.DataFrame:
    """
    Charge un jeu de données CSV depuis le dossier datasets.

    Cette fonction centralise le chargement des données pour garantir
    que tout le projet utilise les mêmes chemins et la même méthode.

    Paramètres
    ----------
    file_name : str
        Nom du fichier CSV à charger (par exemple : "train.csv" ou "test.csv").

    Retourne
    --------
    pandas.DataFrame
        Les données chargées, prêtes pour l'entraînement ou le test.
    """
    # Construction du chemin complet
    data_path = DATASET_DIR / file_name
    
    # Chargement avec pandas
    return pd.read_csv(data_path)


def load_pipeline(*, file_name: str):
    """
    Charge un modèle de machine learning préalablement sauvegardé.

    Fonction essentielle pour :
    - Le déploiement en production (charger le modèle entraîné)
    - Les tests (charger un modèle de référence)
    - Le versioning (charger différentes versions de modèles)

    Args:
        file_name: Nom du fichier .pkl contenant le modèle
                  (exemples : 'lasso_regression.pkl', 'model_v1.2.0.pkl')

    Returns:
        Un pipeline scikit-learn entraîné, prêt à faire des prédictions.
    """
    # Construction du chemin vers le fichier modèle
    pipeline_path = TRAINED_MODEL_DIR / file_name

    # Log pour la traçabilité (quel modèle, depuis où)
    logger.info(f"Loading pipeline from: {pipeline_path}")

    # Chargement avec joblib (format standard pour scikit-learn)
    trained_model = joblib.load(pipeline_path)
    
    return trained_model