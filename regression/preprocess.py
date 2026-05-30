import sys
import sqlite3
import pandas as pd
from pathlib import Path
import argparse
from typing import Dict, Any

sys.path.append(str(Path(__file__).parent.parent))
from tools.various import string_cleanup, normalize_date, get_xml_data
from tools.soil_type import get_soil_type


def fetch_properties_from_db(db_path: Path) -> Dict[str, Any]:
    """Fetch property data from SQLite database"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()
    
    # Fetch basic property info
    cursor.execute("""
        SELECT cadastral_nr, area, county, added_on, price
        FROM properties
        WHERE hidden = 0 AND price > 1000 AND area > 1000
          AND (county IS NOT NULL) AND (TRIM(county) != '') AND (TRIM(county) != 'N/A')
    """)
    properties = cursor.fetchall()
    
    # Fetch stands for each property
    property_data = {}
    for prop in properties:
        cadaster_nr = prop['cadastral_nr']

        xml_data = get_xml_data(cadaster_nr)

        if not xml_data['no_data']:
            soil = get_soil_type(xml_data['epsg_x'], xml_data['epsg_y']) or {}

            property_data[cadaster_nr] = {
                'cadaster_nr': cadaster_nr,
                'area': prop['area'],
                'maakond': prop['county'],
                'sale_date': prop['added_on'],
                'epsg_x': xml_data['epsg_x'],
                'epsg_y': xml_data['epsg_y'],
                'soilbodylabel': soil.get('soilbodylabel'),
                'soil_profile': soil.get('soil_profile'),
                'soil_mod': soil.get('soil_mod'),
                'price': prop['price'],
        }
    
    conn.close()
    return property_data

def process_to_dataframe(property_data: Dict[str, Any]) -> pd.DataFrame:
    """Convert raw property data to processed DataFrame"""
    records = []
    for cadaster, data in property_data.items():
        # if not data['stands']:
            # continue  # Skip properties with no stands
            
        records.append({
            'area': data['area'],
            'maakond': string_cleanup(data['maakond']),
            'sale_date': normalize_date(data['sale_date']),
            'epsg_x': data['epsg_x'],
            'epsg_y': data['epsg_y'],
            'soilbodylabel': data['soilbodylabel'],
            'soil_profile': data['soil_profile'],
            'soil_mod': data['soil_mod'],
            'price': data['price'],
        })
    return pd.DataFrame(records)

def main():
    parser = argparse.ArgumentParser(description='Process property data from SQLite to training CSV/PARQUET')
    # args = parser.parse_args()

    
    # Configure paths
    DB_PATH = Path("../metsad.sqlite")
    OUTPUT_PATH = Path("data")

    # Process data
    print(f"Loading data from {DB_PATH}...")
    property_data = fetch_properties_from_db(DB_PATH)
    df = process_to_dataframe(property_data)
    df.to_csv(OUTPUT_PATH / "training_data.csv", index=False)
    df.to_parquet(OUTPUT_PATH / "training_data.parquet")

    print(f"Successfully processed {len(df)} properties to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()