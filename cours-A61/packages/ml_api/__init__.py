## Package ml_api : REST API pour servir le modèle regression_model.##
from pathlib import Path

# Détermination du dossier racine du package ml_api
# Utile pour construire des chemins relatifs fiables
PACKAGE_ROOT = Path(__file__).resolve().parent

# Lecture du numéro de version de l'API depuis un fichier dédié
# Cette approche facilite la gestion des versions (CI/CD, déploiements)
with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()
