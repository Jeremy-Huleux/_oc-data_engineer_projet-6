import bentoml
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# --- 1. ENUMS ---
class NeighborhoodEnum(str, Enum):
    # Liste fusionnée majuscules
    DOWNTOWN = "DOWNTOWN"
    SOUTHEAST = "SOUTHEAST"
    NORTHEAST = "NORTHEAST"
    EAST = "EAST"
    CENTRAL = "CENTRAL"
    NORTH = "NORTH"
    MAGNOLIA_QUEEN_ANNE = "MAGNOLIA / QUEEN ANNE"
    LAKE_UNION = "LAKE UNION"
    GREATER_DUWAMISH = "GREATER DUWAMISH"
    BALLARD = "BALLARD"
    NORTHWEST = "NORTHWEST"
    SOUTHWEST = "SOUTHWEST"
    DELRIDGE = "DELRIDGE"
    DELRIDGE_NEIGHBORHOODS = "DELRIDGE NEIGHBORHOODS"

class BuildingTypeEnum(str, Enum):
    # la liste filtrée
    NonResidential = "NonResidential"
    Nonresidential_COS = "Nonresidential COS"
    SPS_District_K12 = "SPS-District K-12"
    Campus = "Campus"
    Nonresidential_WA = "Nonresidential WA"

# --- 2. INPUT COMPLET ---
class BuildingInput(BaseModel):
    # Feature 1 : La Surface
    PropertyGFATotal: float = Field(gt=0, description="Surface Totale (pieds carrés)")
    
    # Feature 2 : Le Score
    ENERGYSTARScore: float = Field(ge=0, le=100, description="Score Énergétique")
    
    # Feature 3 (Indirect) : L'Année (pour calculer l'âge)
    YearBuilt: int = Field(gt=1900, le=2050, description="Année de construction")
    
    # Feature 4 : Le Type
    BuildingType: BuildingTypeEnum
    
    # Feature 5 : Le Quartier
    Neighborhood: NeighborhoodEnum

@bentoml.service(name="seattle_energy_service")
class SeattleEnergyService:
    def __init__(self):
        model_ref = bentoml.sklearn.get("seattle_energy_pipeline:latest")
        self.pipeline = model_ref.load_model()

    @bentoml.api
    def predict(self, input_data: BuildingInput) -> dict:
        data = input_data.dict()
        
        # --- TRAITEMENT ---
        
        # 1. Calcul de l'Âge (Feature 3)
        # On utilise 2016 pour rester cohérent avec l'entrainement, ou l'année actuelle.
        # Si ton modèle a appris "Age en 2016", il faut idéalement garder cette logique ou réentraîner.
        # Pour l'API temps réel, souvent on prend l'année en cours :
        current_year = datetime.now().year
        age = current_year - data['YearBuilt']
        if age < 0: age = 0
            
        # 2. Majuscule Quartier (Feature 5)
        neighborhood = data['Neighborhood'].value.upper()

        # --- DATAFRAME (Strictement 5 colonnes) ---
        input_df = pd.DataFrame([{
            'PropertyGFATotal': data['PropertyGFATotal'],
            'ENERGYSTARScore': data['ENERGYSTARScore'],
            'BuildingAge': age,
            'BuildingType': data['BuildingType'].value,
            'Neighborhood': neighborhood
        }])
        
        # --- PREDICTION ---
        log_pred = self.pipeline.predict(input_df)
        pred = np.expm1(log_pred)
        
        return {"prediction_kbtu": round(pred[0], 2)}