import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

# 1. Chargement (Comme d'hab)
df = pd.read_csv("features.csv")
features = ['PropertyGFATotal', 'ENERGYSTARScore', 'BuildingAge', 'BuildingType', 'Neighborhood']
X = df[features]
y = np.log1p(df['SiteEnergyUse(kBtu)'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Le Pipeline SANS les hyperparamètres fixés
preprocessor = make_column_transformer(
    (OneHotEncoder(handle_unknown='ignore'), ['BuildingType', 'Neighborhood']),
    (StandardScaler(), ['PropertyGFATotal', 'ENERGYSTARScore', 'BuildingAge'])
)

pipeline = make_pipeline(preprocessor, RandomForestRegressor(random_state=42))

# 3. La Grille de Recherche (Le Menu des Tests)
# On va tester toutes ces combinaisons :
param_grid = {
    'randomforestregressor__n_estimators': [100, 200, 300], # Nombre d'arbres
    'randomforestregressor__max_depth': [10, 20, None],     # Profondeur max
    'randomforestregressor__min_samples_leaf': [1, 2, 4]    # Minimum par groupe
}

# 4. Lancement de la recherche
print("Recherche des meilleurs paramètres en cours...")
grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1)
grid_search.fit(X_train, y_train)

# 5. Résultat
print("\n🏆 MEILLEURS PARAMÈTRES TROUVÉS :")
print(grid_search.best_params_)
print(f"Meilleur score : {grid_search.best_score_}")