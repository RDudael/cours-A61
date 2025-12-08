## regression_model/processing/preprocessors.py ##

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CategoricalImputer(BaseEstimator, TransformerMixin):
    ## Remplit les valeurs manquantes dans les variables catégorielles.##

    def __init__(self, variables=None):
        # On accepte une seule variable (string) ou une liste
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X: pd.DataFrame, y=None):
        # Aucun calcul à faire pendant l'apprentissage
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        # Pour chaque colonne catégorielle, on remplace les NaN par "Missing"
        for feature in self.variables:
            X[feature] = X[feature].fillna("Missing")
        return X


class NumericalImputer(BaseEstimator, TransformerMixin):
    
    ## Remplit les valeurs manquantes dans les variables numériques.
    ## Astuce : si on ne précise pas de variables, il prend automatiquement
    ## toutes les colonnes numériques du jeu de données.
    

    def __init__(self, variables=None):
        self.variables = variables

    def fit(self, X: pd.DataFrame, y=None):
        X = X.copy()

        # Mode automatique : détection de toutes les colonnes numériques
        if self.variables is None:
            self.variables_ = X.select_dtypes(include=["number"]).columns.tolist()
        else:
            self.variables_ = self.variables

        # Pour chaque variable, on calcule et mémorise la médiane
        # (plus robuste que la moyenne face aux valeurs extrêmes)
        self.imputer_dict_ = {}
        for feature in self.variables_:
            self.imputer_dict_[feature] = X[feature].median()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        # Application : on remplace chaque NaN par la médiane calculée précédemment
        for feature in self.variables_:
            X[feature] = X[feature].fillna(self.imputer_dict_[feature])
        return X


class LogTransformer(BaseEstimator, TransformerMixin):
    ## Applique une transformation logarithmique à des variables numériques.##

    def __init__(self, variables=None):
        # On accepte une seule variable (string) ou une liste
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X: pd.DataFrame, y=None):
        # Transformation purement mathématique, pas d'apprentissage
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for feature in self.variables:
            # On s'assure que c'est un nombre, on coupe à 0 (pas de valeurs négatives)
            # et on applique log(1 + x) pour gérer les zéros
            X[feature] = np.log1p(X[feature].astype(float).clip(lower=0))
        return X


class SimpleCategoricalEncoder(BaseEstimator, TransformerMixin):
    
    ## Convertit les variables textuelles en nombres (encodage).
    ## Deux façons de l'utiliser :
    ## - Sans spécifier de variables : il traite toutes les colonnes de type texte
    ##- Avec une liste : il ne traite que les colonnes mentionnées
    

    def __init__(self, variables=None):
        self.variables = variables

    def fit(self, X: pd.DataFrame, y=None):
        X = X.copy()

        # Mode automatique : détection des colonnes texte
        if self.variables is None:
            self.variables_ = [col for col in X.columns if X[col].dtype == "O"]
        else:
            self.variables_ = self.variables

        # Construction du dictionnaire d'encodage pour chaque variable
        self.encoder_dict_ = {}
        for feature in self.variables_:
            # On récupère toutes les valeurs uniques (même les NaN convertis en "nan")
            categories = X[feature].astype(str).unique()
            # Chaque catégorie reçoit un numéro unique
            self.encoder_dict_[feature] = {
                cat: idx for idx, cat in enumerate(categories)
            }

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for feature in self.variables_:
            encoder = self.encoder_dict_[feature]
            # Conversion : texte → nombre correspondant
            X[feature] = (
                X[feature]
                .astype(str)               # Conversion en texte pour être sûr
                .map(encoder)              # Remplacement par le numéro (si connu)
                .fillna(-1)                # -1 pour les nouvelles catégories
            )
        return X