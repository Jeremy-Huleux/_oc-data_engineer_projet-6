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