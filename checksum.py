
import geopandas as gpd
from sys import argv


# Read in the file.
fin = argv[-1]
units = gpd.read_file(fin)

# Get the population column and all the total population columns with OMB in them.
omb = [col for col in list(units) if "OMB" in col and "VAP" not in col]
pop = "Population2020"

# Get the sum of the columns and compare it to the total population.
try:
    assert units[pop].sum() == sum(units[col].sum() for col in omb)
except:
    print(units[pop].sum(), sum(units[col].sum() for col in omb))
