## regression_model/pipeline.py ##
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Lasso

from regression_model.processing.preprocessors import (CategoricalImputer, NumericalImputer, LogTransformer, SimpleCategoricalEncoder,)

# Variables catégorielles qui ont parfois des valeurs manquantes
# On va remplacer ces NaN par "Missing"
CATEGORICAL_VARS = [
    "MSZoning",
    "Neighborhood",
    "RoofStyle",
    "MasVnrType",
    "BsmtQual",
    "BsmtExposure",
    "HeatingQC",
    "CentralAir",
    "KitchenQual",
    "FireplaceQu",
    "GarageType",
    "GarageFinish",
    "PavedDrive",
]

# Variables numériques qu'on transforme avec un logarithme
# Ça aide souvent à mieux modéliser ce genre de données
LOG_VARS = [
    "LotFrontage",   # distance entre la maison et la rue
    "LotArea",       # surface totale du terrain
    "GrLivArea",     # surface habitable (salle de séjour)
    "1stFlrSF",      # surface du premier étage
    "TotalBsmtSF",   # surface totale du sous-sol
]

# Un nom simple pour identifier notre pipeline sauvegardé
PIPELINE_NAME = "lasso_regression"

# Notre chaîne de traitement complète, étape par étape
price_pipe = Pipeline(
    [
        # 1. Nettoyage des variables catégorielles (remplacement des NaN)
        ("categorical_imputer", CategoricalImputer(variables=CATEGORICAL_VARS)),
        
        # 2. Nettoyage des variables numériques (remplacement des NaN par la médiane)
        #    Note : si on ne précise pas de variables, il prend toutes les colonnes numériques
        ("numerical_imputer", NumericalImputer()),
        
        # 3. Transformation logarithmique sur certaines variables
        ("log_transformer", LogTransformer(variables=LOG_VARS)),
        
        # 4. Conversion des variables texte en nombres
        #    (indispensable pour que le modèle puisse les utiliser)
        ("categorical_encoder", SimpleCategoricalEncoder()),
        
        # 5. Le modèle de prédiction final (régression Lasso)
        ("model", Lasso(alpha=0.005, random_state=0)),
    ]
)