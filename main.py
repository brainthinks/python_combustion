#!/usr/bin/env python3

from cffi import FFI
import ctypes
import os

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
pc_base_dir = base_dir + "Halo/MAPS/halo_pc/"
ce_base_dir = base_dir + "Halo Custom Edition/maps/"

# Construct the file names
target_map_path = ce_base_dir + "test/" + map_file
source_map_path = pc_base_dir + map_file
multiplayer_path = pc_base_dir + '???' # @todo!!!
bitmaps_pc_path = pc_base_dir + "bitmaps.map"
bitmaps_ce_path = ce_base_dir + "bitmaps.map"
sounds_pc_path = pc_base_dir + "sounds.map"
sounds_ce_path = ce_base_dir + "sounds.map"

# Prepare the files in Python
buffer = ctypes.create_string_buffer(0)
map_data_file = open(source_map_path, 'rb')
multiplayer_file = '???'
bitmaps_pc_file = open(bitmaps_pc_path, 'rb')
bitmaps_ce_file = open(bitmaps_ce_path, 'rb')
sounds_pc_file = open(sounds_pc_path, 'rb')
sounds_ce_file = open(sounds_ce_path, 'rb')

# Calculate the number of bytes in each file
buffer_len = 0;
map_data_len = os.fstat(map_data_file.fileno()).st_size
multiplayer_len = 0
bitmaps_pc_len = os.fstat(bitmaps_pc_file.fileno()).st_size
bitmaps_ce_len = os.fstat(bitmaps_ce_file.fileno()).st_size
sounds_pc_len = os.fstat(sounds_pc_file.fileno()).st_size
sounds_ce_len = os.fstat(sounds_ce_file.fileno()).st_size

# Prepare the files for the combustion library
buffer_raw = ffi.new("char[]", 0)
map_data_raw = ffi.from_buffer(map_data_file.read(map_data_len))
multiplayer_raw = ffi.from_buffer(ctypes.create_string_buffer(0))
bitmaps_pc_raw = ffi.from_buffer(bitmaps_pc_file.read(bitmaps_pc_len))
bitmaps_ce_raw = ffi.from_buffer(bitmaps_ce_file.read(bitmaps_ce_len))
sounds_pc_raw = ffi.from_buffer(sounds_pc_file.read(sounds_pc_len))
sounds_ce_raw = ffi.from_buffer(sounds_ce_file.read(sounds_ce_len))

# Call the library method to convert the maps!
converted_map_file_size = libcombustion_r.convert_map_cd(
  buffer_raw, buffer_len,
  map_data_raw, map_data_len,
  multiplayer_raw, multiplayer_len,
  bitmaps_pc_raw, bitmaps_pc_len,
  bitmaps_ce_raw, bitmaps_ce_len,
  sounds_pc_raw, sounds_pc_len,
  sounds_ce_raw, sounds_ce_len,
  # This last argument is needed to ensure that cffi passes the rest of the arguments correctly.
  # I don't know why.
  0
)

# Write the converted map to a file
# buffer_file = open(target_map_path, 'wb')

print(len(buffer_raw))
# buffer_file.write(buffer)

print(converted_map_file_size)
