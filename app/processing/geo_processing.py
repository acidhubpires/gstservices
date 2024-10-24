# app/processing/geo_processing.py
from app.processing.grid_calculations import (
    calcular_limites_1000000,
    calcular_limites_500000,
    calcular_limites_250000,
    calcular_limites_100000,
    calcular_limites_50000,
    calcular_limites_25000,
    determinar_zona,
    determinar_quadricula_500000,
    determinar_quadricula_250000,
    determinar_quadricula_100000,
    determinar_quadricula_50000,
    determinar_quadricula_25000
)

def gerar_nomenclatura(lat, lon):
    try:
        zona = determinar_zona(lat, lon)
        lat_min_1000000, lat_max_1000000, lon_min_1000000, lon_max_1000000 = calcular_limites_1000000(lat, lon)
        quadricula_500k = determinar_quadricula_500000(lat, lon, lat_min_1000000, lat_max_1000000, lon_min_1000000, lon_max_1000000)

        lat_min_500000, lat_max_500000, lon_min_500000, lon_max_500000 = calcular_limites_500000(lat_min_1000000, lat_max_1000000, lon_min_1000000, lon_max_1000000, quadricula_500k)
        quadricula_250k = determinar_quadricula_250000(lat, lon, lat_min_500000, lat_max_500000, lon_min_500000, lon_max_500000)

        lat_min_250000, lat_max_250000, lon_min_250000, lon_max_250000 = calcular_limites_250000(lat_min_500000, lat_max_500000, lon_min_500000, lon_max_500000, quadricula_250k)
        quadricula_100k = determinar_quadricula_100000(lat, lon, lat_min_250000, lat_max_250000, lon_min_250000, lon_max_250000)

        lat_min_100000, lat_max_100000, lon_min_100000, lon_max_100000 = calcular_limites_100000(lat_min_250000, lat_max_250000, lon_min_250000, lon_max_250000, quadricula_100k)
        quadricula_50k = determinar_quadricula_50000(lat, lon, lat_min_100000, lat_max_100000, lon_min_100000, lon_max_100000)

        lat_min_50000, lat_max_50000, lon_min_50000, lon_max_50000 = calcular_limites_50000(lat_min_100000, lat_max_100000, lon_min_100000, lon_max_100000, quadricula_50k)
        quadricula_25k = determinar_quadricula_25000(lat, lon, lat_min_50000, lat_max_50000, lon_min_50000, lon_max_50000)

        nomenclatura_completa = f"{zona}-{quadricula_500k}-{quadricula_250k}-{quadricula_100k}-{quadricula_50k}-{quadricula_25k}"

        return nomenclatura_completa
    except Exception as e:
        return f"Erro ao gerar nomenclatura: {str(e)}"

def process_geodata(coordenadas):
    resultados = []
    for coord_set in coordenadas:
        for coord in coord_set:
            lon, lat = coord
            nomenclatura = gerar_nomenclatura(lat, lon)
            resultados.append({"coordenada": (lat, lon), "nomenclatura": nomenclatura})
    return resultados
