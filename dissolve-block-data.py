
from evaltools.geography import dissolve
import geopandas as gpd
from sys import argv


fin, fout = argv[-2], argv[-1]
blocks = gpd.read_file(fin)

# Which columns do we keep?
keep = [
    'ChildAtHome', 'Inc$75k+', 'Renters', 'Apts', 'HSGrads', 'CollegeGrads',
    'SpanishAtHome', 'AsnLangAtHome', 'OthLangAtHome', 'Inc75'
]

# Fill all NaNs with zeros.
blocks = blocks.fillna(0)

# Write to file.
bgs = dissolve(blocks, by="BlockGroup", keep=keep + ["State"], aggfunc="first")
bgs.to_file(fout, driver="GeoJSON")
