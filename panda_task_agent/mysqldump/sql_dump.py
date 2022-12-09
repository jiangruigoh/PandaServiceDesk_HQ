# SQL DUMP 
"""
Version No: 1
Release Date: 18 October 2021 
KKSC
"""

import os
import time
from subprocess import Popen, PIPE, STDOUT
import subprocess

from sqlalchemy.sql.expression import table

def create_sqlfilename(store_code, date_code, hourly_code, sequence, dump_path):
    abs_path =  os.path.join(dump_path,store_code + "_" + \
               date_code + "_" +  \
               hourly_code + "_" +  \
               sequence + ".sql")
    return abs_path


def create_sqlfilename_only(store_code, date_code, hourly_code, sequence):
    filename =  store_code + "_" + \
                date_code + "_" +  \
                hourly_code + "_" +  \
                sequence + ".sql"
    return filename

class SqlDumper():
    def __init__(self):
        self.hostname = None
        self.port = None
        self.db_user = None
        self.db_pwd = None
        self.database_name = None
        self.table_main = None
        self.where_clause_main = None
        self.filename = None
        self.poll = ""
        self.pre_item = None
        self.end_item = None
        self.dump_path = None
        self.abs_dump_path = None
        self.filestamp = time.strftime('%Y-%m-%d-%I')
        self.branch_code = None
        self.date_code = None
        self.hourly_code = None
        self.sequence_no = None
        self.table_child1 = ""
        self.table_child2 = ""
        self.table_child3 = ""
        self.table_child4 = ""
        self.where_clause_child1 = ""
        self.where_clause_child2 = ""
        self.where_clause_child3 = ""
        self.where_clause_child4 = ""
        self.condition = ""
        self.tablename_to_dump = ""
        self.tables = None
    
    def dump(self):
        try:
            # -t, Do not write CREATE TABLE statements that create each dumped table.
            # self.filename = self.table_main+"_"+self.filestamp+".sql" # OLD FORMAT
            # self.filename = self.branch_code + self.date_code + self.hourly_code + self.sequence_no + ".sql" 
            # output_path_file = os.path.join(self.dump_path, self.filename)
            file = open(self.abs_dump_path, 'a')  # so that data written to it will be appended
            query = " /usr/bin/mysqldump -h %s -P %s -u %s -t --single-transaction --extended-insert -c --replace -p%s %s %s %s" \
                    %( self.hostname, self.port, self.db_user, self.db_pwd, self.database_name, \
                        self.tablename_to_dump, self.condition) 
            # p = os.popen(query)
            # print(query)
            # print(output_path_file)
            process = subprocess.Popen(query, stdout=file, shell=True)
            # stdoutdata, stderrdata = process.communicate()
            # print(stdoutdata)
            process.wait() # Ensures that SQLDUMP process finish before doing anything else
            file.close()
            returnCode = process.poll() 
            # process.terminate()
            print("Return Code" +  str(returnCode))
            # self.abs_dump_path = output_path_file
            return "DUMPED: " + " db_name: " +  str(self.database_name) +  \
                " table_name: " + str(self.tablename_to_dump) + " ," 
        except Exception as e:
            print(str(e))
            return "Dump process Fail"
    
    def no_tables_checkpoint(self):
        res = False
        if all(x in [None,"","None"] for x in self.tables):
            res = True
        return res

    
    def run(self):
        # D:/xampp/mysql/bin/mysqldump for xamp windows
        where_clause_list = [self.where_clause_main, self.where_clause_child1, self.where_clause_child2, \
                            self.where_clause_child3, self.where_clause_child4]
        table_name_list = [self.table_main, self.table_child1, self.table_child2, \
                            self.table_child3, self.table_child4]
        self.tables = table_name_list
        opt_res = ""
        # print(self.tables)
        # print(self.no_tables_checkpoint())
        try:
            if self.no_tables_checkpoint() == True: # IF no tables THEN Backup all tables
                res = self.dump()
                opt_res +=res
                return opt_res
            else:
                for i in range(len(where_clause_list)-1):
                    con_iter = where_clause_list[i]
                    self.tablename_to_dump = table_name_list[i]

                    # Base Casses
                    if con_iter == self.tablename_to_dump: 
                        continue
                    if (self.tablename_to_dump == "") or (self.tablename_to_dump == None) or (self.tablename_to_dump == "None"):
                        continue
                        
                    if (con_iter == "") or (con_iter == None) or (con_iter == "None"): # Handles Conditions
                        self.condition = ""
                        # print(self.tablename_to_dump, self.condition)
                        res = self.dump()
                        opt_res +=res
                    elif (con_iter !="") or (con_iter != None) or (con_iter != "None"):
                        self.condition = """ --where="%s" """%(con_iter)
                        # print(self.tablename_to_dump, self.condition)
                        res = self.dump()
                        opt_res +=res
                return opt_res
        except Exception as e:
            print(str(e))
            return "Dump process Fail"
            
    
    def appendin(self):
        # time.sleep(3)
        try:
            # Append to sqldump file
            # path_file = os.path.join(self.dump_path,self.filename)
            back_alter = open(self.abs_dump_path, "a")
            back_alter.write(self.end_item)
            back_alter.close()
            return "Sucessfully added post script: " + str(self.end_item) 
        except Exception as e:
            print(str(e))
            return "Append FAIL"
    
    def prependin(self):
        try:
            # PRE-Append to sqldump file
            #file = open(self.abs_dump_path, "r")
            #file.seek(0)
            #content = file.read()

            with open(self.abs_dump_path, "r") as file:
                file.seek(0)
                content = file.read()
            file.close()

            with open(self.abs_dump_path, "w") as new_file:
                new_file.write(self.pre_item + "\n" + "USE " + self.database_name + ";" + "\n" + content)
                new_file.seek(0)
            new_file.close()
            return "Sucessfully added pre-script: " + str(self.pre_item) 
        except Exception as e:
            print(str(e))
            return "PRE-append script FAIL"
    
    def path_checkpoint(self):
        res = "Path exist"
        try:
            path_existence = os.path.exists(self.dump_path)
            # print(self.dump_path)
            # print(path_existence)
            if path_existence == False:
                # print("No such Directory exist")
                # print("Proceed Creating new directoy")
                os.mkdir(self.dump_path)
                res = "New path directory created: " + str(self.dump_path)
        except Exception as e:
            # print(str(e))
            return str(e)
        return res

    def abs_path_join(self):
        try:
            self.abs_dump_path = os.path.join(self.dump_path, self.branch_code + "_" + \
                                                                self.date_code + "_" +  \
                                                                self.hourly_code + "_" +  \
                                                                self.sequence_no + ".sql" )
            return self.abs_dump_path
        except Exception as e:
            print(str(e))
            return "Path Issue"

    def file_checkpoint(self):
        try:
            res = os.path.exists(self.abs_dump_path)
            return res
        except Exception as e:
            # print(str(e))
            return str(e)
    
    def delete_exist(self):
        try:
            os.remove(self.abs_dump_path)
            return "Deleted Existing File"
        except Exception as e:
            print(str(e))
            return "Delete exisiting Fail"
