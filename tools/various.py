import unicodedata
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
