## tests/test_predict.py ##
import pandas as pd

from regression_model.train_pipeline import TESTING_DATA_FILE
from regression_model.predict import make_prediction


def test_make_prediction_returns_right_shape():
    # On se prépare : on charge les données de test qu'on a mises de côté
    test_data = pd.read_csv(TESTING_DATA_FILE)
    # Pour ce test, on prend juste les 5 premières maisons
    input_data = test_data.iloc[:5, :]

    # Action : on demande au modèle de prédire les prix de ces maisons
    result = make_prediction(input_data)
    preds = result["predictions"]

    # Vérifications :
    # 1. Est-ce qu'on a bien reçu des prédictions (et pas "None") ?
    assert preds is not None
    # 2. Est-ce qu'on a autant de prédictions que de maisons en entrée ?
    assert len(preds) == len(input_data)