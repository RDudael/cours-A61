class BaseError(Exception):
    """Classe de base pour toutes les erreurs personnalisées de notre package."""


class InvalidModelInputError(BaseError):
    """Erreur spécifique quand les données fournies au modèle ne sont pas valides."""
    pass