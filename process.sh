
for dir in ./modules/*; do
    if [ -f "$dir/blocks-properties.geojson" ]; then
        rm "$dir/blocks-properties.geojson"
        rm "$dir/blockgroups.geojson"
    fi

    python assign-features-to-blocks.py "$dir/blocks.geojson" "$dir/blocks-properties.geojson"
    python dissolve-block-data.py "$dir/blocks-properties.geojson" "$dir/blockgroups.geojson"
done
