#!/usr/bin/env python3

# This script will convert all retail Halo PC map files into map files that are
# compatible with Halo CE.  This script assumes that Halo and Halo CE are
# installed in their default directories.
#
# If you know that your Halo installations are in different directories, or you
# want to convert a non-retail map, or you have some other custom requirement,
# you do not have to use this script.  You can import the Python package in the
# src directory, as is done in this file, to get access to functions that give
# you control over what files you want to convert.

import os

# This allows me to import the pycombustion package
# @see - https://stackoverflow.com/a/4383597
# @see - https://stackoverflow.com/a/30218825
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pycombustion

# These must be provided.  See the included "convert_all_retail_maps.sh" file
# for an example
drive_c_path = sys.argv[1]
combustion_lib_path = sys.argv[2]

pycombustion.convert_all_retail_maps(drive_c_path, combustion_lib_path)
