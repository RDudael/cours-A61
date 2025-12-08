## config.py ##
import logging.config
from pathlib import Path

# Détermination du dossier racine du package ml_api
# (on remonte de deux niveaux depuis ce fichier)
PACKAGE_ROOT = Path(__file__).resolve().parent.parent

# Chemin du dossier pour les fichiers de log
LOG_DIR = PACKAGE_ROOT / "logs"
# Création du dossier s'il n'existe pas déjà
LOG_DIR.mkdir(exist_ok=True)

# Configuration centralisée du système de logs
# Utiliser dictConfig est la méthode recommandée par Python
LOGGING_CONFIG = {
    "version": 1,  # Version obligatoire du schéma
    "disable_existing_loggers": False,  # On ne désactive pas les loggers existants
    
    # Formats disponibles pour les messages de log
    "formatters": {
        "standard": {
            "format": "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
        },
    },
    
    # Handlers : où envoyer les logs
    "handlers": {
        "console": {  # Affichage dans le terminal/console
            "class": "logging.StreamHandler",
            "level": "INFO",  # Niveau minimal : INFO
            "formatter": "standard",
        },
        "file": {  # Écriture dans un fichier
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": str(LOG_DIR / "ml_api.log"),  # Fichier de log principal
        },
    },
    
    # Configuration des loggers spécifiques
    "loggers": {
        "ml_api": {  # Logger principal de notre API
            "handlers": ["console", "file"],  # Utilise les deux handlers
            "level": "INFO",  # Niveau global pour ce logger
            "propagate": False,  # Ne pas propager aux loggers parents
        },
    },
}


def configure_logging() -> None:
    """
    Applique la configuration du logging à l'ensemble de l'application.
    
    Cette fonction doit être appelée au démarrage de l'API
    pour que tous les modules bénéficient de la même configuration.
    """
    logging.config.dictConfig(LOGGING_CONFIG)