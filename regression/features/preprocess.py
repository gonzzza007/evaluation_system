import sqlite3
import pandas as pd
from pathlib import Path
import argparse
from typing import Dict, Any

def fetch_properties_from_db(db_path: Path) -> Dict[str, Any]:
    """Fetch property data from SQLite database"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()
    
    # Fetch basic property info
    cursor.execute("""
        SELECT cadastral_nr, area, county, added_on, price 
        FROM properties
    """)
    properties = cursor.fetchall()
    
    # Fetch stands for each property
    property_data = {}
    for prop in properties:
        cadaster_nr = prop['cadastral_nr']
        
        '''
        cursor.execute("""
            SELECT tree_breed, age 
            FROM forest_stands 
            WHERE cadaster_nr = ?
        """, (cadaster_nr,))
        stands = cursor.fetchall()
        '''
        
        property_data[cadaster_nr] = {
            'cadaster_nr': cadaster_nr,
            'area': prop[1],
            'maakond': prop[2],
            'soil_type': prop[3],
            'water_distance': prop[4],
            'price': prop['price'],
            # 'stands': [{'tree_breed': s[0], 'age': s[1]} for s in stands]
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
            'cadaster_nr': cadaster,
            'area': data['area'],
            'maakond': data['maakond'],
            # 'soil_type': data['soil_type'],
            # 'water_distance': data['water_distance'],
            # 'avg_tree_age': sum(s['age'] for s in data['stands'])/len(data['stands']),
            # 'dominant_breed': max(
                # set(s['tree_breed'] for s in data['stands']), 
                # key=lambda x: sum(1 for s in data['stands'] if s['tree_breed'] == x)
            # ),
            'target_price': data['price']
        })
    return pd.DataFrame(records)

def main():
    parser = argparse.ArgumentParser(description='Process property data from SQLite to training CSV')
    parser.add_argument('--db-path', type=str, required=True,
                      help='Path to SQLite database file')
    parser.add_argument('--output', type=str, required=True,
                      help='Output CSV file path')
    
    args = parser.parse_args()
    
    # Convert strings to Path objects
    db_path = Path(args.db_path)
    output_path = Path(args.output)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Process data
    print(f"Loading data from {db_path}...")
    property_data = fetch_properties_from_db(db_path)
    df = process_to_dataframe(property_data)
    df.to_csv(output_path, index=False)
    print(f"Successfully processed {len(df)} properties to {output_path}")

if __name__ == "__main__":
    main()