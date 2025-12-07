## regression_model/processing/features.py ##

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class LogTransformer(BaseEstimator, TransformerMixin):
    """Applique une transformation logarithmique à des variables numériques."""

    def __init__(self, variables=None):
        # On doit obligatoirement savoir quelles colonnes transformer
        if variables is None:
            raise ValueError("Il faut préciser quelles variables transformer (liste 'variables').")
        # Pour plus de commodité, on accepte aussi bien une seule variable qu'une liste
        if not isinstance(variables, list):
            variables = [variables]
        self.variables = variables

    def fit(self, X: pd.DataFrame, y=None):
        # Cette transformation est purement mathématique, elle ne nécessite pas d'apprentissage
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for feature in self.variables:
            # np.log1p calcule log(1 + x), ce qui évite les erreurs avec les zéros
            X[feature] = np.log1p(X[feature])
        return X
