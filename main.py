#!/usr/bin/env python3

import os

from src.combustion import convert_map

lib_path = os.path.join(os.path.dirname(__file__), '../combustion/target/release/libcombustion_r.so')
map_name = "a10"
ms_games_path = "/home/user/PlayOnLinux's virtual drives/halo_ce_new/drive_c/Program Files/Microsoft Games/"

convert_map(map_name, ms_games_path, lib_path)

# @todo - convert them all!
map_names = [
  'a10', #
  'a30', #
  'a50', #
  'b30', #
  'b40', #
  'c10', #
  'c20', #
  'c40', #
  'd20', #
  'd40', #
]

