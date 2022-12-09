# Function to test if health of zip files are fine
import bz2
import gzip
import os

def check_dump_sql(filename):
    if filename.endswith(".bz2") or filename.endswith(".gz"):
        return False
    else:
        return True

def check_bz2(filename):
    if filename.endswith(".bz2"):
        return True
    else:
        return False

def check_gz(filename):
    if filename.endswith(".gz"):
        return True
    else:
        return False

def gz_check(filename):
    try:
        gzip.open(filename).read()
        # print('Intact')
        return "Intact"
    except IOError:
        # print('Corrupted')
        return "Corrupted"

def bz_check(filename):
    try:
        bz2.BZ2File(filename).read()
        # print('Intact')
        return "Intact"
    except IOError:
        # print('Corrupted')
        return "Corrupted"

class Health_Check_Compressed(object):
    def __init__(self):
        self.filename = None
        self.file_path = None
        self.working_dir_path = os.path.dirname(os.path.abspath(__file__))

    def check(self):
        # To Test if Compressed files is fine
        os.chdir(self.file_path)
        if self.filename.endswith(".bz") or self.filename.endswith(".bz2"):
            result = bz_check(self.filename)
            os.chdir(self.working_dir_path)
            return result
        elif self.filename.endswith(".gz"):
            result = gz_check(self.filename)
            os.chdir(self.working_dir_path)
            return result
        else:
            os.chdir(self.working_dir_path)
            return "Please select files with bz or gz compression type"
        
"""
# TESTING SCRIPT
health = Health_Check_Compressed()
health.filename = "backend-schema-Monday.sql.bz2"
health.file_path = "/media/karajan/Backup/dailybackup4/dailybackup/backend"
print(health.check())
print(os.path.dirname(os.path.abspath(__file__)))
"""