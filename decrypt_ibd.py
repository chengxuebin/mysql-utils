#!/usr/bin/env python3
# encoding=utf-8

"""innodb tablespace file decrypt script.

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
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

if sys.version_info < (3, 0):
  sys.exit("Requires Python 3.0 or later.")

# some constants
# default page size 16k
PAGE_SIZE = 0x4000
# the start address of encryption info
ENCRYPTION_INFO_POSITION = 10390
# key、iv offset according to encrytion_info
KEY_IV_OFFSET_57 = 47
KEY_IV_OFFSET_80 = 43
# the storage lengths of key and iv
KEY_IV_LEN = 32
# the real length of iv
ACTUAL_IV_LEN = 16
# the offset of encrypted data in page
ENCRYPTION_OFFSET_IN_PAGE = 38
# the page index used for data
DATA_PAGE_57 = 3
DATA_PAGE_80 = 4
# the bytes to be decrypted
DECRYPTION_LEN = 1024

title_format = bcolors.OKGREEN + "{}: " + bcolors.ENDC


def DecryptFile(file_path, master_key, version, page):
  if (page == None):
    page = (DATA_PAGE_57 if version == '5.7' else DATA_PAGE_80)
  page = int(page)

  # r+b mode is open the binary file in read or write mode.
  with open(file_path, "rb") as f:
    # read key、iv
    f.seek(ENCRYPTION_INFO_POSITION +
           (KEY_IV_OFFSET_57 if version == '5.7' else KEY_IV_OFFSET_80))
    table_key_cipher = f.read(KEY_IV_LEN)
    iv_cipher = f.read(KEY_IV_LEN)
    # decrypt key、iv
    table_key = AesDecrypt(master_key, table_key_cipher, modes.ECB())
    iv = AesDecrypt(master_key, iv_cipher, modes.ECB())
    print(title_format.format("table key"))
    print(table_key_cipher.hex())
    print(title_format.format("--> real key"))
    print(table_key.hex())
    print(title_format.format("iv"))
    print(iv_cipher.hex())
    print(title_format.format("--> real key"))
    print(iv.hex())

    # Read the first N bytes
    f.seek(PAGE_SIZE*page + ENCRYPTION_OFFSET_IN_PAGE, 0)
    cipher_text = f.read(DECRYPTION_LEN)
    print(title_format.format(
        "table cipher text (" + str(DECRYPTION_LEN) + " bytes)"))
    print(cipher_text.hex())

    plain_text = AesDecrypt(table_key, cipher_text,
                            modes.CBC(iv[0:ACTUAL_IV_LEN]))
    print(title_format.format("table palin text"))
    print(plain_text.decode('latin-1'))


def AesEncrypt(key, input, mode):
  encryptor = Cipher(algorithms.AES(key), mode).encryptor()
  return encryptor.update(input) + encryptor.finalize()


def AesDecrypt(key, input, mode):
  encryptor = Cipher(algorithms.AES(key), mode).decryptor()
  return encryptor.update(input) + encryptor.finalize()


def main(argv):
  parser = optparse.OptionParser("Usage: %prog [options] file")
  parser.add_option("-k", "--key", dest="master_key")
  parser.add_option("-p", "--page", dest="page")
  parser.add_option("-v", "--ver", dest="version", default="5.7")
  # parse cmdline arguments to an object
  # then pass to main
  (options, args) = parser.parse_args()
  if len(args) != 1:
    parser.error("The argument of ibd file is missing.")
  file_path = os.path.realpath(args[0])

  if not os.path.exists(file_path):
    parser.error("The argument of ibd file does not exist.")

  if options.master_key == None:
    parser.error("The argument of master key is missing.")

  DecryptFile(file_path, bytes.fromhex(options.master_key),
              options.version, options.page)


# Omitted when being used as module
if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
