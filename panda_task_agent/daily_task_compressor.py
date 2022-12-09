# STEP 9: COMPRESS
"""
Version No: 1
Release Date: 2 October 2021 
KKSC
"""

# from daily_panda_task_agent import Daily_Panda_Task_Agent
from yaml_read_config import assign_config_values
from housekeeping.delete_files import delete_file_abs

def compress_run():
    # Initialize all defaul Params
    daily_task = assign_config_values()

    # STEP 1: List Task Status == 0 
    daily_task.url = daily_task.BASE_URL + "get_task_status"
    daily_task.tablename = "from_outlet"
    daily_task.url_obj = {
      "database_name": daily_task.database_name,
      "table_name": daily_task.tablename,
      "task_status_value": 0,
      "ascending": "true"
    }
    task_status_0 = daily_task.post_req()
    task_records = task_status_0['data']
    filename_list = []
    zipfilename_list = []
    md5_list = []
    zipfilename_status = []


    for row in range(len(task_records)):
        row_item = task_records[row]
        daily_task.branch_code = row_item['store_code']
        daily_task.date_code = str(row_item['date_code'])
        daily_task.hourly_code = str(row_item['hour_code'])
        daily_task.sequence = str(row_item['sequence'])
        # print(daily_task.create_filename_only())
        filename_list.append(daily_task.create_filename_only_sql())

    # print(len(filename_list))
    # print(filename_list)

    if len(filename_list) != 0:
        # STEP 2: COMPRESSION
        daily_task.url = daily_task.BASE_URL + "compress"
        error_ctr = 0
        for file_i in range(len(filename_list)):
            daily_task.url_data = {"compress_mode": "bz2"}
            daily_task.url_obj = {
                    "filename": filename_list[file_i],
                    "path_to_zip": daily_task.dump_path,
                    "path_store_zip": daily_task.zip_store_path
                    }
            # print(daily_task.url_obj)
            task_zip_status = daily_task.post_req()
            # print("ZIP STATUS: " + str(task_zip_status))
            # print(task_zip_status)
            daily_task.url_data = ""
            compressed_filename = task_zip_status["zip_filename"]
            zipfilename_list.append(compressed_filename)
            zipfilename_status.append(task_zip_status)
            # print(compressed_filename)


    for i in range(len(zipfilename_list)):
        # STEP 3: CALCULATES Checksum for compressed file .bz2/gzip
        daily_task.url = daily_task.BASE_URL + "cal_MD5_checksum"
        daily_task.url_obj = {
                            "filename_path": daily_task.zip_store_path,
                            "filename": zipfilename_list[i]
                            }
        md5_digest_sql_res = daily_task.post_req()
        print(md5_digest_sql_res)
        md5_data_sql = md5_digest_sql_res["data"]
        # md5_status_sql = md5_digest_sql_res["message"]
        md5_list.append(md5_data_sql)

    for j in range(len(task_records)):
        # STEP 4: Update record checksum
        row_i = task_records[j]
        daily_task.url = daily_task.BASE_URL + "update_compressed_MD5_checksum"
        daily_task.url_obj = {
                            "database_name": daily_task.database_name,
                            "table_name": daily_task.tablename,
                            "compressed_md5": md5_list[j],
                            "store_code": row_i['store_code'],
                            "date_code": row_i['date_code'],
                            "hour_code": row_i['hour_code'],
                            "sequence": int(row_i['sequence'])
                            }
        # print(daily_task.url_obj)
        update_md5_value = daily_task.post_req()
        print(update_md5_value)
        
        #if md5_status_sql == "fail":
        #    error_ctr = 1
    
    # HOUSEKEEPING: REMOVE UNWATED .SQL FILES     
    for f in range(len(filename_list)):
        file_name = filename_list[f]
        print(delete_file_abs(daily_task.dump_path, file_name))

    for k in range(len(zipfilename_status)):
        # print(task_zip_status["message"])
        status_row = zipfilename_status[k]
        if "200" in status_row["message"]:
            # STEP 5: UPDATE STATUS to 1
            row_item = task_records[k]
            daily_task.url = daily_task.BASE_URL + "task_status_update_v2"
            daily_task.url_obj = {
            "database_name": daily_task.database_name,
            "table_name": daily_task.tablename,
            "task_status": 1,
            "store_code": row_item['store_code'],
            "date_code": row_item['date_code'],
            "hour_code": row_item['hour_code'],
            "sequence": int(row_item['sequence'])
            }
            task_update_status = daily_task.post_req()
            print(task_update_status)
    
    


