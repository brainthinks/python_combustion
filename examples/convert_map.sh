#!/usr/bin/env bash

# Note - you should execute this script from the project directory, like so:
#
# ./examples/convert_all_retail_maps.sh "a10" "path/to/drive_c"

map_name="$1"
drive_c_path="$2"

if [ -z "$map_name" ]; then
  echo "ERROR: You must provide the name of the map you wish to convert!"
  exit 1
fi

if [ -z "$drive_c_path" ]; then
  echo "ERROR: You must provide the path to the C drive that contains Halo PC and Halo CE!"
  exit 1
fi

source "./examples/utils.sh"
# installSystemDependencies
# installCombustion

"./examples/convert_map.py" "$map_name" "$drive_c_path" "$combustion_lib_path"

if [ $? -ne 0 ]; then
  echo "Failed to convert map ${map_name}!!"
  exit 1
fi

echo "Successfully converted the ${map_name} map."
exit 0
