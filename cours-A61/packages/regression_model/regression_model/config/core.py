# regression_model/config/core.py

from pathlib import Path
from dataclasses import dataclass


# ---- Chemins de base du package ----
# Détermination des chemins importants une fois pour toutes
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PACKAGE_ROOT / "datasets"           # Dossier des jeux de données
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models" # Dossier des modèles sauvegardés
VERSION_FILE_PATH = PACKAGE_ROOT / "VERSION.txt"   # Fichier contenant la version


# ---- Config de l'application ----

@dataclass
class AppConfig:
    
    ## Configuration principale de l'application.
    
    ## Contient les paramètres qui pourraient changer selon l'environnement
    ## (développement, test, production) ou les besoins.
    
    package_name: str          # Nom de notre package
    training_data_file: str    # Nom du fichier d'entraînement
    test_data_file: str        # Nom du fichier de test
    pipeline_name: str         # Nom du pipeline (pour le fichier .pkl)


@dataclass
class Config:
    
    ## Conteneur racine pour toute la configuration.
    ## Permet d'organiser la configuration par sections
    ## (app_config, model_config, etc.) si besoin d'extension.
    
    app_config: AppConfig


def create_and_validate_config() -> Config:
    
    ## Crée et valide la configuration de l'application.
    ## Pour simplifier, on utilise des valeurs en dur plutôt qu'un fichier YAML.
    ## Cette approche est plus simple pour un projet de taille modeste.
    
    app_cfg = AppConfig(
        package_name="regression_model",    # Notre package
        training_data_file="train.csv",     # Fichier pour l'entraînement
        test_data_file="test.csv",          # Fichier pour les tests
        pipeline_name="lasso_regression",   # Nom de notre pipeline
    )

    # Validation basique pourrait être ajoutée ici si besoin
    # (vérifier que les fichiers existent, etc.)

    return Config(app_config=app_cfg)


# Instance globale de configuration
# C'est cet objet qu'on importe dans tout le code :
#   from regression_model.config.core import config
config = create_and_validate_config()