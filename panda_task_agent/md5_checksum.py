# Check file integrity
"""
Version No: 1
Release Date: 14 September 2021 
KKSC
"""

import hashlib
from os import error
import os

def cal_checksum(path, filename):
    try:
        abs_pth = os.path.join(path, filename)
        md5_hash = hashlib.md5()
        a_file = open(abs_pth, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        return { "data": str(digest),
                    "message": "success",
                    "path": str(path),
                    "filename": str(filename)}
    except error as e:
        return { "data": str(e),
                    "message": "fail",
                    "path": str(path),
                    "filename": str(filename)}

