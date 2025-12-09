# packages/ml_api/api/validation.py

from marshmallow import Schema, fields


class PredictionResultSchema(Schema):
    """
    Schéma de validation pour la réponse JSON de notre API de prédiction.
    
    Ce schéma garantit que les réponses de l'API respectent toujours
    le même format, ce qui facilite :
    - L'intégration avec d'autres services
    - La détection rapide des problèmes
    - La documentation automatique
    
    Structure attendue :
    {
        "predictions": [12.5, 24.8, 30.1, ...],  # Liste des prix estimés
        "version": "0.1.0",                      # Version du modèle utilisé
        "errors": null                           # Aucune erreur (ou dict si problème)
    }
    """

    predictions = fields.List(
        fields.Float(),  # Chaque prédiction doit être un nombre décimal
        required=True    # Ce champ est obligatoire dans la réponse
    )
    version = fields.String(required=True)  # La version doit être une chaîne de caractères
    # On autorise deux formats pour les erreurs :
    # - None (null en JSON) lorsqu'il n'y a pas d'erreur
    # - Un dictionnaire contenant les détails des erreurs
    errors = fields.Raw(allow_none=True, required=True)