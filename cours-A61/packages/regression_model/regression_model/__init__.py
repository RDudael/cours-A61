# regression_model/__init__.py

from pathlib import Path
from .logging_config import get_logger

# Dossier racine du package regression_model
PACKAGE_ROOT = Path(__file__).resolve().parent

# Fichier de version (ton fichier s'appelle bien VERSION.txt)
VERSION_PATH = PACKAGE_ROOT / "VERSION.txt"

with open(VERSION_PATH, "r") as version_file:
    __version__ = version_file.read().strip()

# Logger global du package
logger = get_logger("regression_model")

__all__ = ["logger", "__version__"]
