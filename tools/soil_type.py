import urllib.request

_SUBSCRIPT = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
_JSON_SPECIAL = str.maketrans('",{}[]:', '_______')

import xml.etree.ElementTree as ET
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / 'cache' / 'soil_type'
WFS_URL = (
    'https://inspire.geoportaal.ee/geoserver/SO_pinnas/wfs'
    '?service=WFS&version=2.0.0&request=GetFeature'
    '&typeNames=SO_pinnas:SO.SoilBody'
    '&CQL_FILTER=INTERSECTS(geom,POINT({y}%20{x}))'
)

NAMESPACES = {
    'wfs': 'http://www.opengis.net/wfs/2.0',
    'SO_pinnas': 'ee.maaamet.so-mullakaart',
}

def _clean(s: str) -> str | None:
    return s.translate(_SUBSCRIPT).translate(_JSON_SPECIAL) or None


def _cache_path(x: float, y: float) -> Path:
    return CACHE_DIR / f'{round(x, 2)}_{round(y, 2)}.xml'


def _fetch(x: float, y: float) -> str:
    url = WFS_URL.format(x=x, y=y)
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read().decode('utf-8')


def _parse(xml_text: str) -> dict | None:
    root = ET.fromstring(xml_text)
    members = root.findall('.//wfs:member', NAMESPACES)
    if not members:
        return None
    body = members[0].find('SO_pinnas:SO.SoilBody', NAMESPACES)
    label = body.find('SO_pinnas:soilbodylabel', NAMESPACES)
    name = body.find('SO_pinnas:gml_name', NAMESPACES)
    gml_name = name.text if name is not None else ''
    profile, _, mod = gml_name.partition('/')
    return {
        'soilbodylabel': label.text if label is not None else None,
        'soil_profile': _clean(profile),
        'soil_mod': _clean(mod),
    }


def get_soil_type(x: float, y: float) -> dict | None:
    cache_file = _cache_path(x, y)

    if cache_file.exists():
        return _parse(cache_file.read_text(encoding='utf-8'))

    xml_text = _fetch(x, y)
    result = _parse(xml_text)
    if result is not None:
        cache_file.write_text(xml_text, encoding='utf-8')
    return result
