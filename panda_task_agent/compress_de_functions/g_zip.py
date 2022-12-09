# ZIP SCRIPT
"""
Version No: 1
Release Date: 20 August 2021 
KKSC
"""

import shutil
import os
import gzip
from panda_task_agent.compress_de_functions.zip_helper import check_gz, check_dump_sql

def test_compress_file(write_filename):
    # To Test if Compressed files is fine
    try:
        gzip.open(write_filename).read()
        print('Intact')
        return "Intact"
    except IOError:
        print('Corrupted')
        return "Corrupted"

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

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
                
def zipper(path_to_zip, filename, path_to_store):
    """
    Read file and zip the file to assigned path
    """
    # Pre-Computation Phase (Cleaning Paths and Filenames)
    read_path_file = find_file(filename, path_to_zip)
    filename_split_type = filename.split(".")
    clean_filename = filename_split_type[0]

    # Join various path components
    write_filename = os.path.join(path_to_store, clean_filename + ".gz")
    # print(write_filename)

    # 4.1 Delete Exsiting compress file
    if os.path.exists(write_filename) == True:
        os.remove(write_filename)
    
    with open(read_path_file, 'rb') as f_in:
        with gzip.open(write_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_out.close()
    f_in.close()

    test_compress = test_compress_file(write_filename)

    if test_compress == "Corrupted":
        return {
            "message": "Corrupted"
        }

    
    return {
        "message": "Succesfully compressed " + filename
    }

def unzipper(path_to_zip, filename, path_to_store):
    """
    Read File and Decompress 
    """

    # Pre-Computation Phase (Cleaning Paths and Filenames)

    # Read_filename
    read_path_file = find_file(filename, path_to_zip)

    # Clean filename
    filename_split_type = filename.split(".")
    clean_filename = filename_split_type[0]

    # Join various path components
    write_path_file = os.path.join(path_to_store, clean_filename + ".sql")
    # print(write_path_file)

    with gzip.open(read_path_file, 'rb') as f_in:
        with open(write_path_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        f_out.close()
    f_in.close()
    
    return {
        "message": "Succesfully decompress " + filename
    }

def unzipper_agent(filename, source_path, path_store_zip):
    """
    param_1: path that contains the filename to be unzipped
    param_2: filename to be unzip
    """

    # Check if file is already a compressed file
    if check_gz(filename) == False:
        return "Please specify a proper gz compressed file"

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

        print(file_status)

    if file_status == False:
        return { 
                "path_to_zip" : isExist_1,
                "message": "No Such filename exist in path"
                }
    
    if file_status == True:
        unzipper(source_path, filename, path_store_zip)

    return {
        "source_path" : source_path,
        "filename": filename,
        "message": "200"
    }

def zip_agent(filename, path_to_zip, path_store_zip):
    """
    param_1: filename
    param_2: the path for the filename
    param_2: the path used to store the zip file
    """

    # Check if file is already a compressed file
    if check_dump_sql(filename) == False:
        return "This is already a bz2 compressed file"

    # Check Path Existence
    isExist_1 = path_checker(path_to_zip)
    isExist_2 = path_checker(path_store_zip)
    file_status = False
    # print(isExist_1, isExist_2)

    # Check if paths parameters are correct
    if (isExist_1  == False) or (isExist_2 == False):
        return { 
                 "path_to_zip" : isExist_1,
                 "path_to_store": isExist_2,
                 "message": "Invalid Paths"
               }

    # Checks if filename parameter exist
    if (isExist_1 == True) and (isExist_2 == True):
        file_status = file_checker(path_to_zip, filename)

    if file_status == False:
        return {
                "path_to_zip" : isExist_1,
                "path_to_store": isExist_2,
                "message": "No Such filename exist in path"
                }

    # Start G-ZIP process
    if file_status == True:
        zipper(path_to_zip, filename, path_store_zip)
        
    # SET back WORKING DIRECTORY After Completion
    # working_basename_abs = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(working_basename_abs)
    
    #print(file_opener())
    return { 
            "path_to_zip" : isExist_1,
            "path_to_store": isExist_2,
            "message": "200"
            }


# TEST BELOW
"""
# COMPRESS
print(zip_agent(
    "sqlserver_sqlscript.sql",
    "/media/karajan/Backup/18 June 2021/", 
    "/media/karajan/Backup/18 June 2021/store_zip"
))

# DECOMPRESS
print(unzipper_agent(
    "sqlserver_sqlscript.gz",
    "/media/karajan/Backup/18 June 2021/store_zip/",
    "/media/karajan/Backup/18 June 2021/store_unzip"
))
"""