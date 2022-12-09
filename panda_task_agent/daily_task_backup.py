"""
Version No: 1
Release Date: 23 September 2021 
KKSC
"""
# from daily_panda_task_agent import Daily_Panda_Task_Agent
from yaml_read_config import assign_config_values
from mysqldump.sql_dump import create_sqlfilename, create_sqlfilename_only
from mysqldump.script_append import check_file_exist
import time

def sqldump_run():
    # Initialize all defaul Params
    daily_task = assign_config_values()
    error_ctr = 0

    # STEP 1: List Task
    daily_task.tablename = "task_agent"
    daily_task.enable = 1

    daily_task.url =  daily_task.BASE_URL + "get_task_last_run"
    daily_task.url_obj = {
                            "database_name": daily_task.database_name,
                            "table_name": daily_task.tablename,
                            "enable_in": daily_task.enable,
                            "task_type_in": daily_task.task_type
                            }

    # STEP 2: Obtain each row for list task and assign values
    list_task_obj = daily_task.post_req()
    list_task = list_task_obj["active_task"]
    for task_i in range(len(list_task)):
        row = list_task[task_i]
        daily_task.source_database_name = row["source_database_name"]
        daily_task.source_table_name = row["source_table_name"]
        daily_task.target_database_name = row["target_database_name"]
        daily_task.target_table_name = row["target_table_name"]
        daily_task.table_main = str(row["table_main"])
        daily_task.table_child1 = str(row["table_child1"])
        daily_task.table_child2 = str(row["table_child2"])
        daily_task.table_child3 = str(row["table_child3"])
        daily_task.table_child4 = str(row["table_child4"])
        daily_task.save_file_pre_script = str(row["save_file_pre_script"])
        daily_task.save_file_post_script = str(row["save_file_post_script"])
        daily_task.where_main = str(row["where_main"])
        daily_task.where_child1 = str(row["where_child1"])
        daily_task.where_child2 = str(row["where_child2"])
        daily_task.where_child3 = str(row["where_child3"])
        daily_task.where_child4 = str(row["where_child4"])
        daily_task.task_guid = str(row["task_guid"])

        # STEP 3: Get sequence for naming filenames
        daily_task.tablename = "from_outlet" # Re-assign table to query from
        daily_task.url = daily_task.BASE_URL + "get_sequence_no"
        daily_task.url_obj = {
                            "database_name": daily_task.database_name,
                            "table_name": daily_task.tablename,
                            "store_code_in": daily_task.store_code,
                            "task_type_in": daily_task.task_type
                            }
        # print(daily_task.url_obj)
        file_items = daily_task.post_req()
        print(file_items)
        
        daily_task.hourly_code = file_items["hourly_code"]
        daily_task.sequence = file_items["last_sequence"]
        daily_task.date_code = file_items["date_code"]
        
        # STEP 4: DELETE previous existing file
        daily_task.dump_path_abs  = create_sqlfilename(daily_task.store_code, daily_task.date_code, \
                                    daily_task.hourly_code, daily_task.sequence, daily_task.dump_path)
        daily_task.dump_filename = create_sqlfilename_only(daily_task.store_code, daily_task.date_code, \
                                    daily_task.hourly_code, daily_task.sequence)
        check_file_exist(daily_task.dump_path_abs)
        
        start = time.time()
        # STEP 5: Pre-Append Script
        daily_task.url = daily_task.BASE_URL +  "pre_script_append"
        daily_task.url_obj = {
            "abs_path": daily_task.dump_path_abs,
            "pre_script": daily_task.save_file_pre_script,
            "database_name": daily_task.target_database_name
            }
        
        pre_script_status = daily_task.post_req()
        print(pre_script_status)
        
        # STEP 6: for EACH TASK along with SEQUENCE, Create DUMP
        daily_task.url = daily_task.BASE_URL + "sqldump"
        daily_task.url_obj = {
            "hostname": daily_task.d_hostname,
            "port": daily_task.d_port,
            "db_user": daily_task.d_username,
            "db_pwd": daily_task.d_pwd,
            "database_name": daily_task.source_database_name,
            "dump_path": daily_task.dump_path,
            "pre_execute_script": daily_task.save_file_pre_script,
            "post_execute_script": daily_task.save_file_post_script,
            "branch_code": daily_task.store_code,
            "date_code": daily_task.date_code,
            "hourly_code": daily_task.hourly_code,
            "sequence_no": daily_task.sequence,
            "table_main": daily_task.table_main,
            "main_where_clause": daily_task.where_main,
            "table_child1": daily_task.table_child1,
            "where_child1": daily_task.where_child1,
            "table_child2": daily_task.table_child2,
            "where_child2": daily_task.where_child2,
            "table_child3": daily_task.table_child3,
            "where_child3": daily_task.where_child3,
            "table_child4": daily_task.table_child4,
            "where_child4": daily_task.where_child4
            }

        # print(daily_task.url_obj)
        dumped_result = daily_task.post_req()
        dumped_path_status = dumped_result['dump_path_status']
        sqldump_status = dumped_result['sqldump_status']
        # print(dumped_result)

        # STEP 7: Append Script
        daily_task.url = daily_task.BASE_URL + "post_script_append"
        daily_task.url_obj = {
            "abs_path": daily_task.dump_path_abs,
            "post_script": daily_task.save_file_post_script
            }
            
        post_script_status = daily_task.post_req()
        print(post_script_status)
        end = time.time()

        # CALCULATES Checksum for sqldumped file .sql
        daily_task.url = daily_task.BASE_URL + "cal_MD5_checksum"
        daily_task.url_obj = {
                            "filename_path": daily_task.dump_path,
                            "filename": daily_task.dump_filename
                            }
        md5_digest_sql_res = daily_task.post_req()
        print(md5_digest_sql_res)
        md5_data_sql = md5_digest_sql_res["data"]
        md5_status_sql = md5_digest_sql_res["message"]
        
        if md5_status_sql == "fail":
            error_ctr = 1

        # STEP 8: Create new record at from_outlet aka panda_upload
        if 'exist' in dumped_path_status and \
            "DUMPED" in sqldump_status and "Sucessfully" in pre_script_status and\
            "Sucessfully" in post_script_status:
            sqldump_status = "Successfully Dumped"
            daily_task.url = daily_task.BASE_URL + "create_task_agent"
            daily_task.tablename = "from_outlet"
            daily_task.url_obj = {
                    "database_name": daily_task.database_name,
                    "tablename": daily_task.tablename,
                    "task_type": daily_task.task_type,
                    "store_code": daily_task.store_code,
                    "date_code": daily_task.date_code,
                    "hourly_code": daily_task.hourly_code,
                    "sequence": daily_task.sequence,
                    "task_status": 0,
                    "source_database_name": daily_task.source_database_name,
                    "source_table_name": daily_task.source_table_name,
                    "uncompress_checksum": md5_data_sql,
                    "compress_checksum": "",
                    "error": error_ctr,
                    "resolve": 0
                    }
            
            task_upload_status = daily_task.post_req()
            print(task_upload_status)
        else:
            sqldump_status = "Failed dump"
            print("Mysqldump failure")

        executed_time = str(round(end-start,2))
        if "Successfully" in sqldump_status:
            daily_task.tablename = "task_agent"
            daily_task.url = daily_task.BASE_URL +"task_status_update"
            daily_task.url_obj = {
                "database_name": daily_task.database_name,
                "table_name": daily_task.tablename,
                "task_guid": daily_task.task_guid,
                "execute_time": executed_time
                }
            task_upload_status = daily_task.post_req()


    
