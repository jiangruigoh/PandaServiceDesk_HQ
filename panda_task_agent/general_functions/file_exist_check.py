"""
Version No: 1
Release Date: 22 September 2021 
KKSC
"""

import os
from os import error

def file_exist_checker(file_path, file_name):
    try:
        res = {"status": "success",
                            "data": {
                                "filename": file_name,
                                "filepath": file_path
                            },
                            "message": False,
                            "code": 200
                    }
        for path, dirs, files in os.walk(file_path):
            for i in range(len(files)):
                # print(files[i])
                if files[i] == file_name:
                    res = {"status": "success",
                            "data": {
                                "filename": file_name,
                                "filepath": file_path
                            },
                            "message": True,
                            "code": 200
                    }
                    
        return res
        
    except error as e:
        return {"status": "fail: " + str(e),
                "data": {
                    "filename": file_name,
                    "filepath": file_path
                },
                "message": False,
                "code": 422
        }