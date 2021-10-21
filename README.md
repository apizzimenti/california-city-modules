
# California City- and County-Based Districtr Modules
Included here is a batch-based flow for processing California's City- and
County-based modules.

## Installation
Clone this repository and install the [`plan-evaluation-processing`](https://github.com/mggg/plan-evaluation-processing) package; `dissolve-block-script.py` requires it.

## Usage
The `process.sh` shell script is the driver for processing modules. On each run,
it erases all program-generated files and re-generates those files according to
the instructions in `assign-features-to-blocks.py` and `dissolve-block-data.py`
`process.sh` looks for specifically-named files in subdirectories of `modules/`,
modifies and assigns new features to blocks, and dissolves the block geometries
into block group geometries. The GeoJSON files produced are immediately ready
for upload to mapbox.

### Workflow
Let's say we want to prep a City of Lakewood module based on info sent to us from
the NDC.

1. Unzip `census-block-files.zip` and retrieve the `Lakewood Census Blocks 2020.json`
file.
2. Create a new subdirectory in the `modules/` directory called `lakewood/`, so the
path `modules/lakewood/` exists.
3. Move `Lakewood Census Blocks 2020.json` to `modules/lakewood/` and rename it
`blocks.geojson`, so the file `modules/lakewood/blocks.geojson` exists.
    * Repeat this step for any desired modules; some examples already exist in
    the `modules` directory, but feel free to delete them as they'll be re-processed
    each time `process.sh` is run.
4. Run `sh process.sh` from the root directory. This processes _any_ file which
matches the expression `modules/*/blocks.geojson`, so all GeoJSON files are
processed as a batch.
5. There should exist a `modules/lakewood/blockgroups.geojson` file which contains
the processed block group geometries.
6. The `modules/lakewood/blockgroups.geojson` and `modules/lakewood/blocks.geojson`
files are ready for use with districtr_process! (Pro tip: just copy all the
module subdirectories to districtr_process to make organizing them easier!)
