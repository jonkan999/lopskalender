import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import pyproj

gdf = gpd.read_file('counties/fylker.geojson')


def find_county(lat, lon):
    # Define the point coordinates you want to map
    # Create a Point object from the point coordinates
    point_coords = (lat, lon)
    point = Point(point_coords)

    # Define the original CRS of the point (WGS84)
    crs_wgs84 = pyproj.CRS('EPSG:4326')

    # Define the target CRS of the GeoJSON file (the CRS in which the GeoJSON file is projected)
    crs_target = pyproj.CRS('EPSG:25833')

    # Create a transformer to transform the coordinates from the original CRS to the target CRS
    transformer = pyproj.Transformer.from_crs(crs_wgs84, crs_target, always_xy=True)

    # Transform the point coordinates to the target CRS
    point_transformed = transformer.transform(point_coords[1], point_coords[0])

    # Create a new Point object from the transformed coordinates
    point_transformed = Point(point_transformed)

    # Use the 'contains' method to check if the point falls within a polygon
    # representing a region in Norway
    for index, row in gdf.iterrows():
        if row['geometry'].contains(point_transformed):
            return row['navn']

    # If no mapping was found, try adjusting the latitude and longitude by ±0.5% and ±1%
    for lat_adjust in [-0.05, 0, 0.05]:
        for lon_adjust in [-0.05, 0, 0.05]:
            new_lat = lat + lat_adjust
            new_lon = lon + lon_adjust

            # Define the point coordinates with the adjustments
            new_point_coords = (new_lat, new_lon)
            new_point = Point(new_point_coords)

            # Transform the adjusted point coordinates to the target CRS
            new_point_transformed = transformer.transform(new_point_coords[1], new_point_coords[0])

            # Create a new Point object from the transformed adjusted coordinates
            new_point_transformed = Point(new_point_transformed)

            # Use the 'contains' method to check if the adjusted point falls within a polygon
            # representing a region in Norway
            for index, row in gdf.iterrows():
                if row['geometry'].contains(new_point_transformed):
                    return row['navn']





if __name__ == "__main__":
    #read_dpf()
    print(find_county(58.77882439999999,5.623686000000001))
    #print(find_county(60.329306, 11.018611))
