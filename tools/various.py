import os
import time
import unicodedata
from datetime import datetime
import xml.etree.ElementTree as ET

'''
# Coordinate transformation (EPSG:3301 -> WGS84 if needed)
transformer = pyproj.Transformer.from_crs(3301, 4326, always_xy=True)

def process_coordinates(x: float, y: float) -> Tuple[float, float]:
    """Transform coordinates if needed"""
    lon, lat = transformer.transform(x, y)
    return round(lon, 6), round(lat, 6)  # 6 decimal places (~10cm precision)
'''

def maakond_to_id(maakond: str) -> int:
    
    maakond = maakond.strip().decode("utf-8")
    maakonnad = {
        "Harju maakond": 0,          
        "Hiiu maakond" : 1,
        "Ida-Viru maakond": 2,
        "Jõgeva maakond": 3,
        "Järva maakond": 4,
        "Lääne maakond": 5,
        "Lääne-Viru maakond": 6,
        "Põlva maakond": 7,
        "Pärnu maakond": 8,
        "Rapla maakond": 9,
        "Saare maakond": 10,
        "Tartu maakond": 11,
        "Valga maakond": 12,
        "Viljandi maakond": 13,
        "Võru maakond": 14,
    }

    if maakond in maakonnad:
        return maakonnad[maakond]
    return 999


def string_cleanup(txt: str) -> str:
    normalized = unicodedata.normalize('NFKD', txt.decode('utf-8').lower().replace(' ', '_'))
    return ''.join(c for c in normalized if not unicodedata.combining(c))


def normalize_date(date_str: str) -> int:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        reference_dt = datetime(2025, 1, 1, 0, 0, 0)
        seconds_elapsed = int((dt - reference_dt).total_seconds())
        return seconds_elapsed
        
    except (ValueError, TypeError) as e:
        print(f"Error normalizing date {date_str}: {e}")
        return 0  # Fallback value
    

def prettify_cadaster(cadaster_nr: str) -> str:
    return cadaster_nr.decode('utf-8').replace(':', '_')
    
def get_xml_data(cadaster_nr: str) -> dict:

    x_min = 9999999
    x_max = 0
    y_min = 9999999
    y_max = 0
    no_data = False
    
    # we have owner XML!
    filepath = '../metsaregister_xml/' + prettify_cadaster(cadaster_nr) + ".xml"
    if os.path.isfile(filepath):

        tree = ET.parse(filepath)
        namespaces = {
                    'mets': 'http://metsaregister.x-road.eu',
                    'gml': 'http://www.opengis.net/gml',
                    'xlink': 'http://www.w3.org/1999/xlink'
        }
        elements = tree.findall('.//mets:eraldis', namespaces)
        for el in elements:
            geom = el.find('.//mets:geomeetria', namespaces)
            coords_el = geom.find('.//gml:coordinates', namespaces)
            if coords_el is not None and coords_el.text:
                coords_text = coords_el.text.strip()
                # Split into coordinate pairs
                for pair in coords_text.split():
                    x, y = map(float, pair.split(','))
                    if x < x_min: x_min = x # 600 000
                    if x > x_max: x_max = x
                    if y < y_min: y_min = y # 6 000 000
                    if y > y_max: y_max = y

    
    # we will use PUBLIC xml!
    else:
        filepath = '../metsaregister_cache/metsaregister_eraldis__katastri_nr-' + prettify_cadaster(cadaster_nr) + ".xml"


        if os.path.isfile(filepath):
            tree = ET.parse(filepath)
            namespaces = {
                "wfs": "http://www.opengis.net/wfs/2.0",
                "gml": "http://www.opengis.net/gml/3.2",
                "metsaregister": "https://mets-ave.envir.ee"
            }
            members = tree.findall('.//wfs:member', namespaces)
            if len(members):
                for member in members:
                    pos_lists = member.findall(".//gml:posList", namespaces)
                    for pos_list in pos_lists:
                        coord_text = pos_list.text.strip()
                        coords = list(map(float, coord_text.split()))
                        # Group into (x, y) pairs
                        coordinate_pairs = list(zip(coords[::2], coords[1::2]))

                        # Loop through coordinate pairs
                        # NOTE! x, y order!
                        for y, x in coordinate_pairs:
                            if x < x_min: x_min = x # 600 000
                            if x > x_max: x_max = x
                            if y < y_min: y_min = y # 6 000 000
                            if y > y_max: y_max = y
            else:
                print(f"Error: XML has no eraldis: {cadaster_nr}")
                no_data = True
        else:
            print(f"Error: MISSING XML: {cadaster_nr}")
            no_data = True
        

    
    return {
        'epsg_x': (x_min + x_max) / 2.0,
        'epsg_y': (y_min + y_max) / 2.0,
        'no_data': no_data
        }
