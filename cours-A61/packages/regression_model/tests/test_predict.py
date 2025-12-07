## tests/test_predict.py ##
import pandas as pd

from regression_model.train_pipeline import TESTING_DATA_FILE
from regression_model.predict import make_prediction


def test_make_prediction_returns_right_shape():
    # Préparation : on charge le jeu de données de test complet
    test_data = pd.read_csv(TESTING_DATA_FILE)
    # Pour ce test, on prend juste les 5 premières maisons
    input_data = test_data.iloc[:5, :]

    # Action : on demande une prédiction pour ces 5 maisons
    result = make_prediction(input_data)
    preds = result["predictions"]   # Les prix estimés
    errors = result["errors"]       # Les problèmes éventuels

    # Vérifications :
    # 1. Tout d'abord, on vérifie qu'il n'y a pas eu d'erreur de validation
    #    (les données de test sont censées être propres)
    assert errors == {}
    # 2. On s'assure qu'on a bien reçu des prédictions (pas un "None")
    assert preds is not None
    # 3. On vérifie qu'on a exactement 5 prédictions pour 5 maisons
    assert len(preds) == len(input_data)


def test_validation_missing_column_generates_error():
    # Préparation : cette fois, on simule une erreur courante
    # On charge les données, puis on supprime délibérément une colonne importante
    test_data = pd.read_csv(TESTING_DATA_FILE)
    input_data = test_data.iloc[:5, :].copy()
    input_data.drop("MSSubClass", axis=1, inplace=True)  # Colonne manquante !

    # Action : on essaie quand même de faire une prédiction
    result = make_prediction(input_data)
    preds = result["predictions"]
    errors = result["errors"]

    # Vérifications :
    # 1. Étant donné qu'il manque une colonne, on ne devrait PAS obtenir de prédictions
    assert preds is None
    # 2. Par contre, on DOIT avoir un message d'erreur qui nous dit ce qui ne va pas
    assert "missing_columns" in errors
    # 3. Et cette erreur doit bien mentionner la colonne manquante ("MSSubClass")
    assert "MSSubClass" in errors["missing_columns"]