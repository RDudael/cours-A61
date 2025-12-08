# regression_model/logging_config.py

import logging
import sys

# Format standard pour tous nos messages de log
# Inclut : timestamp, nom du logger, niveau de log, message
LOG_FORMAT = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"


def get_logger(logger_name: str) -> logging.Logger:
    """
    Crée et configure un logger pour une partie spécifique du projet.
    
    Cette fonction centralise la configuration des logs pour garantir
    une cohérence dans tout le package regression_model.
    
    Args:
        logger_name: Le nom du logger (ex: "regression_model.predict")
        
    Returns:
        Un logger configuré et prêt à l'emploi
    """
    # Récupération ou création du logger
    logger = logging.getLogger(logger_name)

    # Vérification qu'on ne configure pas plusieurs fois le même logger
    # (cela éviterait d'avoir des messages en double)
    if not logger.handlers:
        # Handler qui envoie les logs vers la sortie standard (console)
        handler = logging.StreamHandler(sys.stdout)
        
        # Application de notre format personnalisé
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)

        # Association du handler au logger
        logger.addHandler(handler)
        
        # Définition du niveau de log (INFO = messages informatifs et plus critiques)
        logger.setLevel(logging.INFO)
        
        # Désactivation de la propagation pour un contrôle total
        logger.propagate = False

    return logger