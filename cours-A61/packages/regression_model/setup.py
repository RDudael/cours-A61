## Setup.py ##
from pathlib import Path
from setuptools import setup, find_packages

# Lecture de la version depuis un fichier dédié
# (plus pratique que de la coder en dur, surtout pour les mises à jour)
VERSION_PATH = Path(__file__).resolve().parent / "regression_model" / "VERSION.txt"
with open(VERSION_PATH, "r") as version_file:
    __version__ = version_file.read().strip()

# Configuration de notre package pour pip/setuptools
setup(
    name="regression_model",
    version=__version__,  # Utilise la version lue depuis le fichier
    description="Modèle de régression pour prédire le prix des maisons (cours A61)",
    
    # Détection automatique de tous les packages Python dans le projet
    packages=find_packages(),
    
    # Inclut les fichiers de données non-Python (comme VERSION.txt)
    include_package_data=True,
    
    # Liste des dépendances nécessaires au fonctionnement du modèle
    install_requires=[
        "numpy",        # Calculs numériques
        "pandas",       # Manipulation de données tabulaires
        "scikit-learn", # Machine Learning (modèles et pipelines)
        "joblib",       # Sauvegarde/chargement des modèles
    ],
    
    # Version minimale de Python requise
    python_requires=">=3.9",)