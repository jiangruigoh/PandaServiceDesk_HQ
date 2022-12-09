"""
Version No: 1
Release Date: 15 September 2021 
KKSC
"""

import shutil
import os
import bz2
from panda_task_agent.compress_de_functions.zip_helper import check_bz2, check_dump_sql

def test_compress_file(write_filename):
    # To Test if Compressed files is fine
    try:
        bz2.BZ2File(write_filename).read()
        print('Intact')
        return "Intact"
    except IOError:
        print('Corrupted')
        return "Corrupted"

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def path_checker(path_assigned):
    path_existence = os.path.exists(path_assigned)
    return path_existence

def file_checker(path_to_zip, filename):
    file_status = False
    for path, dirs, files in os.walk(path_to_zip):
        for file_i in range(len(files)):
            # print(files[file_i], filename)
            if files[file_i] == filename:
                file_status = True
    return file_status

def bzip_unzipper(path_to_zip, filename, path_to_store):

    # Read_filename
    read_path_file = find_file(filename, path_to_zip)

    # Clean filename
    filename_split_type = filename.split(".")
    clean_filename = filename_split_type[0]

    # Join various path components
    write_path_file = os.path.join(path_to_store, clean_filename + ".sql")
    # print(write_path_file)

    with bz2.open(read_path_file, 'rb') as f_in:
        with open(write_path_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        f_out.close()
    f_in.close()
    
    return {
        "message": "Succesfully decompress " + filename
    }

def bzip_unzipper_agent(filename, source_path, path_store_zip):
    """
    param_1: path that contains the filename to be unzipped
    param_2: filename to be unzip
    """
    # Checks if path_to_store exist if not create new directory
    isExist_2 = path_checker(path_store_zip)
    if (isExist_2  == False):
        create_dir_status = create_new_dir(path_store_zip)
        """
        return { 
                 "path_to_store" : isExist_2,
                 "message": str(create_dir_status)
               }
        """
    # Check if file is already a compressed file
    if check_bz2(filename) == False:
        return "Please specify a proper bz2 compressed file"

    # Check Path Existence
    isExist_1 = path_checker(source_path)
    # print(isExist_1)
    # Check if paths parameters are correct
    if isExist_1  == False:
        return { 
                 "path_to_zip" : isExist_1,
                 "message": "Invalid Paths"
               }

    # Checks if filename parameter exist
    if isExist_1 == True:
        file_status = file_checker(source_path, filename)
        # print(file_status)

    if file_status == False:
        return { 
                "path_to_zip" : isExist_1,
                "message": "No Such filename exist in path"
                }
    
    if file_status == True:
        bzip_unzipper(source_path, filename, path_store_zip)

    return {
        "source_path" : source_path,
        "filename": filename,
        "message": "200"
    }

def bzip_zipper(path_to_zip, filename, path_to_store):
    """
    Read file and zip the file to assigned path
    """
    # Pre-Computation Phase (Cleaning Paths and Filenames)
    read_path_file = find_file(filename, path_to_zip)
    filename_split_type = filename.split(".")
    clean_filename = filename_split_type[0]

    # Join various path components
    write_filename = os.path.join(path_to_store, clean_filename + ".bz2")
    # print(write_filename)
    zip_filename = clean_filename + ".bz2"

    # 4.1 Delete Exsiting compress file
    if os.path.exists(write_filename) == True:
        os.remove(write_filename)

    with open(read_path_file, 'rb') as f_in:
        with bz2.open(write_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_out.close()
    f_in.close()

    test_compress = test_compress_file(write_filename)
    
    #if test_compress == "Corrupted":
    #    return {
    #        "message": "Corrupted"
    #    }

    return {
        "message": "Succesfully compressed " + filename,
        "zip_filename": str(zip_filename)
    }

def create_new_dir(path_to_store):
    status = "Store Directory already Exist"
    try:
        os.mkdir(path_to_store)
        status = "New path directory created: " + str(path_to_store)
    except Exception as e:
            # print(str(e))
            return str(e)
    return status


def bzip_zip_agent(filename, path_to_zip, path_store_zip):
    """
    param_1: filename
    param_2: the path for the filename
    param_2: the path used to store the zip file
    """

    # Check if file is already a compressed file
    #if check_dump_sql(filename) == False:
    #    return { 
    #             "message": "This is already a bz2 compressed file"
    #           }

    # Check Path Existence
    isExist_1 = path_checker(path_to_zip)
    isExist_2 = path_checker(path_store_zip)
    file_status = False
    # print(isExist_1, isExist_2)

    # IF storing path did not exist then create new  directory
    if (isExist_2  == False):
        create_dir_status = create_new_dir(path_store_zip)
        if "Store" in create_dir_status or "New" in create_dir_status:
            isExist_2 =True
        return { 
                 "path_to_store" : isExist_1,
                 "message": str(create_dir_status)
               }

    # Check if paths parameters are correct
    if (isExist_1  == False) :
        return { 
                 "path_to_zip" : isExist_1,
                 "message": "Invalid Path"
               }

    # Checks if filename parameter exist
    if (isExist_1 == True):
        file_status = file_checker(path_to_zip, filename)

    if file_status == False:
        return {
                "path_to_zip" : isExist_1,
                "path_to_store": isExist_2,
                "message": "No Such filename exist in path"
                }

    # Start bz2 compression process
    if file_status == True:
        zip_stat = bzip_zipper(path_to_zip, filename, path_store_zip)
        
    # SET back WORKING DIRECTORY After Completion
    # working_basename_abs = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(working_basename_abs)
    
    #print(file_opener())
    print(zip_stat)

    return { 
            "path_to_zip" : isExist_1,
            "path_to_store": isExist_2,
            "message": "200",
            "zip_filename": zip_stat["zip_filename"]
            }


"""
print(bzip_unzipper_agent("mrpreport-data-Friday.sql.bz2", \
                            "/media/karajan/Backup/dailybackup4/dailybackup/mrpreport",\
                            "/media/karajan/Backup/dailybackup4/dailybackup/mrpreport/to_store_zip"))

print(bzip_zip_agent("mrpreport-data-Friday.sql",
            "/media/karajan/Backup/dailybackup4/dailybackup/mrpreport/to_store_zip",
            "/media/karajan/Backup/dailybackup4/dailybackup/mrpreport/to_store_zip"))

print(bzip_zip_agent("backend-data-Monday.sql",
            "/media/karajan/Backup/dailybackup4/dailybackup/backend",
            "/media/karajan/Backup/dailybackup4/dailybackup/backend"))

"""
