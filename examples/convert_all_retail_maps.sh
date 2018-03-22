#!/usr/bin/env bash

# Note - you should execute this script from the project directory, like so:
#
# ./examples/convert_all_retail_maps.sh "path/to/drive_c"

drive_c_path="$1"

if [ -z "$drive_c_path" ]; then
  echo "ERROR: You must provide the path to the C drive that contains Halo PC and Halo CE!"
  exit 1
fi

source "./examples/utils.sh"
installSystemDependencies
installCombustion

"./examples/convert_all_retail_maps.py" "$drive_c_path" "$combustion_lib_path"

if [ $? -ne 0 ]; then
  echo "Failed to convert maps!!"
  exit 1
fi

echo "Successfully converted all Halo PC maps."
exit 0
