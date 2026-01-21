# 🏙️ Seattle Building Energy Prediction API

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![BentoML](https://img.shields.io/badge/Serving-BentoML-green)](https://www.bentoml.com/)
[![Docker](https://img.shields.io/badge/Deployment-Docker-blue)](https://www.docker.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange)](https://scikit-learn.org/)

> **Projet OpenClassrooms - Data Engineer (P6)**
> Prédiction de la consommation énergétique et des émissions de CO2 des bâtiments non-résidentiels de la ville de Seattle pour atteindre l'objectif "Neutralité Carbone 2050".

---

## 📋 Description du Projet

Ce projet déploie une **API de Machine Learning** capable de prédire la consommation annuelle d'énergie (`SiteEnergyUse(kBtu)`) d'un bâtiment en fonction de ses caractéristiques structurelles.

L'architecture repose sur une approche **MLOps** :
1.  **Exploration & Analyse** : Notebooks d'analyse exploratoire et de tests de modèles.
2.  **ETL Automatisé** : Nettoyage et transformation des données via scripts Python.
3.  **Optimisation** : Recherche des meilleurs hyperparamètres (GridSearch).
4.  **Mise en Production** : API REST sécurisée via BentoML et conteneurisée avec Docker.

---

## 📂 Architecture du Répertoire

```bash
Seattle-Energy-Prediction/
├── 📜 pyproject.toml                           # Gestion des dépendances (Poetry)
├── 📜 poetry.lock                              # Verrouillage des versions exactes
├── 📜 preprocess_data.py                       # Script ETL : Nettoyage et Feature Engineering
├── 📜 grid_search.py                           # Script : Recherche des meilleurs hyperparamètres
├── 📜 save_model.py                            # Script ML : Entraînement final et sauvegarde BentoML
├── 📜 service.py                               # Script API : Logique de l'API et Validation Pydantic
├── 📜 bentofile.yaml                           # Configuration de construction BentoML
├── 📓 template_modelistation_supervisee.ipynb  # Notebook d'analyse et modélisation
├── 📊 Projet Seattle.pptx                      # Support de présentation du projet
└── 📜 README.md                                # Documentation du projet

## ⚙️ Installation

Ce projet utilise **Poetry** pour la gestion des dépendances.

### 1. Cloner le projet

```bash
git clone https://github.com/Jeremy-Huleux/Seattle-Energy-Prediction.git
cd Seattle-Energy-Prediction
```

### 2. Installer l’environnement

```bash
poetry install
```

Cette commande :
- crée l’environnement virtuel
- installe toutes les dépendances (pandas, scikit-learn, bentoml, etc.)

---

## 🚀 Guide d’Utilisation (Pipeline MLOps)

Toutes les commandes doivent être exécutées avec **`poetry run`** afin d’utiliser l’environnement virtuel géré par Poetry.

---

### 1. Préparation des Données (ETL)

Nettoyage des données brutes, gestion des valeurs manquantes et feature engineering.

```bash
poetry run python preprocess_data.py
```

- **Input** : `2016_Building_Energy_Benchmarking.csv` (à placer à la racine)
- **Output** : `data_cleaned_final.csv`

---

### 2. Recherche d’Hyperparamètres (Optionnel)

```bash
poetry run python grid_search.py
```

---

### 3. Entraînement du Modèle

Entraînement du modèle final (**RandomForest**) et sauvegarde dans le **BentoML Model Store**.

```bash
poetry run python save_model.py
```

---

### 4. Lancement de l’API (Mode Développement)

```bash
poetry run bentoml serve service:SeattleEnergyService --reload
```

📍 **Swagger UI** :  
👉 http://localhost:3000

---

## 🐳 Déploiement Docker

### 1. Construire le Bento

```bash
poetry run bentoml build
```

📌 Notez le **TAG généré** (ex : `seattle_energy_service:xyz123`).

---

### 2. Créer l’image Docker

```bash
poetry run bentoml containerize seattle_energy_service:VOTRE_TAG
```

---

### 3. Lancer le conteneur

```bash
docker run --rm -p 3000:3000 seattle_energy_service:VOTRE_TAG
```

---

## 🔌 Documentation de l’API

### Endpoint

```http
POST /predict
```

### Exemple de requête (JSON)

```json
{
  "input_data": {
    "PropertyGFATotal": 45000,
    "ENERGYSTARScore": 85,
    "YearBuilt": 1998,
    "BuildingType": "NonResidential",
    "Neighborhood": "DOWNTOWN"
  }
}
```

### Exemple de réponse (JSON)

```json
{
  "prediction_kbtu": 1250430.55
}
```

---

## 👤 Auteur

**Jeremy Huleux**  
Data Engineer Student @ OpenClassrooms