# mysql-utils
A toolbox for mysql database

## Parse ibd tablespace file

```shell
Usage: parse_ibd.py [options] file
```

The console output:

```shell

Tablespace: t_user
+--------------------------+----------------------------------------+
| File properties          | Value                                  |
+--------------------------+----------------------------------------+
| Total bytes              | 98304                                  |
| Total pages              | 6                                      |
+--------------------------+----------------------------------------+

Page 0
+--------------------------+----------------------------------------+
| Page properties          | Value                                  |
+--------------------------+----------------------------------------+
| PAGE_TYPE                | FSP_HDR (File Space Header)            |
| PAGE_ADDRESS             | 0                                      |
| SPACE_OR_CHECKSUM        | 2934ee83                               |
| OFFSET                   | 0                                      |
| PREV                     | 00000000                               |
| NEXT                     | 00000000                               |
| LSN                      | 000000096abd1ada                       |
| FILE_FLUSH_LSN           | 0000000000000000                       |
| ARCH_LOG_NO_OR_SPACE_ID  | 00000c23                               |
| SPACE_ID                 | 00000c23                               |
| SIZE                     | 6                                      |
| NOT_USED                 | 00000000                               |
| FREE_LIMIT               | 00000040                               |
| FRAG_N_USED              | 00000004                               |
| SPACE_FLAGS              | 00000021                               |
| ENCRYPTION (加密状态)    | 0                                      |
| PAGE_SSIZE               | 0                                      |
+--------------------------+----------------------------------------+

Page 1
+--------------------------+----------------------------------------+
| Page properties          | Value                                  |
+--------------------------+----------------------------------------+
| PAGE_TYPE                | IBUF_BITMAP (Insert Buffer Bitmap)     |
| PAGE_ADDRESS             | 16384                                  |
| SPACE_OR_CHECKSUM        | 9348006d                               |
| OFFSET                   | 1                                      |
| PREV                     | 00000000                               |
| NEXT                     | 00000000                               |
| LSN                      | 000000096abd0d16                       |
| FILE_FLUSH_LSN           | 0000000000000000                       |
| ARCH_LOG_NO_OR_SPACE_ID  | 00000c23                               |
+--------------------------+----------------------------------------+

Page 2
+--------------------------+----------------------------------------+
| Page properties          | Value                                  |
+--------------------------+----------------------------------------+
| PAGE_TYPE                | INODE (Index node)                     |
| PAGE_ADDRESS             | 32768                                  |
| SPACE_OR_CHECKSUM        | c098d205                               |
| OFFSET                   | 2                                      |
| PREV                     | 00000000                               |
| NEXT                     | 00000000                               |
| LSN                      | 000000096abd1ada                       |
| FILE_FLUSH_LSN           | 0000000000000000                       |
| ARCH_LOG_NO_OR_SPACE_ID  | 00000c23                               |
+--------------------------+----------------------------------------+

Page 3
+--------------------------+----------------------------------------+
| Page properties          | Value                                  |
+--------------------------+----------------------------------------+
| PAGE_TYPE                | INDEX (B-tree node)                    |
| PAGE_ADDRESS             | 49152                                  |
| SPACE_OR_CHECKSUM        | 2adff3cd                               |
| OFFSET                   | 3                                      |
| PREV                     | ffffffff                               |
| NEXT                     | ffffffff                               |
| LSN                      | 000000096abd2b4c                       |
| FILE_FLUSH_LSN           | 0000000000000000                       |
| ARCH_LOG_NO_OR_SPACE_ID  | 00000c23                               |
| PAGE_LEVEL               | 0                                      |
+--------------------------+----------------------------------------+

Page 4
+--------------------------+----------------------------------------+
| Page properties          | Value                                  |
+--------------------------+----------------------------------------+
| PAGE_TYPE                | ALLOCATED (Freshly Allocated Page)     |
| PAGE_ADDRESS             | 0                                      |
| SPACE_OR_CHECKSUM        | 00000000                               |
| OFFSET                   | 0                                      |
| PREV                     | 00000000                               |
| NEXT                     | 00000000                               |
| LSN                      | 0000000000000000                       |
| FILE_FLUSH_LSN           | 0000000000000000                       |
| ARCH_LOG_NO_OR_SPACE_ID  | 00000000                               |
+--------------------------+----------------------------------------+

Page 5
+--------------------------+----------------------------------------+
| Page properties          | Value                                  |
+--------------------------+----------------------------------------+
| PAGE_TYPE                | ALLOCATED (Freshly Allocated Page)     |
| PAGE_ADDRESS             | 0                                      |
| SPACE_OR_CHECKSUM        | 00000000                               |
| OFFSET                   | 0                                      |
| PREV                     | 00000000                               |
| NEXT                     | 00000000                               |
| LSN                      | 0000000000000000                       |
| FILE_FLUSH_LSN           | 0000000000000000                       |
| ARCH_LOG_NO_OR_SPACE_ID  | 00000000                               |
+--------------------------+----------------------------------------+
```

