"""
# Uncompressor
Version No: 1
Release Date: 2 October 2021 
KKSC
"""

# from daily_panda_task_agent import Daily_Panda_Task_Agent
from yaml_read_config import assign_config_values
from housekeeping.delete_files import delete_file_abs

def restore_uncompress():
    # Initialize all defaul Params
    filename_list = []
    sql_filename_list =[]
    daily_task = assign_config_values()
    daily_task.file_path = daily_task.zip_store_path
    # ========= STEP 1: GET from_outlet record,  STATUS ==1, Errror column checkpoint ========= #
    """ IF task_status ==1  AND error ==0 THEN GO next step
        IF error ==1 THEN SKIP """
    daily_task.url = daily_task.BASE_URL + "get_task_status"
    daily_task.tablename = "from_outlet"
    daily_task.url_obj = {
      "database_name": daily_task.database_name,
      "table_name": daily_task.tablename,
      "task_status_value": 1,
      "ascending": "true"
    }
    # print(daily_task.url)
    task_status_1 = daily_task.post_req()
    task_records = task_status_1['data']
    # print(task_records)

    for row in range(len(task_records)):
        row_item = task_records[row]
        error_value = row_item['error']
        # print(daily_task.create_filename_only())

        if error_value == 1:
            continue # ERROR THEN SKIP
        else:
            # filename_list.append(daily_task.create_filename_only_bz2()) # ON SUCCESS
            filename_list.append(row_item)
    # print(filename_list)

    # ================ END OF STEP 1 ================ #

    # ================ STEP 2: CHECK FILE EXISTENCE ================ #
    """ File exist THEN go STEP 3
        ELSE  SKIP"""
    # print("FILENAME_LIST: ", str(filename_list))
    if len(filename_list) != 0:
        for file_i in range(len(filename_list)):
            each_row = filename_list[file_i]
            daily_task.store_code = each_row['store_code']
            daily_task.date_code = str(each_row['date_code'])
            daily_task.hourly_code = str(each_row['hour_code'])
            daily_task.sequence = str(each_row['sequence'])

            daily_task.file_path = daily_task.zip_store_path
            daily_task.file_name = daily_task.create_filename_only_bz2() # Asembles the filename for compressed
            file_exist_status = daily_task.check_file_exist()
            # print(file_exist_status)
            # print(daily_task.file_name)
    # ================ END OF STEP 2 ================ #
            print(file_exist_status["message"])
            if file_exist_status["message"] == True: # IF Compressed file EXIST

    # ================ STEP 3: Check the checksum of the compressed file ================ #
                daily_task.url = daily_task.BASE_URL + "cal_MD5_checksum"
                daily_task.url_obj = {
                "filename_path": daily_task.zip_store_path,
                "filename": daily_task.file_name
                }
                checksum_compressed_local = daily_task.post_req()
                # print(checksum_compressed_local)
                local_checksum = checksum_compressed_local["data"]
                if local_checksum == each_row["compress_checksum"]:
                    
    # ================ END OF STEP 3 ================ #

                    # ================ STEP 4: UNCOMPRESS ================ #
                    daily_task.url = daily_task.BASE_URL + "decompress"
                    # daily_task.unzip_store_path = "/home/panda/test_SFTP/Test_dir/new"
                    # daily_task.file_path = "/home/panda/test_SFTP/Test_dir"
                    daily_task.url_obj = {
                    "filename": daily_task.file_name,
                    "source_path": daily_task.zip_store_path,
                    "path_store_zip": daily_task.unzip_store_path
                    }
                    uncompress_stat = daily_task.post_req()
                    print(uncompress_stat)
                    # ================ END OF STEP 4 ================ #

                    # ================ STEP 5: CHECKSUM for .sql file ================ #
                    daily_task.file_name = daily_task.create_filename_only_sql()
                    # sql_filename_list.append(daily_task.file_name)
                    # daily_task.unzip_store_path = "/home/panda/test_SFTP/Test_dir/new"
                    daily_task.url = daily_task.BASE_URL + "cal_MD5_checksum"
                    daily_task.url_obj = {
                    "filename_path": daily_task.unzip_store_path,
                    "filename": daily_task.file_name
                    }
                    umcompressed_sql_res = daily_task.post_req()
                    print(umcompressed_sql_res)
                    # ================ END OF STEP 5 ================ #

                    # ================ STEP 6: Update STATUS to 2 UNZIP COMPLETED ================ #
                    daily_task.url = daily_task.BASE_URL + "task_status_update_v2"
                    daily_task.url_obj = {
                    "database_name": daily_task.database_name,
                    "table_name": daily_task.tablename,
                    "task_status": 2,
                    "store_code": each_row['store_code'],
                    "date_code": each_row['date_code'],
                    "hour_code": each_row['hour_code'],
                    "sequence": int(each_row['sequence'])
                    }
                    task_update_status = daily_task.post_req()
                    print(task_update_status)
                    
                    # ================ END OF STEP 6 ================ #
                    if umcompressed_sql_res["data"] == each_row["uncompress_checksum"]:
                        # ================ STEP 7: RESTORE SCRIPT ================ #
                        # daily_task.unzip_store_path = "/home/panda/test_SFTP/Test_dir/new"
                        daily_task.file_name = daily_task.create_filename_only_sql()
                        daily_task.url = daily_task.BASE_URL + "restore_sql"
                        daily_task.url_obj = {
                        "file_source_path": daily_task.unzip_store_path,
                        "filename": daily_task.file_name
                        }
                        print(daily_task.url_obj)
                        restore_status = daily_task.post_req()
                        print(restore_status)
                        # ================ END OF STEP 7 ================ #

                        if restore_status["status"] == "success":
                            
                            # HOUSEKEEPING: REMOVE UNWATED .SQL FILES    
                            print(delete_file_abs(daily_task.unzip_store_path, daily_task.file_name))

                            # ================ STEP 8: Update STATUS to 3 RESTORE COMPLETED ================ #
                            daily_task.url = daily_task.BASE_URL + "task_status_update_v2"
                            daily_task.url_obj = {
                            "database_name": daily_task.database_name,
                            "table_name": daily_task.tablename,
                            "task_status": 3,
                            "store_code": each_row['store_code'],
                            "date_code": each_row['date_code'],
                            "hour_code": each_row['hour_code'],
                            "sequence": int(each_row['sequence'])
                            }
                            task_update_status = daily_task.post_req()
                            print(task_update_status)
                            # ================ END OF STEP 8 ================ #

    # HOUSEKEEPING: REMOVE UNWATED .SQL FILES     
    #for f in range(len(sql_filename_list)):
    #    sql_file_name = sql_filename_list[f]
    #    print(delete_file_abs(daily_task.unzip_store_path, sql_file_name))

                

        


             







