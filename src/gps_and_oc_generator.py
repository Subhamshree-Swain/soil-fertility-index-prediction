import load_dataset.py
import numpy as np

field_size_m = 1000 #in meters
m_degree_conversion = 111000
seed1 = 35
seed2 = 56


def gps_generator(data, field_size_m):

    # 22°18'57.6"N 87°18'31.0"E # IIT KGP centeral location

    lat_center = 22.18576
    lon_center = 87.1831

    lat_range = (field_size_m / m_degree_conversion) / 2
    lon_range = (field_size_m / (m_degree_conversion * np.cos(np.radians(lat_center)))) / 2


    np.random.seed(seed1)
    n_samples = len(data)

    grid_sz = int(np.sqrt(n_samples))
    lat_grid = np.linspace(lat_center - lat_range, lat_center + lat_range, grid_sz)
    lon_grid = np.linspace(lat_center - lat_range, lat_center + lat_range, grid_sz)

    latitudes = []
    longitudes = []
    for i in range(n_samples):
        grid_i = i // grid_sz
        grid_j = i % grid_sz
        if grid_i < len(lat_grid) and grid_j < len(lon_grid):
            lat = lat_grid[grid_i] + np.random.normal(0, lat_range/grid_sz/3)
            lon = lon_grid[grid_j] + np.random.normal(0, lon_range/grid_sz/3)
        else:
            lat = np.random.uniform(lat_center - lat_range, lat_center + lat_range)
            lon = np.random.uniform(lon_center - lon_range, lon_center + lon_range)
        
        latitudes.append(lat)
        longitudes.append(lon)

    data["Latitude"] = latitudes[0:n_samples]
    data["Longitude"] = longitudes[0:n_samples]
    
    return data

def oc_generator(data):
    np.random.seed(seed2)

    n_samples = len(data)
    data["OC"] = 0.005 * data["N"] + np.random.normal(0.2, 0.5, n_samples)
    data["OC"] = data["OC"].clip(0.3, 2.5) # indian farmland max OC 2.5%

    return data
