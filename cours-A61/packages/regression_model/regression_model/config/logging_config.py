## logging_config.py ##
import logging


def get_console_handler() -> logging.Handler:
    """Crée un handler qui affiche les messages de log directement dans la console."""
    # Handler qui envoie les logs vers la sortie standard (console)
    console_handler = logging.StreamHandler()
    
    # On définit un format lisible pour nos messages
    # Exemple : "2023-12-01 14:30:00 — regression_model — INFO — Modèle chargé avec succès"
    formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
    )
    console_handler.setFormatter(formatter)
    
    return console_handler