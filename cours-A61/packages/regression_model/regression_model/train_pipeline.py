## train_pipeline.py ##
import pathlib
from typing import List

import joblib
import pandas as pd

from regression_model.pipeline import price_pipe, PIPELINE_NAME

# Où se trouvent les choses sur notre machine #
PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"   # Dossier pour stocker les modèles finaux
DATASET_DIR = PACKAGE_ROOT / "datasets"              # Dossier avec nos jeux de données

# Les fichiers de données qu'on va utiliser #
TESTING_DATA_FILE = DATASET_DIR / "test.csv"    # Données pour tester plus tard
TRAINING_DATA_FILE = DATASET_DIR / "train.csv"  # Données pour l'entraînement

# Notre objectif : prédire le prix de vente
TARGET = "SalePrice"

# Toutes les caractéristiques des maisons qu'on prend en compte pour la prédiction #
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
    ## On Prend le pipeline tout entraîné et on le met de côté sur le disque pour pouvoir le réutiliser.###
    # On s'assure que le dossier existe, sinon on le crée
    TRAINED_MODEL_DIR.mkdir(exist_ok=True)
    
    # On choisit un nom de fichier et l'endroit où le sauvegarder
    save_file_name = f"{PIPELINE_NAME}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    
    # Sauvegarde !
    joblib.dump(pipeline_to_persist, save_path)


def run_training() -> None:
    ## C'est le cœur du script : on lit les données, on entraîne le modèle, et on le sauvegarde.###
    # Chargement des données d'entraînement
    data = pd.read_csv(TRAINING_DATA_FILE)

    # On sépare les caractéristiques (X) de ce qu'on veut prédire (y)
    X = data[FEATURES].copy()
    y = data[TARGET]

    # On lance l'entraînement du modèle
    price_pipe.fit(X, y)

    # On garde une copie du modèle entraîné pour plus tard
    save_pipeline(price_pipe)
    print("Modèle entraîné et sauvegardé avec succès !")


# Si on exécute ce fichier directement, on lance l'entraînement
if __name__ == "__main__":
    run_training()