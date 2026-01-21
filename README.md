# 🏙️ Seattle Building Energy Prediction API

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![BentoML](https://img.shields.io/badge/Serving-BentoML-green)](https://www.bentoml.com/)
[![Docker](https://img.shields.io/badge/Deployment-Docker-blue)](https://www.docker.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange)](https://scikit-learn.org/)

> **Projet OpenClassrooms - Data Engineer (P6)**
> Prédiction de la consommation énergétique et des émissions de CO2 des bâtiments non-résidentiels de la ville de Seattle pour atteindre l'objectif "Neutralité Carbone 2050".

---

## 📋 Description du Projet

Ce projet déploie une **API de Machine Learning** capable de prédire la consommation annuelle d'énergie (`SiteEnergyUse(kBtu)`) d'un bâtiment en fonction de ses caractéristiques structurelles.

L'architecture repose sur une approche **MLOps** :
1.  **ETL Automatisé** : Nettoyage et transformation des données brutes.
2.  **Modélisation** : Entraînement d'un `RandomForestRegressor` optimisé.
3.  **Mise en Production** : API REST sécurisée via BentoML et conteneurisée avec Docker.

---

## 📂 Architecture du Répertoire

```bash
Seattle-Energy-Prediction/
├── 📜 preprocess_data.py       # Script ETL : Nettoyage et Feature Engineering
├── 📜 save_model.py            # Script ML : Entraînement et sauvegarde BentoML
├── 📜 service.py               # Script API : Logique de l'API et Validation Pydantic
├── 📜 bentofile.yaml           # Configuration de construction BentoML
├── 📜 requirements.txt         # Dépendances Python
└── 📜 README.md                # Documentation du projet