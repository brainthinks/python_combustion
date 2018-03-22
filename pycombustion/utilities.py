"""
Package containing bindings for the combustion library and utilities for
converting a single Halo PC map to be compatible with Halo CE and converting all
retail Halo PC maps.
"""

import os
from .bindings import _convert_map

"""
A tuple containing tuples that represents
* [0] the map file name without the extension
* [1] the name of the level contained in the map file
"""
HALO_MAPS = (
  ('a10', 'The Pillar of Autumn' ),
  ('a30', 'Halo' ),
  ('a50', 'The Truth and Reconciliation' ),
  ('b30', 'The Silent Cartographer' ),
  ('b40', 'Assault on the Control Room' ),
  ('c10', '343 Guilty Spark' ),
  ('c20', 'The Library' ),
  ('c40', 'Two Betrayals' ),
  ('d20', 'Keyes' ),
  ('d40', 'The Maw' ),
)


def _assert_file_exists(file_path):
  if os.path.isfile(file_path) is False:
    raise Exception("Could not find file " + file_path)


def _backup_target_file(file_path):
  if os.path.isfile(file_path) is True:
    # @todo - backup file at target location, if it exists, in a timestamped directory
    print("Found target file {}, going to overwrite...".format(file_path));
  else:
    print("Target file {} not found, going to create...".format(file_path));


# @todo - allow paths to be specified?
# @todo - provide a default for combustion_lib_path
def convert_map(map_name, drive_c_path, combustion_lib_path, title = ''):
  print("About to convert {}...".format(title or map_name))

  # Default locations of the Halo PC and Halo CE map directories
  pc_base_dir = drive_c_path + "/Program Files/Microsoft Games/Halo/MAPS/"
  ce_base_dir = drive_c_path + "/Program Files/Microsoft Games/Halo Custom Edition/maps/"

  # Construct the file names
  target_map_path = ce_base_dir + map_name + ".map"
  source_map_path = pc_base_dir + map_name + ".map"
  # @todo
  multiplayer_path = source_map_path
  bitmaps_pc_path = pc_base_dir + "bitmaps.map"
  bitmaps_ce_path = ce_base_dir + "bitmaps.map"
  sounds_pc_path = pc_base_dir + "sounds.map"
  sounds_ce_path = ce_base_dir + "sounds.map"

  _assert_file_exists(source_map_path)
  _assert_file_exists(multiplayer_path)
  _assert_file_exists(bitmaps_pc_path)
  _assert_file_exists(bitmaps_ce_path)
  _assert_file_exists(sounds_pc_path)
  _assert_file_exists(sounds_ce_path)

  _backup_target_file(target_map_path)

  _convert_map(
    source_map_path,
    multiplayer_path,
    bitmaps_pc_path,
    bitmaps_ce_path,
    sounds_pc_path,
    sounds_ce_path,
    target_map_path,
    combustion_lib_path,
  )

  print("Finished converting {}!".format(title or map_name))


def convert_all_retail_maps(drive_c_path, combustion_lib_path):
  for halo_map in HALO_MAPS:
    convert_map(halo_map[0], drive_c_path, combustion_lib_path, halo_map[1])
