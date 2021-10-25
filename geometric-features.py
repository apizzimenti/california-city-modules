
from evaltools.geography import dissolve
import geopandas as gpd
import pandas as pd
import warnings
from sys import argv

# Filter warnings.
warnings.simplefilter("ignore", UserWarning)

blocksin, bgsin, dout = argv[-3], argv[-2], argv[-1]
blocks = gpd.read_file(blocksin).to_crs("epsg:4326")

# Get the name of the module.
name = blocksin.split("/")[2].replace("-", "_")

# Create a CSV of unit centroids.
blocks["CENTROID"] = blocks["geometry"].centroid
blocks[["LAT", "LNG"]] = blocks["CENTROID"].apply(lambda p: pd.Series([p.y, p.x]))
blocks = blocks.rename({"Block": "GEOID"}, axis=1)
blocks[["GEOID", "LAT", "LNG"]].to_csv(f"{dout}/{name}_blocks20.csv", index=False)

# Create boundaries.
bgs = gpd.read_file(bgsin).to_crs("epsg:4326")
boundary = dissolve(blocks, by="State").boundary
boundary.to_file(f"{dout}/{name}.geojson", driver="GeoJSON")
