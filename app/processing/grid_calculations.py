import hashlib

# Função para converter graus sexagesimais para decimais
def sexagesimal_para_decimal(graus, minutos, segundos, direcao):
    decimal = graus + minutos / 60 + segundos / 3600
    if direcao in ['S', 'W']:  # Se for Sul (S) ou Oeste (W), torna o valor negativo
        decimal = -decimal
    return decimal

# Função para calcular os vértices da folha de 1:1.000.000
def calcular_limites_1000000(latitude, longitude):
    lat_min_1000000 = int(latitude // 4) * 4
    lat_max_1000000 = lat_min_1000000 + 4
    lon_min_1000000 = int(longitude // 6) * 6
    lon_max_1000000 = lon_min_1000000 + 6
    return lat_min_1000000, lat_max_1000000, lon_min_1000000, lon_max_1000000

# Função para determinar a letra da zona com base na latitude
def determinar_letra_zona(latitude):
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
    letra_index = int(abs(latitude) // 4)  # Calcula o índice da letra com base no intervalo de 4º
    return letras[letra_index]

# Função para determinar o fuso com base na longitude
def determinar_fuso(longitude):
    fuso = int((longitude + 180) // 6) + 1
    return fuso

# Função para calcular a nomenclatura completa da zona
def determinar_zona(latitude, longitude):
    hemisferio = "S" if latitude < 0 else "N"
    letra = determinar_letra_zona(latitude)
    fuso = determinar_fuso(longitude)
    return f"{hemisferio}{letra}-{fuso}"

# Função para determinar em qual das quadriculas (V, X, Y, Z) o ponto está na folha 1:500.000
def determinar_quadricula_500000(lat, lon, lat_min, lat_max, lon_min, lon_max):
    lat_mid = (lat_min + lat_max) / 2
    lon_mid = (lon_min + lon_max) / 2
    if lat >= lat_mid and lon < lon_mid:
        return "V"  # Noroeste
    elif lat >= lat_mid and lon >= lon_mid:
        return "X"  # Nordeste
    elif lat < lat_mid and lon < lon_mid:
        return "Y"  # Sudoeste
    elif lat < lat_mid and lon >= lon_mid:
        return "Z"  # Sudeste

# Função para calcular os limites da folha de 1:500.000
def calcular_limites_500000(lat_min_1000000, lat_max_1000000, lon_min_1000000, lon_max_1000000, quadricula_500k):
    lat_mid = (lat_min_1000000 + lat_max_1000000) / 2
    lon_mid = (lon_min_1000000 + lon_max_1000000) / 2
    if quadricula_500k == "V":  # Noroeste
        return lat_mid, lat_max_1000000, lon_min_1000000, lon_mid
    elif quadricula_500k == "X":  # Nordeste
        return lat_mid, lat_max_1000000, lon_mid, lon_max_1000000
    elif quadricula_500k == "Y":  # Sudoeste
        return lat_min_1000000, lat_mid, lon_min_1000000, lon_mid
    elif quadricula_500k == "Z":  # Sudeste
        return lat_min_1000000, lat_mid, lon_mid, lon_max_1000000

# Função para determinar em qual das quadriculas (NO, NE, SO, SE) o ponto está na folha 1:250.000

# Função para determinar em qual das quadriculas (A, B, C, D) o ponto está na folha 1:250.000
def determinar_quadricula_250000(lat, lon, lat_min, lat_max, lon_min, lon_max):
    lat_mid = (lat_min + lat_max) / 2
    lon_mid = (lon_min + lon_max) / 2
    if lat >= lat_mid and lon < lon_mid:
        return "A"  # Noroeste
    elif lat >= lat_mid and lon >= lon_mid:
        return "B"  # Nordeste
    elif lat < lat_mid and lon < lon_mid:
        return "C"  # Sudoeste
    elif lat < lat_mid and lon >= lon_mid:
        return "D"  # Sudeste


# Função para calcular os limites da folha de 1:250.000
def calcular_limites_250000(lat_min_500000, lat_max_500000, lon_min_500000, lon_max_500000, quadricula_250k):
    lat_mid = (lat_min_500000 + lat_max_500000) / 2
    lon_mid = (lon_min_500000 + lon_max_500000) / 2
    if quadricula_250k == "A":  # Noroeste
        return lat_mid, lat_max_500000, lon_min_500000, lon_mid
    elif quadricula_250k == "B":  # Nordeste
        return lat_mid, lat_max_500000, lon_mid, lon_max_500000
    elif quadricula_250k == "C":  # Sudoeste
        return lat_min_500000, lat_mid, lon_min_500000, lon_mid
    elif quadricula_250k == "D":  # Sudeste
        return lat_min_500000, lat_mid, lon_mid, lon_max_500000


# Função para determinar em qual das quadriculas (I, II, III, IV, V, VI) o ponto está na folha 1:100.000
def determinar_quadricula_100000(lat, lon, lat_min, lat_max, lon_min, lon_max):
    lat_metade = (lat_max - lat_min) / 2
    lon_terco = (lon_max - lon_min) / 3
    lat_bounds = [lat_min, lat_min + lat_metade, lat_max]
    lon_bounds = [lon_min, lon_min + lon_terco, lon_min + 2 * lon_terco, lon_max]

    if lat >= lat_bounds[1] and lon < lon_bounds[1]:
        return "I"  # Noroeste
    elif lat >= lat_bounds[1] and lon >= lon_bounds[1] and lon < lon_bounds[2]:
        return "II"  # Norte-central
    elif lat >= lat_bounds[1] and lon >= lon_bounds[2]:
        return "III"  # Nordeste
    elif lat < lat_bounds[1] and lon < lon_bounds[1]:
        return "IV"  # Sudoeste
    elif lat < lat_bounds[1] and lon >= lon_bounds[1] and lon < lon_bounds[2]:
        return "V"  # Sul-central
    elif lat < lat_bounds[1] and lon >= lon_bounds[2]:
        return "VI"  # Sudeste

# Função para calcular os limites da folha de 1:100.000
def calcular_limites_100000(lat_min_250000, lat_max_250000, lon_min_250000, lon_max_250000, quadricula_100k):
    lat_metade = (lat_max_250000 - lat_min_250000) / 2
    lon_terco = (lon_max_250000 - lon_min_250000) / 3

    if quadricula_100k == "I":  # Noroeste
        return lat_min_250000 + lat_metade, lat_max_250000, lon_min_250000, lon_min_250000 + lon_terco
    elif quadricula_100k == "II":  # Norte-central
        return lat_min_250000 + lat_metade, lat_max_250000, lon_min_250000 + lon_terco, lon_min_250000 + 2 * lon_terco
    elif quadricula_100k == "III":  # Nordeste
        return lat_min_250000 + lat_metade, lat_max_250000, lon_min_250000 + 2 * lon_terco, lon_max_250000
    elif quadricula_100k == "IV":  # Sudoeste
        return lat_min_250000, lat_min_250000 + lat_metade, lon_min_250000, lon_min_250000 + lon_terco
    elif quadricula_100k == "V":  # Sul-central
        return lat_min_250000, lat_min_250000 + lat_metade, lon_min_250000 + lon_terco, lon_min_250000 + 2 * lon_terco
    elif quadricula_100k == "VI":  # Sudeste
        return lat_min_250000, lat_min_250000 + lat_metade, lon_min_250000 + 2 * lon_terco, lon_max_250000

# Função corrigida para determinar em qual das quadriculas (1, 2, 3, 4) o ponto está na folha 1:50.000
def determinar_quadricula_50000(lat, lon, lat_min, lat_max, lon_min, lon_max):
    lat_metade = (lat_min + lat_max) / 2
    lon_metade = (lon_min + lon_max) / 2
    if lat >= lat_metade and lon < lon_metade:
        return "1"  # Noroeste
    elif lat >= lat_metade and lon >= lon_metade:
        return "2"  # Nordeste
    elif lat < lat_metade and lon < lon_metade:
        return "3"  # Sudoeste
    elif lat < lat_metade and lon >= lon_metade:
        return "4"  # Sudeste


# Função para calcular os limites da folha de 1:50.000
def calcular_limites_50000(lat_min_100000, lat_max_100000, lon_min_100000, lon_max_100000, quadricula_50k):
    lat_metade = (lat_max_100000 - lat_min_100000) / 2
    lon_metade = (lon_max_100000 - lon_min_100000) / 2

    if quadricula_50k == "1":  # Noroeste
        return lat_min_100000 + lat_metade, lat_max_100000, lon_min_100000, lon_min_100000 + lon_metade
    elif quadricula_50k == "2":  # Nordeste
        return lat_min_100000 + lat_metade, lat_max_100000, lon_min_100000 + lon_metade, lon_max_100000
    elif quadricula_50k == "3":  # Sudoeste
        return lat_min_100000, lat_min_100000 + lat_metade, lon_min_100000, lon_min_100000 + lon_metade
    elif quadricula_50k == "4":  # Sudeste
        return lat_min_100000, lat_min_100000 + lat_metade, lon_min_100000 + lon_metade, lon_max_100000

# Função para determinar em qual das quadriculas (NO, NE, SO, SE) o ponto está na folha 1:25.000
def determinar_quadricula_25000(lat, lon, lat_min, lat_max, lon_min, lon_max):
    lat_metade = (lat_max - lat_min) / 2
    lon_metade = (lon_max - lon_min) / 2
    lat_bounds = [lat_min, lat_min + lat_metade, lat_max]
    lon_bounds = [lon_min, lon_min + lon_metade, lon_max]

    if lat >= lat_bounds[1] and lon < lon_bounds[1]:
        return "NO"  # Noroeste
    elif lat >= lat_bounds[1] and lon >= lon_bounds[1]:
        return "NE"  # Nordeste
    elif lat < lat_bounds[1] and lon < lon_bounds[1]:
        return "SO"  # Sudoeste
    elif lat < lat_bounds[1] and lon >= lon_bounds[1]:
        return "SE"  # Sudeste

# Função para calcular os limites da folha de 1:25.000
def calcular_limites_25000(lat_min_50000, lat_max_50000, lon_min_50000, lon_max_50000, quadricula_25k):
    lat_metade = (lat_max_50000 - lat_min_50000) / 2
    lon_metade = (lon_max_50000 - lon_min_50000) / 2

    if quadricula_25k == "NO":  # Noroeste
        return lat_min_50000 + lat_metade, lat_max_50000, lon_min_50000, lon_min_50000 + lon_metade
    elif quadricula_25k == "NE":  # Nordeste
        return lat_min_50000 + lat_metade, lat_max_50000, lon_min_50000 + lon_metade, lon_max_50000
    elif quadricula_25k == "SO":  # Sudoeste
        return lat_min_50000, lat_min_50000 + lat_metade, lon_min_50000, lon_min_50000 + lon_metade
    elif quadricula_25k == "SE":  # Sudeste
        return lat_min_50000, lat_min_50000 + lat_metade, lon_min_50000 + lon_metade, lon_max_50000

# Função para calcular grid1k_x e grid1k_y dinamicamente
def calcular_grid1k(lat, lon):
    """
    Esta função calcula os grids de 1km x 1km baseados na latitude e longitude.
    """
    # Multiplicamos por 100 para transformar a latitude/longitude em um número para divisão por 1000
    grid1k_x = int((lon * 100) % 1000)  # Valor exemplo para longitude
    grid1k_y = int((lat * 100) % 1000)  # Valor exemplo para latitude
    return grid1k_x, grid1k_y



# Função para converter decimal para Graus, Minutos e Segundos (GMS) truncado na segunda casa decimal dos segundos
def decimal_para_gms_truncado(coordenada, direcao):
    graus = int(coordenada)
    minutos = int((abs(coordenada) - abs(graus)) * 60)
    segundos = round((abs(coordenada) - abs(graus) - minutos / 60) * 3600, 2)
    
    # Formatar como solicitado: GºM'S'' -> e.g. 1S272291 para 1°27'22.91"S
    return f"{abs(graus)}{direcao}{abs(minutos):02d}{str(segundos).replace('.', '')}"

# Função para gerar o geo-hash SHA-128
def gerar_geo_hash(nomenclatura):
    return hashlib.sha512(nomenclatura.encode()).hexdigest()[:32]  # Truncando para 128 bits


# Função para gerar a nomenclatura completa
def gerar_nomenclatura_completa(zona, quadricula_500k, quadricula_250k, quadricula_100k, quadricula_50k, quadricula_25k, grid1k_x, grid1k_y, lat_origem, lon_origem):
    # Gerar latitude e longitude no formato GMS truncado
    lat_gms_truncado = decimal_para_gms_truncado(lat_origem, 'S' if lat_origem < 0 else 'N')
    lon_gms_truncado = decimal_para_gms_truncado(lon_origem, 'W' if lon_origem < 0 else 'E')

    grid_x_part = f"{grid1k_x}W" if grid1k_x < 0 else f"{grid1k_x}E"
    grid_y_part = f"{grid1k_y}S" if grid1k_y < 0 else f"{grid1k_y}N"

    # Nomenclatura textual completa
    nomenclatura = f"{zona}-{quadricula_500k}-{quadricula_250k}-{quadricula_100k}-{quadricula_50k}-{quadricula_25k}-{lat_gms_truncado}-{lon_gms_truncado}-{grid_x_part}-{grid_y_part}"

    # Gerar geo-hash
    geo_hash = gerar_geo_hash(nomenclatura)

    return nomenclatura, geo_hash