## Parse keyring file

```shell
Usage: parse_keyring.py [options] file
```

The console output:

```shell
+------------------+----------------------------------------+
| File properties  | Value                                  |
+------------------+----------------------------------------+
| Total bytes      | 363                                    |
| Version bytes    | 21                                     |
| Version          | Keyring file version:1.0               |
+------------------+----------------------------------------+

Key 0: 72 bytes (include LENGTH_DESP 40 bytes)
+--------------+--------+--------------------------------------------------------------------+
| Field        | Length | Data                                                               |
+--------------+--------+--------------------------------------------------------------------+
| KEY_ID       |      1 | x                                                                  |
| KEY_TYPE     |      3 | AES                                                                |
| USER_ID      |      6 | root@%                                                             |
| KEY_DATA     |     16 | 8117ad41443a191866a17fc794770387                                   |
| ACTUAL_KEY   |     16 | ab249d747976736c568b5e87b03f6dea                                   |
| PADDING      |      6 | 0                                                                  |
+--------------+--------+--------------------------------------------------------------------+

Key 1: 128 bytes (include LENGTH_DESP 40 bytes)
+--------------+--------+--------------------------------------------------------------------+
| Field        | Length | Data                                                               |
+--------------+--------+--------------------------------------------------------------------+
| KEY_ID       |     48 | INNODBKey-5ee6e0b4-11c8-11ea-8162-5a712873cba1-1                   |
| KEY_TYPE     |      3 | AES                                                                |
| USER_ID      |      0 |                                                                    |
| KEY_DATA     |     32 | 49a27eba9594c4703fbf61f6c11de780d3fe22fc85e03b48de3f94d00f146263   |
| ACTUAL_KEY   |     32 | 63914e8fa8d8ae040f9540b6e55589edfbd40fc5a8970072f40ca4e532580817   |
| PADDING      |      5 | 0                                                                  |
+--------------+--------+--------------------------------------------------------------------+

Key 2: 136 bytes (include LENGTH_DESP 40 bytes)
+--------------+--------+--------------------------------------------------------------------+
| Field        | Length | Data                                                               |
+--------------+--------+--------------------------------------------------------------------+
| KEY_ID       |     48 | INNODBKey-5ee6e0b4-11c8-11ea-8162-5a712873cba1-x                   |
| KEY_TYPE     |      3 | AES                                                                |
| USER_ID      |      6 | root@%                                                             |
| KEY_DATA     |     32 | 49a27eba9594c4703fbf61f6c11de780d3fe22fc85e03b48de3f94d00f146263   |
| ACTUAL_KEY   |     32 | 63914e8fa8d8ae040f9540b6e55589edfbd40fc5a8970072f40ca4e532580817   |
| PADDING      |      7 | 0                                                                  |
+--------------+--------+--------------------------------------------------------------------+

Reached end symbol: b'EOF'
```

## Decrypt ibd tablespace file

```shell
Usage: decrypt_ibd.py [options] file

Options:
  -h, --help            show this help message and exit
  -k MASTER_KEY, --key=MASTER_KEY
  -p PAGE, --page=PAGE  
  -v VERSION, --ver=VERSION
```

The console output:

