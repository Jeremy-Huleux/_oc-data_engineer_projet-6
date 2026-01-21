import pandas as pd
import numpy as np

def process_raw_data(input_file: str, output_file: str):
    print(f"🔄 Chargement : {input_file}...")
    df = pd.read_csv(input_file)
    
    # 1. FILTRAGE BATIMENTS
    filtre_types = [
        'NonResidential', 'Nonresidential COS',
        'Nonresidential WA', 'Campus', 'SPS-District K-12'
    ]
    df = df[df['BuildingType'].isin(filtre_types)].copy()
    print(f"✅ Filtrage types : {df.shape[0]} lignes restantes")

    # 2. GESTION DES OUTLIERS OFFICIELS
    # On supprimes si la colonne 'Outlier' contient quelque chose
    if 'Outlier' in df.columns: #On vérifie si la colonne existe dans le fichier
        df = df[df['Outlier'].isna()]#On garde que les lignes ou Outlier est vide (NaN)
    
    # 3. NETTOYAGE COLONNES VIDES & INUTILES
    cols_to_drop = [
        'Comments', 'YearsENERGYSTARCertified', 'ThirdLargestPropertyUseType', 
        'ThirdLargestPropertyUseTypeGFA', 'Outlier', '2015', 'City', 'State',
        'ZipCode', 'TaxParcelIdentificationNumber', 'CouncilDistrictCode',
        'Latitude', 'Longitude', 'DefaultData', 'ComplianceStatus',
        'ListOfAllPropertyUseTypes', 'LargestPropertyUseType', 'SecondLargestPropertyUseType',
        'SiteEUI(kBtu/sf)', 'SiteEUIWN(kBtu/sf)', 'SourceEUI(kBtu/sf)', 'SourceEUIWN(kBtu/sf)',
        'SiteEnergyUseWN(kBtu)', 'SteamUse(kBtu)', 'Electricity(kWh)', 'Electricity(kBtu)',
        'NaturalGas(therms)', 'NaturalGas(kBtu)', 'TotalGHGEmissions', 'GHGEmissionsIntensity',
        'LargestPropertyUseTypeGFA', 'SecondLargestPropertyUseTypeGFA'
    ]
    # On ne supprime que ce qui existe
    existing_drops = [c for c in cols_to_drop if c in df.columns] #Compréhension de liste
    #La même chose que :
    #existing_drops = []                # 1. On crée une liste vide
    #for c in cols_to_drop:             # 2. On boucle sur ta liste de choses à supprimer
    #   if c in df.columns:             # 3. On vérifie : Est-ce que cette colonne existe vraiment ?
    #      existing_drops.append(c)     # 4. Si oui, on l'ajoute à la liste finale
    df.drop(columns=existing_drops, inplace=True)

    # 4. IMPUTATION INTELLIGENTE
    print("🧠 Imputation ENERGYSTARScore par type...")
    if 'ENERGYSTARScore' in df.columns:
        # Calcul de la médiane par type
        medianes = df.groupby('PrimaryPropertyType')['ENERGYSTARScore'].transform('median')
        # Remplissage
        df['ENERGYSTARScore'] = df['ENERGYSTARScore'].fillna(medianes)
        # S'il reste des trous, médiane globale
        df['ENERGYSTARScore'] = df['ENERGYSTARScore'].fillna(df['ENERGYSTARScore'].median())

    # 5. FEATURE ENGINEERING
    print("⚙️ Création des variables...")
    
    # BuildingAge (Basé sur 2016)
    df['BuildingAge'] = 2016 - df['YearBuilt']
    df['BuildingAge'] = df['BuildingAge'].apply(lambda x: x if x >= 0 else 0)
                                    #On applique a toutes les lignes : Si >= 0 on garde sinon on remplace par 0
    # Age_Category
    # On utilise qcut
    df['Age_Category'] = pd.qcut(df['BuildingAge'], q=4, labels=['Very Recent', 'Recent', 'Old', 'Very Old'])

    # 6. NETTOYAGE QUARTIERS (Doublons)
    df['Neighborhood'] = df['Neighborhood'].str.upper()

    # 7. Nettoyage de la TARGET (On prépare la cible)
    print("🎯 Nettoyage de la Target (SiteEnergyUse)...")
    
    # 7.1 On retire les lignes où la réponse est vide (NaN)
    df = df.dropna(subset=['SiteEnergyUse(kBtu)'])
    # 7.2 On retire les valeurs négatives ou nulles (impossible physiquement + bug avec le Log)
    df = df[df['SiteEnergyUse(kBtu)'] > 0]

    # 8. SAUVEGARDE
    print(f"💾 Sauvegarde : {output_file} ({df.shape})")
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    process_raw_data("2016_Building_Energy_Benchmarking.csv", "data_cleaned_final.csv")