import os
import ctypes
from cffi import FFI

# @todo - do we have to pass ffi?
def _create_read_only_buffer_tuple(ffi, file_path):
  file = open(file_path, 'rb')

  # the number of bytes in the file
  # using "len" because that is combustion's terminology
  file_len = os.fstat(file.fileno()).st_size
  # the ffi-compatible read-only buffer
  # using "raw" because that is combustion's terminology
  file_raw = ffi.from_buffer(file.read(file_len))

  return ( file_raw, file_len )

# @todo - do we have to pass ffi?
# @todo - do we really have to know the length up front?
def _create_writable_buffer_tuple(ffi, length):
  # @todo - is it possible to create a buffer that can be passed as a pointer
  # without first knowing the size it will need to be?  If that can be done, the
  # above function wouldn't need to be called, and in fact it wouldn't need to be
  # present at all.  Until I know how to do that, converted_map_len is needed
  # here.

  # this is the buffer that will be written to
  # to write its contents to a file, it must be converted by ffi.buffer()
  buffer_raw = ffi.new("char[]", length)
  # this is the pointer that needs to be passed to the library
  buffer_pointer = ffi.cast("char *buffer", buffer_raw)

  return ( buffer_raw, buffer_pointer, length )


"""
===================================
Bindings for the Combustion Library
===================================
"""

# @todo - provide a default for combustion_lib_path
def _convert_map(map_data_path, multiplayer_path, bitmaps_pc_path, bitmaps_ce_path, sounds_pc_path, sounds_ce_path, destination, combustion_lib_path):
  # Initialize the FFI
  ffi = FFI()
  # Use the c header
  ffi.cdef(open(os.path.join(os.path.dirname(__file__), 'combustion.h')).read())
  # Import the dynamic library
  libcombustion_r = ffi.dlopen(combustion_lib_path)

  map_data = _create_read_only_buffer_tuple(ffi, map_data_path)

  # @todo
  multiplayer = ( ffi.from_buffer(ctypes.create_string_buffer(0)), 0 )

  bitmaps_pc = _create_read_only_buffer_tuple(ffi, bitmaps_pc_path)
  sounds_pc = _create_read_only_buffer_tuple(ffi, sounds_pc_path)
  bitmaps_ce = _create_read_only_buffer_tuple(ffi, bitmaps_ce_path)
  sounds_ce = _create_read_only_buffer_tuple(ffi, sounds_ce_path)

  converted_map_len = libcombustion_r.convert_map_cd_len(
    map_data[0], map_data[1],
    multiplayer[0], multiplayer[1],
    bitmaps_pc[0], bitmaps_pc[1],
    bitmaps_ce[0], bitmaps_ce[1],
    sounds_pc[0], sounds_pc[1],
    sounds_ce[0], sounds_ce[1],
    # This last argument is needed to ensure that cffi passes the rest of the arguments correctly.
    # I don't know why.
    0
  )

  if converted_map_len is 0:
    raise Exception("ERROR!! No data to write to {}!".format(map_name))

  map_buffer = _create_writable_buffer_tuple(ffi, converted_map_len)

  converted_map_len = libcombustion_r.convert_map_cd(
    map_buffer[1], map_buffer[2],
    map_data[0], map_data[1],
    multiplayer[0], multiplayer[1],
    bitmaps_pc[0], bitmaps_pc[1],
    bitmaps_ce[0], bitmaps_ce[1],
    sounds_pc[0], sounds_pc[1],
    sounds_ce[0], sounds_ce[1],
    # This last argument is needed to ensure that cffi passes the rest of the arguments correctly.
    # I don't know why.
    0
  )

  buffer_file = open(destination, 'wb+')
  buffer_file.write(ffi.buffer(map_buffer[0]))
  buffer_file.close()
