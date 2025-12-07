from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor  
from regression_model import preprocessors as pp

CATEGORICAL_VARS = [
    "MSZoning",
    "Neighborhood",
    "GarageType",
    "GarageFinish",
    "PavedDrive",
]

price_pipe = Pipeline(
    [
        ("categorical_imputer", pp.CategoricalImputer(variables=CATEGORICAL_VARS)),
        # Final estimator MUST have .predict()
        ("model", DummyRegressor(strategy="mean")),
    ]
)

PIPELINE_NAME = "regression_model"