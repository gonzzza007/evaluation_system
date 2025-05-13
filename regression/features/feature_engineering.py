import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

def json_to_features(property_data: dict) -> pd.DataFrame:
    """Convert your property JSON to model features"""
    features = {
        'area': property_data['area'],
        'maakond': property_data['location']['maakond'],
        'soil_code': soil_to_numeric(property_data['location']['soil_type']),
        'water_distance': property_data['location']['water_features']['distance_to_water'],
        'avg_tree_age': sum(s['age'] for s in property_data['stands'])/len(property_data['stands']),
        # Add more feature extraction...
    }
    return pd.DataFrame([features])

def soil_to_numeric(soil_type: str) -> int:
    """Map soil types to ordinal values"""
    soil_rank = {
        'peat': 1,
        'sandy': 2,
        'clay': 3,
        'loam': 4
    }
    return soil_rank.get(soil_type.lower(), 0)