#!/usr/bin/env python3
# encoding=utf-8

"""keyring file decode script.

See http://www.rbxbzd.com for details on the file structure and key structure.
"""
__author__ = "chengxuebin@outlook.com"
__copyright__ = "Copyright 2022 RBXBZD"
__license__ = "MIT"
__version__ = "1.0"

import os
import sys
import optparse
from utils import *

if sys.version_info < (3, 0):
  sys.exit("Requires Python 3.0 or later.")

# some constants
EOF_TAG_SIZE = 3
EOF_TAG = b'EOF'
FILE_VERSION_PREFIX = "Keyring file version:"
FILE_VERSION_SIZE = 3
POM_SIZE = 8
XOR_OBFUSCATE = b'*305=Ljt0*!@$Hnm(*-9-w;:'

# some global variables
# print 3 columns, The value is the width of each column in characters
printer1 = PrettyPrint(
    [{"width": 18, "align": "<"}, {"width": 40, "align": "<"}])
printer2 = PrettyPrint([{"width": 14, "align": "<"}, {
                       "width": 8, "align": ">"}, {"width": 68, "align": "<"}])


def ParseFile(file_path):
  # r+b mode is open the binary file in read or write mode.
  with open(file_path, "rb") as f:
    fbytes = f.read()

  printer1.PrintSplitRow()
  printer1.PrintRow(["File properties", "Value"])
  printer1.PrintSplitRow()
  printer1.PrintRow(["Total bytes", len(fbytes)])
  printer1.PrintRow(["Version bytes", len(FILE_VERSION_PREFIX)])

  read_pos = len(FILE_VERSION_PREFIX)
  file_ver = fbytes[read_pos:read_pos+FILE_VERSION_SIZE].decode('ascii')
  read_pos += FILE_VERSION_SIZE
  printer1.PrintRow(["Version", FILE_VERSION_PREFIX+file_ver])
  printer1.PrintSplitRow()
  # print(fbytes.hex())

  key_index = 0
  while fbytes[read_pos:read_pos+3] != EOF_TAG:
    total_size = int.from_bytes(fbytes[read_pos:read_pos+1], "big")
    print("\n" + bcolors.OKGREEN +
          "Key {}: {} bytes (include LENGTH_DESP 40 bytes)".format(key_index, total_size) + bcolors.ENDC)

    printer2.PrintSplitRow()
    printer2.PrintRow(["Field", "Length", "Data"])
    printer2.PrintSplitRow()

    # 解析各字段长度
    read_pos += POM_SIZE
    key_id_size = int.from_bytes(fbytes[read_pos:read_pos+1], "big")

    read_pos += POM_SIZE
    key_type_size = int.from_bytes(fbytes[read_pos:read_pos+1], "big")

    read_pos += POM_SIZE
    user_size = int.from_bytes(fbytes[read_pos:read_pos+1], "big")

    read_pos += POM_SIZE
    key_data_size = int.from_bytes(fbytes[read_pos:read_pos+1], "big")
    read_pos += POM_SIZE

    # calculate padding accortding to POM_SIZE
    padding_size = (POM_SIZE - (key_id_size+key_type_size +
                                user_size+key_data_size) % POM_SIZE) % POM_SIZE

    # Parse the contents of each field
    key_id = fbytes[read_pos:read_pos+key_id_size]
    printer2.PrintRow(["KEY_ID", key_id_size, key_id.decode('ascii')])
    read_pos += key_id_size

    key_type = fbytes[read_pos:read_pos+key_type_size]
    printer2.PrintRow(["KEY_TYPE", key_type_size, key_type.decode('ascii')])
    read_pos += key_type_size

    user = fbytes[read_pos:read_pos+user_size]
    printer2.PrintRow(["USER_ID", user_size, user.decode('ascii')])
    read_pos += user_size

    key_data = fbytes[read_pos:read_pos+key_data_size]
    printer2.PrintRow(["KEY_DATA", key_data_size, key_data.hex()])

    # The real key needs to be XORed
    actual_key = xor_key(key_data)
    printer2.PrintRow(["ACTUAL_KEY", key_data_size,  actual_key.hex()])

    printer2.PrintRow(["PADDING", padding_size, "0"])
    printer2.PrintSplitRow()
    read_pos += key_data_size + padding_size
    key_index += 1

  print("\nReached end symbol: {}".format(fbytes[read_pos:read_pos+3]))


def xor_key(key_bytes):
  out = bytearray()
  l = 0
  for b in key_bytes:
    out.append(b ^ XOR_OBFUSCATE[l])
    l = (l+1) % len(XOR_OBFUSCATE)
  return out


def main(argv):
  parser = optparse.OptionParser("Usage: %prog [options] file")
  parser.add_option("-v", "--verbose", dest="verbose")
  # parse cmdline arguments to an object
  # then pass to main
  (options, args) = parser.parse_args()
  if len(args) != 1:
    parser.error("The argument of keyring file is missing.")
  keyring_file = os.path.realpath(args[0])
  ParseFile(keyring_file)


# Omitted when being used as module
if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
