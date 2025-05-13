# layers/land_price/soil_adjustment.py
from models.property import Property

SOIL_COEFFICIENTS = {
    "peat": 0.7,
    "sandy": 0.9,
    "clay": 1.1,
    "loam": 1.3,
    "rocky": 0.5
}

def soil_adjustment(property: Property) -> float:
    """Adjust value based on soil type (normalized 0-1)"""
    soil_type = property.location.soil_type.lower()
    coefficient = SOIL_COEFFICIENTS.get(soil_type, 1.0)
    
    # Normalize to our target range
    min_coeff = min(SOIL_COEFFICIENTS.values())
    max_coeff = max(SOIL_COEFFICIENTS.values())
    return (coefficient - min_coeff) / (max_coeff - min_coeff)