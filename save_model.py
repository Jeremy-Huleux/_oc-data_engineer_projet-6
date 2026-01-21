import bentoml
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

# --- 1. SÉLECTION DES DONNÉES (TOP 5) ---
# On reprend la stratégie TOP 5 : moins de variables = plus simple pour l'API
features_top_5 = [
    'PropertyGFATotal',
    'ENERGYSTARScore',
    'BuildingAge',
    'BuildingType',
    'Neighborhood'
]

# Récupération du csv
try:
    df_final = pd.read_csv("data_cleaned_final.csv")
    print(f"Données chargées : {df_final.shape}")
except FileNotFoundError:
    print("ERREUR : Le fichier 'data_cleaned_final.csv' est introuvable.")
    print("Avez-vous bien fait l'export to_csv() dans notebook ?")
    exit()

df_final['Neighborhood'] = df_final['Neighborhood'].str.upper()
X = df_final[features_top_5]
y = np.log1p(df_final['SiteEnergyUse(kBtu)']) # On n'oublie pas le Log !

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 2. CONSTRUCTION DU PIPELINE (LE TUNNEL) ---

# Le Morceau A : Le Trieur (Preprocessor)
preprocessor = make_column_transformer(
    (OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['BuildingType', 'Neighborhood']),
    (StandardScaler(), ['PropertyGFATotal', 'ENERGYSTARScore', 'BuildingAge'])
)

# Le Tunnel Complet : Random Forest optimisé
# On reprend les meilleurs hyperparamètres trouvés tout à l'heure grâce a GridSearch
model_pipeline = make_pipeline(
    preprocessor,
    RandomForestRegressor(
        n_estimators=200,      # Confirmé par GridSearch
        max_depth=10,          # Confirmé par GridSearch
        min_samples_leaf=4,    # Confirmé par GridSearch
        random_state=42
    )
)

# --- 3. ENTRÂINEMENT (.fit) ---
print("Entraînement du Pipeline en cours...")
model_pipeline.fit(X_train, y_train)
print("Pipeline entraîné avec succès ! ✅")

# --- 4. SAUVEGARDE DANS BENTOML 🍱 ---
# On sauvegarde tout le pipeline d'un coup.
# Pas besoin de séparer le preprocessor.

saved_model = bentoml.sklearn.save_model(
    "seattle_energy_pipeline",  # Le nom de l'API
    model_pipeline,             # On sauvegarde le tunnel entier
    signatures={
        "predict": {"batchable": False}
    }
)

print(f"Modèle sauvegardé : {saved_model}")