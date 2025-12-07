## train_pipeline.py ##

import pathlib
from typing import List

import joblib
import pandas as pd

from regression_model.pipeline import price_pipe, PIPELINE_NAME
from regression_model import logger, __version__   # notre logger global et la version du modèle

# --- Chemins des dossiers ---
# Où se trouve notre projet
PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
# Où on rangera les modèles une fois entraînés
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
# Où sont stockées nos données
DATASET_DIR = PACKAGE_ROOT / "datasets"

# --- Fichiers de données ---
# Les données pour tester le modèle (plus tard)
TESTING_DATA_FILE = DATASET_DIR / "test.csv"
# Les données pour entraîner le modèle (maintenant)
TRAINING_DATA_FILE = DATASET_DIR / "train.csv"

# Ce qu'on veut prédire : le prix de vente des maisons
TARGET = "SalePrice"

# Toutes les caractéristiques qu'on utilise pour faire nos prédictions
FEATURES: List[str] = [
    "MSSubClass",
    "MSZoning",
    "LotFrontage",
    "LotArea",
    "Street",
    "Alley",
    "LotShape",
    "LandContour",
    "Utilities",
    "LotConfig",
    "LandSlope",
    "Neighborhood",
    "Condition1",
    "Condition2",
    "BldgType",
    "HouseStyle",
    "OverallQual",
    "OverallCond",
    "YearBuilt",
    "YearRemodAdd",
    "RoofStyle",
    "RoofMatl",
    "Exterior1st",
    "Exterior2nd",
    "MasVnrType",
    "MasVnrArea",
    "ExterQual",
    "ExterCond",
    "Foundation",
    "BsmtQual",
    "BsmtCond",
    "BsmtExposure",
    "BsmtFinType1",
    "BsmtFinSF1",
    "BsmtFinType2",
    "BsmtFinSF2",
    "BsmtUnfSF",
    "TotalBsmtSF",
    "Heating",
    "HeatingQC",
    "CentralAir",
    "Electrical",
    "1stFlrSF",
    "2ndFlrSF",
    "LowQualFinSF",
    "GrLivArea",
    "BsmtFullBath",
    "BsmtHalfBath",
    "FullBath",
    "HalfBath",
    "BedroomAbvGr",
    "KitchenAbvGr",
    "KitchenQual",
    "TotRmsAbvGrd",
    "Functional",
    "Fireplaces",
    "FireplaceQu",
    "GarageType",
    "GarageYrBlt",
    "GarageFinish",
    "GarageCars",
    "GarageArea",
    "GarageQual",
    "GarageCond",
    "PavedDrive",
    "WoodDeckSF",
    "OpenPorchSF",
    "EnclosedPorch",
    "3SsnPorch",
    "ScreenPorch",
    "PoolArea",
    "PoolQC",
    "Fence",
    "MiscFeature",
    "MiscVal",
    "MoSold",
    "YrSold",
    "SaleType",
    "SaleCondition",
]


def save_pipeline(pipeline_to_persist) -> None:
    """Prend le modèle entraîné et le sauvegarde sur le disque pour plus tard."""
    # On s'assure que le dossier existe (on le crée si besoin)
    TRAINED_MODEL_DIR.mkdir(exist_ok=True)

    # On choisit un nom de fichier cohérent
    save_file_name = f"{PIPELINE_NAME}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    # Sauvegarde avec joblib (format standard pour scikit-learn)
    joblib.dump(pipeline_to_persist, save_path)


def run_training() -> None:
    """La fonction principale : charge les données, entraîne le modèle, le sauvegarde."""
    # Étape 1 : Chargement des données d'entraînement
    data = pd.read_csv(TRAINING_DATA_FILE)

    # On sépare les caractéristiques (X) de la cible (y)
    X = data[FEATURES].copy()
    y = data[TARGET]

    # On commence par un message dans les logs
    logger.info("Starting model training")

    # Étape 2 : Entraînement du modèle
    price_pipe.fit(X, y)

    # Étape 3 : On note la version et on sauvegarde
    logger.info(f"saving model version: {__version__}")
    save_pipeline(pipeline_to_persist=price_pipe)

    # Message final de confirmation
    logger.info("Model trained and saved successfully")
    print("Modèle entraîné et sauvegardé avec succès !")


# Si on exécute ce fichier directement (et non en l'important), on lance l'entraînement
if __name__ == "__main__":
    run_training()