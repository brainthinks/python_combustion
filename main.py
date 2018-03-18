#!/usr/bin/env python3

from cffi import FFI
from ctypes import *

lib_path = '../combustion/target/release/libcombustion_r.so'

ffi = FFI()

# @todo - is this the header file?
ffi.cdef("""
    int convert_map_cd(
      char *buffer, int,
      char *buffer, int,
      char *buffer, int,
      char *buffer, int,
      char *buffer, int,
      char *buffer, int,
      char *buffer, int,
      int
    );
""")

libcombustion_r = ffi.dlopen(lib_path)

# What map are we converting?
map_name = "a10"

# What is the directory to the Halo installations?
base_dir = "/home/user/PlayOnLinux's virtual drives/halo_ce_new/drive_c/Program Files/Microsoft Games/"

# Information necessary to construct file names
map_file = map_name + ".map"
pc_base_dir = base_dir + "Halo/MAPS/"
ce_base_dir = base_dir + "Halo Custom Edition/maps/"

# Construct the file names
target_map_path = ce_base_dir + "test/" + map_file
source_map_path = pc_base_dir + map_file
multiplayer_path = pc_base_dir + map_file # @todo
bitmaps_pc_path = pc_base_dir + "bitmaps.map"
bitmaps_ce_path = ce_base_dir + "bitmaps.map"
sounds_pc_path = pc_base_dir + "sounds.map"
sounds_ce_path = ce_base_dir + "sounds.map"

# Prepare the files
buffer = ffi.from_buffer(create_string_buffer(0))
map_data_raw = ffi.from_buffer(create_string_buffer(1))
multiplayer_raw = ffi.from_buffer(create_string_buffer(2))
bitmaps_pc_raw = ffi.from_buffer(create_string_buffer(3))
bitmaps_ce_raw = ffi.from_buffer(create_string_buffer(4))
sounds_pc_raw = ffi.from_buffer(create_string_buffer(5))
sounds_ce_raw = ffi.from_buffer(create_string_buffer(6))

# @todo - until I can figure out what multiplayer is...
multiplayer_raw = ffi.from_buffer(create_string_buffer(0))

# Calculate the number of bytes in each file
buffer_len = ffi.sizeof(buffer)
map_data_len = ffi.sizeof(map_data_raw)
multiplayer_len = ffi.sizeof(multiplayer_raw)
bitmaps_pc_len = ffi.sizeof(bitmaps_pc_raw)
bitmaps_ce_len = ffi.sizeof(bitmaps_ce_raw)
sounds_pc_len = ffi.sizeof(sounds_pc_raw)
sounds_ce_len = ffi.sizeof(sounds_ce_raw)

result = libcombustion_r.convert_map_cd(
  buffer, buffer_len,
  map_data_raw, map_data_len,
  multiplayer_raw, multiplayer_len,
  bitmaps_pc_raw, bitmaps_pc_len,
  bitmaps_ce_raw, bitmaps_ce_len,
  sounds_pc_raw, sounds_pc_len,
  sounds_ce_raw, sounds_ce_len,
  0
)

print(result)
