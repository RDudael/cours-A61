# regression_model/__init__.py

from pathlib import Path
import logging

from regression_model.config import logging_config

# Détermination du chemin racine de notre package
PACKAGE_ROOT = Path(__file__).resolve().parent
# Emplacement du fichier contenant le numéro de version
VERSION_PATH = PACKAGE_ROOT / "VERSION"

# Lecture du numéro de version depuis le fichier
# (plus pratique que de le coder en dur, surtout pour le CI/CD)
try:
    with open(VERSION_PATH, "r") as version_file:
        __version__ = version_file.read().strip()
except FileNotFoundError:
    # Si le fichier VERSION n'existe pas (environnement de développement local par exemple),
    # on utilise une valeur par défaut pour éviter de planter
    __version__ = "0.1.0"

# Configuration du logger central du package
# Tous les modules pourront l'utiliser en important 'logger'
logger = logging.getLogger("regression_model")
# Niveau de base : on veut voir les messages INFO et plus critiques
logger.setLevel(logging.INFO)
# On utilise notre configuration centralisée pour l'affichage console
logger.addHandler(logging_config.get_console_handler())
# On désactive la propagation pour garder un contrôle total sur les logs
logger.propagate = False