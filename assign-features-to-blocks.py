# dissolve geojson blocks into bgs
# without screwing up everything

import json
from sys import argv

into, outto = argv[-2], argv[-1]

prev_features = {}
known_features = {}
out_features = []
cols = ['ChildAtHome', 'Inc75', 'Renters', 'Apts', 'HSGrads', 'CollegeGrads', 'SpanishAtHome', 'AsnLangAtHome', 'OthLangAtHome']

gj = json.load(open(into, 'r'))

for feature in gj["features"]:
    # Set Block Group and State codes.
    feature["properties"]["BlockGroup"] = feature["properties"]["Block"][:12]
    feature["properties"]["State"] = feature["properties"]["Block"][:2]
    blkgrp = feature["properties"]["BlockGroup"]
    missing_col = False

    # Re-name the income column *if* a renamed version doesn't already exist.
    if not feature["properties"].get("Inc75", None):
        feature["properties"]["Inc75"] = feature["properties"]["Inc$75k+"]

    # others
    for col in cols:
        if col not in feature["properties"]:
            print('did not find col ' + col)
            quit()

        if (feature["properties"][col] is not None) and (feature["properties"][col] > 0):
            # valid
            if blkgrp not in known_features:
                known_features[blkgrp] = {}
            if col not in known_features[blkgrp]:
                known_features[blkgrp][col] = feature["properties"][col]
        elif (blkgrp in known_features) and (col in known_features[blkgrp]):
            # populate column now
            feature["properties"][col] = known_features[blkgrp][col]
        else:
            missing_col = True

    if missing_col:
        if blkgrp not in prev_features:
            # fill in these missing columns later, once we know the values
            prev_features[blkgrp] = [feature]
        else:
            # copy from other block in blockgroup
            prev_features[blkgrp].append(feature)
    else:
        # keep feature as-is
        out_features.append(feature)

# fill in blanks which were noticed before we had seen the valid blockgroup values
for bg in prev_features.keys():
    for feature in prev_features[bg]:
        if bg in known_features:
            for col in cols:
                if col in known_features[bg]:
                    feature["properties"][col] = known_features[bg][col]
        out_features.append(feature)

with open(outto, "w") as f: 
    json.dump({
        "type": "FeatureCollection",
        "features": out_features,
    }, f, indent=2)
