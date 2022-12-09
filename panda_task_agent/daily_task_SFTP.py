# STEP 10: SFTP
"""
Version No: 1
Release Date: 23 September 2021 
KKSC
"""

# from daily_panda_task_agent import Daily_Panda_Task_Agent
from yaml_read_config import assign_config_values

def sftp_run():
    # Initialize all defaul Params
    daily_task = assign_config_values()

    # STEP 1: List Task Status == 1
    daily_task.url = daily_task.BASE_URL + "get_task_status"
    daily_task.tablename = "from_outlet"
    daily_task.url_obj = {
      "database_name": daily_task.database_name,
      "table_name": daily_task.tablename,
      "task_status_value": 1,
      "ascending": "true"
    }
    task_status_1 = daily_task.post_req()
    task_records = task_status_1['data']
    task_record_list = []
    filename_list = []
    sftp_status = []
    update_status_list = []
    table_name_lst = []
    database_name_lst = []
    task_upload_status_list = []

    for row in range(len(task_records)):
        row_item = task_records[row]
        daily_task.branch_code = row_item['store_code']
        daily_task.date_code = str(row_item['date_code'])
        daily_task.hourly_code = str(row_item['hour_code'])
        daily_task.sequence = str(row_item['sequence'])
        uncompressed_md5 = str(row_item['uncompress_checksum'])
        compressed_md5 = str(row_item['compress_checksum'])
        error_value = row_item['error']
        resolve_value = row_item['resolve']
        daily_task.target_database_name = row_item["database_name"]
        daily_task.target_table_name = row_item["table_name"]
        database_name_lst.append(daily_task.target_database_name)
        table_name_lst.append(daily_task.target_table_name)

        # print(daily_task.create_filename_only())
        filename_list.append(daily_task.create_filename_only_bz2())
        task_record_list.append(task_records[row])
    # print(filename_list)

    if len(filename_list) != 0:
        # STEP 2: SFTP Transfer
        daily_task.url = daily_task.BASE_URL + "upload_sftp"
        for file_i in range(len(filename_list)):
            daily_task.url_obj = {
                "hostname": daily_task.sftp_hostname,
                "username": daily_task.sftp_username,
                "password": daily_task.sftp_password,
                "remoteFilePath": daily_task.sftp_remote_path,
                "localFilePath": daily_task.zip_store_path,
                "filename": filename_list[file_i],
                "port": daily_task.sftp_port
                }
            #print(daily_task.url_obj)
            task_sftp_status = daily_task.post_req()
            print(task_sftp_status)
            sftp_status.append(task_sftp_status)

    for j in range(len(sftp_status)):
        row_status = sftp_status[j]
        row_item = task_record_list[j]
        # print(row_status["status"])
        if row_status["status"] == 200:
            daily_task.branch_code = row_item['store_code']
            daily_task.date_code = str(row_item['date_code'])
            daily_task.hourly_code = str(row_item['hour_code'])
            daily_task.sequence = str(row_item['sequence'])
            uncompressed_md5 = str(row_item['uncompress_checksum'])
            compressed_md5 = str(row_item['compress_checksum'])
            error_value = row_item['error']
            resolve_value = row_item['resolve']
            # print(daily_task.sequence)

            daily_task.url = daily_task.REMOTE_BASE_URL + "create_task_agent"
            daily_task.tablename = "from_outlet"
            daily_task.url_obj = {
                    "database_name": daily_task.database_name,
                    "tablename": daily_task.tablename,
                    "task_type": daily_task.task_type,
                    "store_code": daily_task.store_code,
                    "date_code": daily_task.date_code,
                    "hourly_code": daily_task.hourly_code,
                    "sequence": daily_task.sequence,
                    "task_status": 1,
                    "source_database_name": database_name_lst[j],
                    "source_table_name": table_name_lst[j],
                    "uncompress_checksum": uncompressed_md5,
                    "compress_checksum": compressed_md5,
                    "error": error_value,
                    "resolve": resolve_value
                    }
            
            task_upload_status = daily_task.post_req()
            task_upload_status_list.append(task_upload_status)
            print(task_upload_status)

    for k in range(len(task_upload_status_list)):
        row_upload_stat = task_upload_status_list[k]
        row_item = task_record_list[k]
        # print(row_upload_stat["status_code"])
        if row_upload_stat["status_code"] == "200":
            # STEP 3: UPDATE STATUS to 2  
            daily_task.url = daily_task.BASE_URL + "task_status_update_v2"
            daily_task.url_obj = {
            "database_name": daily_task.database_name,
            "table_name": daily_task.tablename,
            "task_status": 2,
            "store_code": row_item['store_code'],
            "date_code": row_item['date_code'],
            "hour_code": row_item['hour_code'],
            "sequence": int(row_item['sequence'])
            }
            task_update_status = daily_task.post_req()
            print(task_update_status)
            print(task_update_status["status_code"])
            update_status_list.append(task_update_status["status_code"])

    



