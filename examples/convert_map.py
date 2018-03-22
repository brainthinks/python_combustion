#!/usr/bin/env python3

import os

# This allows me to import the pycombustion package
# @see - https://stackoverflow.com/a/4383597
# @see - https://stackoverflow.com/a/30218825
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pycombustion

map_name = sys.argv[1]
drive_c_path = sys.argv[2]
combustion_lib_path = sys.argv[3]

pycombustion.convert_map(map_name, drive_c_path, combustion_lib_path)
