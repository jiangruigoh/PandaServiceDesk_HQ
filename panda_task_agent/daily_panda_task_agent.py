"""
Version No: 1
Release Date: 14 September 2021 
KKSC
"""

from os import error
import requests
import os

class Daily_Panda_Task_Agent(object):
    def __init__(self):
        self.BASE_URL = ""#"http://office.panda-eco.com:60001/"
        self.REMOTE_BASE_URL = ""#"http://192.168.9.244:60002/"
        self.sequence = ""
        self.task_type = ""#"daily"
        self.store_code = ""#"PANDA"
        self.branch_code = ""
        self.database_name = ""#"batch_script_agent"
        self.tablename = ""
        self.enable = ""
        self.url = ""
        self.url_obj = ""
        self.url_data = ""
        self.table_main = ""
        self.table_child1 = ""
        self.table_child2 = ""
        self.table_child3 = ""
        self.table_child4 = ""
        self.save_file_pre_script = ""
        self.save_file_post_script = ""
        self.source_database_name = ""
        self.source_table_name = ""
        self.target_database_name = ""
        self.target_table_name = ""
        self.hourly_code = ""
        self.date_code = ""
        self.task_guid = ""

        # SQL Dump Defaults
        self.dump_path = ""#"/media/data/fastAPI/PandaServiceDesk/SQLDUMP_files"
        self.d_hostname = ""#"localhost"
        self.d_port = ""#"3306"
        self.d_username = ""#"panda_support"
        self.d_pwd =  ""#"nimdaadnap"
        self.main_clause = ""
        self.where_main = ""
        self.where_child1 = ""
        self.where_child2 = ""
        self.where_child3 = ""
        self.where_child4 = ""
        self.dump_path_abs = ""
        self.dump_filename = ""

        # ZIP Defaults
        self.zip_store_path = ""#"/media/data/fastAPI/PandaServiceDesk/SQLDUMP_files/compress"
        self.unzip_store_path = ""

        # SFTP Defaults
        self.sftp_hostname =  ""#"192.168.9.244"
        self.sftp_username =  ""#"panda"
        self.sftp_password =  ""#"adnap"
        self.sftp_remote_path =   ""#"/home/panda/test_SFTP/Test_dir"
        self.sftp_port =  ""#22

    def post_req(self):
        try:
            response = requests.post(self.url, json = self.url_obj, params=self.url_data)
            # print(response.json())
            response_data = response.json()
            return response_data
        except error as e:
            return e
    
    def create_filename_only_sql(self):
        try:
            filename =  self.store_code + "_" + \
                        self.date_code + "_" +  \
                        self.hourly_code + "_" +  \
                        str(int(self.sequence)).zfill(4) + ".sql"
            return filename
        except error as e:
            return e
    
    def create_filename_only_bz2(self):
        try:
            filename =  self.store_code + "_" + \
                        self.date_code + "_" +  \
                        self.hourly_code + "_" +  \
                        str(int(self.sequence)).zfill(4) + ".bz2"
            return filename
        except error as e:
            return e

    def check_file_exist(self):
        try:
            res = {"status": "success",
                                "data": {
                                    "filename": self.file_name,
                                    "filepath": self.file_path
                                },
                                "message": False,
                                "code": 200
                        }
            for path, dirs, files in os.walk(self.file_path):
                for i in range(len(files)):
                    print(files[i])
                    if files[i] == self.file_name:
                        res = {"status": "success",
                                "data": {
                                    "filename": self.file_name,
                                    "filepath": self.file_path
                                },
                                "message": True,
                                "code": 200
                        }
                        
            return res
        
        except error as e:
            return {"status": "fail",
                    "data": {
                        "filename": self.file_name,
                        "filepath": self.file_path
                    },
                    "message": False,
                    "code": 422
            }
