import random
import math

def gerar_coordenadas(lat_usuario, lon_usuario, distancia_max_km=3):
    delta_lat = (distancia_max_km/111) * random.uniform(-1,1)
    delta_lon = (distancia_max_km / (111 * abs(math.cos(math.radians(lat_usuario))))) * random.uniform(-1, 1)
    return lat_usuario + delta_lat, lon_usuario + delta_lon