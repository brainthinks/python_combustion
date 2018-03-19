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

# Prepare the output file
# @todo - write an empty file first
# @todo - dynamically set the buffer length!  perhaps make it the max of a 32 bit int?
buffer_len = 1000000000
buffer_raw = ffi.new("char[]", buffer_len)
buffer_file = open(target_map_path, 'rb+')
buffer_pointer = ffi.addressof(buffer_raw)

# Prepare the map file that is to be converted
map_data_file = open(source_map_path, 'rb')
map_data_len = os.fstat(map_data_file.fileno()).st_size
map_data_raw = ffi.from_buffer(map_data_file.read(map_data_len))

# @todo - what is multiplayer?!?!?
multiplayer_file = '???'
multiplayer_len = 0
multiplayer_raw = ffi.from_buffer(ctypes.create_string_buffer(0))

# Prepare the Halo PC bitmaps.map file
bitmaps_pc_file = open(bitmaps_pc_path, 'rb')
bitmaps_pc_len = os.fstat(bitmaps_pc_file.fileno()).st_size
bitmaps_pc_raw = ffi.from_buffer(bitmaps_pc_file.read(bitmaps_pc_len))

# Prepare the Halo CE bitmaps.map file
bitmaps_ce_file = open(bitmaps_ce_path, 'rb')
bitmaps_ce_len = os.fstat(bitmaps_ce_file.fileno()).st_size
bitmaps_ce_raw = ffi.from_buffer(bitmaps_ce_file.read(bitmaps_ce_len))

# Prepare the Halo PC sounds.map file
sounds_pc_file = open(sounds_pc_path, 'rb')
sounds_pc_len = os.fstat(sounds_pc_file.fileno()).st_size
sounds_pc_raw = ffi.from_buffer(sounds_pc_file.read(sounds_pc_len))

# Prepare the Halo CE sounds.map file
sounds_ce_file = open(sounds_ce_path, 'rb')
sounds_ce_len = os.fstat(sounds_ce_file.fileno()).st_size
sounds_ce_raw = ffi.from_buffer(sounds_ce_file.read(sounds_ce_len))

print('---')
print('Calling libcombustion_r.convert_map_cd...')
print('---')

# Call the library method to convert the maps!
converted_map_file_size = libcombustion_r.convert_map_cd(
  buffer_pointer, buffer_len,
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

print('---')
print('libcombustion_r.convert_map_cd finished...')
print('---')

print("About to write {} bytes to {}...".format(converted_map_file_size, target_map_path))

# This is the raw converted map
converted_map = buffer_raw[0:converted_map_file_size]

# Write the raw converted map to the target file
buffer_file.write(ffi.buffer(converted_map))

print('Done converting {}!'.format(map_name))
