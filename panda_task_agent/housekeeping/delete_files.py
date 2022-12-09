"""
Version No: 1
Release Date:  1 October 2021
KKSC
"""

import os 
from os import error
from datetime import datetime

def delete_files_dates(FILE_PATH, START_DATE, END_DATE):#, START_DATE, END_DATE):
    try:
        file_lst = []
        for path, dirs, files in os.walk(FILE_PATH):
            for i in range(len(files)):
                abs_path_file = os.path.join(path, files[i])
                # print(files[i])
                time_update = int(os.path.getmtime(abs_path_file))
                timestamp = datetime.fromtimestamp(time_update)
                last_modified = str(timestamp).split(" ")[0]
                # print(last_modified)
                # print("Filename: " + str(files[i]) + " Timestamp: " + str(timestamp))
                if last_modified >= START_DATE and last_modified <=END_DATE and \
                    files[i].endswith(".py"):
                    # print("Filename: " + str(files[i]) + " LastModified: " + str(last_modified))
                    file_lst.append(str(files[i]))

        res = {"status": "success",
                "data": {
                    "filepath": FILE_PATH,
                    "start_date": START_DATE,
                    "end_date": END_DATE,
                    "files_deleted": file_lst
                },
                "message": True,
                "code": 200
        }

        return res
        
    except error as e:
        return {"status": "fail: " + str(e),
                "data": {
                    "filepath": FILE_PATH,
                    "start_date": START_DATE,
                    "end_date": END_DATE,
                    "files_deleted": file_lst
                },
                "message": False,
                "code": 422
        }


def delete_file_abs(path, filename):
    try:
        abs_file_path = os.path.join(path, filename)
        os.remove(abs_file_path)
        return {"status": "SUCCESS",
                "data": {
                    "files_deleted": abs_file_path
                },
                "message": True,
                "code": 200
        }
    

    except error as e:
        return {"status": "fail: " + str(e),
                "data": {
                    "files_deleted": abs_file_path
                },
                "message": False,
                "code": 422
        }