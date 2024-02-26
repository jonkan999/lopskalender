import geopandas as gpd
from shapely.geometry import Point
from sweref99 import projections
import pandas as pd
import pyproj

counties = gpd.read_file("counties/no_10km.shp")

def find_county(lat, lon):
    # Convert the WGS 84 coordinates to SWEREF 99 using the latlon_to_rt90 function
    tm = projections.make_transverse_mercator("SWEREF_99_TM")
    northing, easting = tm.geodetic_to_grid(lat, lon)

    # Create a shapely Point object from the transformed coordinates
    point = Point(easting, northing)
    print(point)
    # Loop through the counties and check if the point is inside each polygon
    for i in range(len(counties)):
        #print(counties.iloc[i].geometry)
        if point.within(counties.iloc[i].geometry):
            return counties.iloc[i]

    # If the point is not inside any polygon, return None
    return None

def find_county(lat, lon):
    # Load the GeoJSON file
    gdf = gpd.read_file('counties/fylker.geojson')

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



if __name__ == "__main__":
    #read_dpf()
    find_county2(60.329306, 11.018611)
    #print(find_county(60.329306, 11.018611))

def read_dpf():
    # Read the data from the file
    df = gpd.read_file('counties/no_10km.shp')

    print(df)