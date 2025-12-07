# regression_model/processing/__init__.py

"""
Ce dossier contient tout ce dont on a besoin pour préparer et vérifier nos données.

On y trouve :
- Des transformateurs pour nettoyer et modifier les données (prétraitement)
- Des fonctions pour vérifier que les données sont valides (validation)
- Des outils pour créer de nouvelles caractéristiques (ingénierie de variables)

Note importante :
On a fait le choix de ne pas importer automatiquement les modules ici.
Pourquoi ? Pour éviter les problèmes d'importation circulaire.

Comment les utiliser alors ?
Simplement en important directement depuis le module concerné :

    from regression_model.processing.preprocessors import CategoricalImputer
    from regression_model.processing.features import LogTransformer
    from regression_model.processing.validation import validate_inputs
"""