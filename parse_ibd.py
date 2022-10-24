#!/usr/bin/env python3
# encoding=utf-8

"""innodb tablespace file decode script.

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
# default page size 16KB
INNODB_PAGE_SIZE = 16*1024
# Start of the data on the page
FIL_PAGE_DATA = 38
# level of the node in an index tree; the leaf level is the level 0 */
PAGE_LEVEL = 26

INNODB_PAGE_TYPE = {
    # common page type
    '45bf': u'INDEX (B-tree node)',
    '45be': u'RTREE (B-tree node)',
    '0001': u'UNUSED',
    '0002': u'UNDO_LOG (Undo Log Page)',
    '0003': u'INODE (Index node)',
    '0004': u'IBUF_FREE_LIST (Insert Buffer Free List)',
    # introduced in MySQL/InnoDB 5.1.7
    '0000': u'ALLOCATED (Freshly Allocated Page)',
    '0005': u'IBUF_BITMAP (Insert Buffer Bitmap)',
    '0006': u'SYS (System Page)',
    '0007': u'TRX_SYS (Transaction system Page)',
    '0008': u'FSP_HDR (File Space Header)',
    '0009': u'XDES (extend description page)',
    '000a': u'BLOB (Uncompressed BLOB Page)',
    '000b': u'ZBLOB (First compressed BLOB page)',
    '000c': u'ZBLOB2 (Subsequent compressed BLOB Page)',
    '000d': u'UNKNOWN',
    '000e': u'COMPRESSED (Compressed page)',
    '000f': u'ENCRYPTED (Encrypted page)',
    '0010': u'COMPRESSED_AND_ENCRYPTED',
    '0011': u'ENCRYPTED_RTREE (Encrypted R-tree page)',
    # after MySQL 5.7
    '0012': u'SDI_BLOB (Uncompressed SDI BLOB page)',
    '0013': u'SDI_ZBLOB (Commpressed SDI BLOB page)',
    '0014': u'LEGACY_DBLWR (Legacy doublewrite buffer page)',
    '0015': u'RSEG_ARRAY (Rollback Segment Array page)',
    '0016': u'LOB_INDEX (Index pages of uncompressed LOB)',
    '0017': u'LOB_DATA (Data pages of uncompressed LOB)',
    '0018': u'LOB_FIRST (The first page of an uncompressed LOB)',
    '0019': u'ZLOB_FIRST (The first page of a compressed LOB)',
    '001a': u'ZLOB_DATA (Data pages of compressed LOB)',
    '001b': u'ZLOB_INDEX (Index pages of compressed LOB)',
    '001c': u'ZLOB_FRAG (Fragment pages of compressed LOB)',
    '001d': u'ZLOB_FRAG_ENTRY (Index pages of fragment pages (compressed LOB))',
    '45bd': u'SDI (Tablespace SDI Index page)'
}

PAGE_CHECKSUM_LEN = 4
PAGE_OFFSET_LEN = 4
PAGE_PREV_LEN = 4
PAGE_NEXT_LEN = 4
PAGE_LSN_LEN = 8
PAGE_TYPE_LEN = 2
PAGE_FILE_FLUSH_LSN_LEN = 8
PAGE_ARCH_LOG_LEN = 4
FSD_HDR_SPCAE_ID_LEN = 4
FSD_HDR_NOT_USED_LEN = 4
FSD_HDR_SIZE_LEN = 4
FSD_HDR_FREE_LIMIT_LEN = 4
FSD_HDR_SPACE_FLAGS_LEN = 4
FSD_HDR_FLAG_N_USED_LEN = 4
INDEX_PAGE_LEVEL_LEN = 2
SPACE_FLAGS_ENCRYTION_OFFSET = 13
SPACE_FLAGS_PAGE_SSIZE_OFFSET = 6

# some global variables
# print 2 columns, The value is the width of each column in characters
printer = PrettyPrint(
    [{"width": 26, "align": "<"}, {"width": 40, "align": "<"}])


def ParseFile(file_path):
  # r+b mode is open the binary file in read or write mode.
  with open(file_path, "rb") as f:
    print("\n" + bcolors.OKGREEN + "Tablespace: " +
          os.path.splitext(os.path.basename(file_path))[0] + bcolors.ENDC)
    printer.PrintSplitRow()
    printer.PrintRow(["File properties", "Value"])
    printer.PrintSplitRow()

    fsize = os.path.getsize(f.name)
    printer.PrintRow(["Total bytes", fsize])
    # "//" is int division operator
    page_count = fsize//INNODB_PAGE_SIZE
    printer.PrintRow(["Total pages", page_count])
    printer.PrintSplitRow()

    for i in range(page_count):
      page = f.read(INNODB_PAGE_SIZE)
      # Parse the contents of each page
      ParsePage(i, page)


def ParsePage(idx, bytes):
  pos = 0

  checksum = bytes[pos:pos+PAGE_CHECKSUM_LEN]
  pos += PAGE_CHECKSUM_LEN

  offset = int.from_bytes(bytes[pos:pos+PAGE_OFFSET_LEN], "big")
  pos += PAGE_OFFSET_LEN

  prev = bytes[pos:pos+PAGE_PREV_LEN]
  pos += PAGE_PREV_LEN

  next = bytes[pos:pos+PAGE_NEXT_LEN]
  pos += PAGE_NEXT_LEN

  lsn = bytes[pos:pos+PAGE_LSN_LEN]
  pos += PAGE_LSN_LEN

  page_type = bytes[pos:pos+PAGE_TYPE_LEN]
  pos += PAGE_TYPE_LEN

  file_flush_lsn = bytes[pos:pos+PAGE_FILE_FLUSH_LSN_LEN]
  pos += PAGE_FILE_FLUSH_LSN_LEN

  arch_log_space = bytes[pos:pos+PAGE_ARCH_LOG_LEN]
  pos += PAGE_ARCH_LOG_LEN

  # print table header
  print("\n" + bcolors.OKGREEN + "Page " + str(idx) + bcolors.ENDC)
  printer.PrintSplitRow()
  printer.PrintRow(["Page properties", "Value"])
  printer.PrintSplitRow()
  # page_type = bytes[FIL_PAGE_TYPE:FIL_PAGE_TYPE+FIL_PAGE_TYPE_LEN]
  printer.PrintRow(["PAGE_TYPE", INNODB_PAGE_TYPE[page_type.hex()]])
  printer.PrintRow(["PAGE_ADDRESS", INNODB_PAGE_SIZE*offset])
  printer.PrintRow(["SPACE_OR_CHECKSUM", checksum.hex()])
  printer.PrintRow(["OFFSET", offset])
  printer.PrintRow(["PREV", prev.hex()])
  printer.PrintRow(["NEXT", next.hex()])
  printer.PrintRow(["LSN", lsn.hex()])
  printer.PrintRow(["FILE_FLUSH_LSN", file_flush_lsn.hex()])
  printer.PrintRow(["ARCH_LOG_NO_OR_SPACE_ID", arch_log_space.hex()])

  # Parse the contents of each specific page
  if page_type.hex() == '0008':
    ParseFSPHDRPage(bytes)
  elif page_type.hex() == '45bf':
    ParseINDEXPage(bytes)
  printer.PrintSplitRow()


def ParseFSPHDRPage(bytes):
  pos = FIL_PAGE_DATA

  space_id = bytes[pos:pos+FSD_HDR_SPCAE_ID_LEN]
  pos += FSD_HDR_SPCAE_ID_LEN

  not_used = bytes[pos:pos+FSD_HDR_NOT_USED_LEN]
  pos += FSD_HDR_NOT_USED_LEN

  size = int.from_bytes(bytes[pos:pos+FSD_HDR_SIZE_LEN], "big")
  pos += FSD_HDR_SIZE_LEN

  free_limit = bytes[pos:pos+FSD_HDR_FREE_LIMIT_LEN]
  pos += FSD_HDR_FREE_LIMIT_LEN

  space_flags = bytes[pos:pos+FSD_HDR_SPACE_FLAGS_LEN]
  pos += FSD_HDR_SPACE_FLAGS_LEN

  frag_n_used = bytes[pos:pos+FSD_HDR_FLAG_N_USED_LEN]
  pos += FSD_HDR_FLAG_N_USED_LEN

  printer.PrintRow(["SPACE_ID", space_id.hex()])
  printer.PrintRow(["SIZE", size])
  printer.PrintRow(["NOT_USED", not_used.hex()])
  printer.PrintRow(["FREE_LIMIT", free_limit.hex()])
  printer.PrintRow(["FRAG_N_USED", frag_n_used.hex()])
  printer.PrintRow(["SPACE_FLAGS", space_flags.hex()])
  # bits = [int(i) for i in "{0:08b}".format(space_flags[2])]
  # The encryption state is stored in the 14th bit of space_flags
  space_flags_val = int.from_bytes(space_flags, "big")
  printer.PrintRow(
      ["ENCRYPTION (加密状态)",  (space_flags_val >> SPACE_FLAGS_ENCRYTION_OFFSET) & 1])
  printer.PrintRow(
      ["PAGE_SSIZE",  (space_flags_val >> SPACE_FLAGS_PAGE_SSIZE_OFFSET) & 0x0f])


def ParseINDEXPage(bytes):
  pos = FIL_PAGE_DATA + PAGE_LEVEL

  len = INDEX_PAGE_LEVEL_LEN
  page_level = int.from_bytes(bytes[pos:pos+len], "big")
  pos += len
  printer.PrintRow(["PAGE_LEVEL", page_level])


def main(argv):
  parser = optparse.OptionParser("Usage: %prog [options] file")
  parser.add_option("-v", "--verbose", dest="verbose")
  # parse cmdline arguments to an object
  # then pass to main
  (options, args) = parser.parse_args()
  if len(args) != 1:
    parser.error("The argument of ibd file is missing.")
  file_path = os.path.realpath(args[0])
  ParseFile(file_path)


# Omitted when being used as module
if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