```shell
table key: 
bb980325d0da64ccfaa7f1785890757100283e93a2cd1b15771f75744e7eed40
--> real key: 
3f71021468c0948c076f2acf2896acc46b25d95b2b09ad9918e5e9ce8ee110f3
iv: 
f768850efb3c44301033ad48a7c05323d6c2a63bb407308a67fe711fb8cc81c3
--> real key: 
382325f2d537d72cb82f14d2d3314afa4e492399546bc332c94b53be2f9f7151
table cipher text (1024 bytes): 
fcf2e3bb36985c807acba6400b7e539ba1bfff1d23e3dc73699792ecd927793413970d979c8944b7d071e72f2bb6270fd74ad3ea6d4f25e8a5534ba10d260c4fb64adbff50a5521ac5b78f24a8a903688756ae2f564868c0ebe5a4ef1fd45b2872f1b86643b65d9abcefd6b6ca1bae7b69e5014e2298cbb9d85399c691234b2c92406ce4d38067535acebdfbbd424ec6aed9c1e0561c52808928cc861b6261c0f650427aa9c01c8c2cbbf7f1daa9499eb37d232678c7a80cece91e882346d59a1aed0c185f0109153e7371362c15f229e29075543745e33d32f11702e4c7fd30ba6b0e5803d93a634cd483e8755c7a3f7e14e010312acd693ae8ca10fd702b459018585ed9e9c269f5f066280313831c7581287821208bd5ddd1756fa406ef9e79e25d5a837aba6e53e9bb4e167e7014894311c2862fa3e9a77ff4a8b7d1a0d6abc07e0c78dbd394294b4021446ae776125c360c800290de6005b6679a3bd31634b72b4a4804c10dc3485b1838e55c240dd235433c39f62a189afc113924ddaeb63a1fcd3c5b4fd37dab34946f604e785aaf18a9be02094fdca33ee13e88dd7f03d87c00a07f2b85981711b3bb7d82aff1ff15788dc4ca6caf478e263f6307d08aea37b49b2ddc6f319527da040eb498c28afade96b142460e95466a1d801b1bd745801d4b9b9004f07fceedfc091e842907d5c78575c7dfc70959071dedd8db6dfe361a7c1b00fb6a1ea4cb225bc445a981e7d46f698894bda195994199c3d5e1074bb57755fbedeb20eeb846e4fe1175d4054120b2fd4e8df34d8ba04cb483227031cb6ed11be3997190b0b452a58f9f6e8871b0f6bcbad20bd3156175f9a8e8356a3c76ebd69c7ad7ecdbeaf043f267e75f21bb582cd9dfb37f4e151fe77744b2b0d0244a382f6851e5ff515046afa15393d7b928f414a8e613748bed6d449008bd13e3e4d28029d5cd13279411d683e302dc60dfb0541f3f2f8c6b652fe2bb8e98a87fed201658d8e058d53ab2d9399dd2d507d2c2af2b2689a226e6d897d2e9ebef51446fba4eedfdaf01c85bd23c05c4e53ab24019cd9ba84c54efcc115976eae211499724eda4bc9ec64bbae477770434f3843a1132db7234eae1d7e09b2dca9978fd55ed4c9fcc14d9b7d47b7a543c9637f116edc1008c42f9f22686e685f7eeb3f5eaa472443a80126665e7b7d55079a97fdc0ecf8b2f016c0bb04f0a7a90c89db2202f7f829a47cf0efd25854d10681aa355fefd18e4db38ad9e1060f6903593b09b701dad69b0d5e6d75f048b7cc0af001f6526d694f2d4915ad7c783fb814f79ee7ae405a093d3d2756d281e03c1be0ee28fc4eed553cc71d1586e942fda824608e8521389c7dfddc8bab9ffe505eab34ac3525510779b3a72bd87d88ee1c5814028c393f46e4a5c1ad09a438fe57bd04878ea8b5423373ce107
table palin text: 
infimum
       supremum!AmanageraaACEObb Ahrcc( Aworkerdd0!Afinanceee8ÿVAitff
```
## Dependency

The script `decrypt_ibd.py` that decrypt table data requires `cryptography` installed:

```shell
pip3 install cryptography
```