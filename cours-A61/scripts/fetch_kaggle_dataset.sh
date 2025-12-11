#!/usr/bin/env bash
set -e  # Arrête le script immédiatement si une commande échoue

echo "=== Script de récupération du dataset Kaggle ==="
echo "Répertoire courant (dans le script) :"
pwd

# Dossier où seront stockées les données
# On s'assure que ce dossier existe (le crée si nécessaire)
DATA_DIR="packages/regression_model/regression_model/datasets"
mkdir -p "$DATA_DIR"

echo "Téléchargement du dataset Kaggle dans : $DATA_DIR"

# Utilisation de l'API Kaggle pour télécharger le dataset
# Les identifiants Kaggle doivent être dans les variables d'environnement :
# KAGGLE_USERNAME et KAGGLE_KEY
kaggle competitions download \
  -c house-prices-advanced-regression-techniques \
  -p "$DATA_DIR"

echo "Décompression du fichier zip…"
# Extraction des fichiers avec l'option -o pour écraser si ils existent déjà
unzip -o "$DATA_DIR/house-prices-advanced-regression-techniques.zip" -d "$DATA_DIR"

echo "Contenu du dossier de données :"
# Affichage détaillé des fichiers téléchargés
ls -l "$DATA_DIR"

echo "=== Fin du script fetch_kaggle_dataset.sh ==="