"""
Version No: 1
Release Date: 23 September 2021 
KKSC
"""
import os

def check_file_exist(abs_path_file):
    try:
        res = os.path.exists(abs_path_file)
        if res == True:
            os.remove(abs_path_file)
        return True
    except Exception as e:
        # print(str(e))
        return str(e)

def pre_append(abs_path, pre_script, database_name):
    try:
        # PRE-Append to sqldump file
        #file = open(self.abs_dump_path, "r")
        #file.seek(0)
        #content = file.read()

        #with open(abs_path, "r") as file:
        #    file.seek(0)
        #    content = file.read()
        #file.close()

        with open(abs_path, "w") as new_file:
            new_file.write("USE " + database_name + ";" + "\n" + pre_script + "\n")
            # new_file.seek(0)
        new_file.close()
        return "Sucessfully added pre-script: " + str(pre_script) 
    except Exception as e:
        print(str(e))
        return "PRE-append script FAIL"

def post_append(abs_path, post_script):
        try:
            back_alter = open(abs_path, "a")
            back_alter.write(post_script)
            back_alter.close()
            return "Sucessfully added post script: " + str(post_script) 
        except Exception as e:
            print(str(e))
            return "Append FAIL"