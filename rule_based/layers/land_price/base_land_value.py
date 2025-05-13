# layers/land_price/base_land_value.py
from models.property import Property

def base_land_value(property: Property) -> float:
    """Calculate base land value (normalized 0-1)"""
    # This could be based on location, historical prices, etc.
    # Simplified example - in reality would use more complex logic
    base_value = 0.5  # Default base value
    
    # Adjust based on region
    if property.location.maakond in ["37", "39"]:  # More valuable regions
        base_value *= 1.2
    elif property.location.maakond in ["44", "45"]:  # Less valuable
        base_value *= 0.8
    
    # Normalize to 0-1 range
    return min(max(base_value, 0), 1)