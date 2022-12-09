"""
Version No: 1
Release Date: 17 September 2021 
KKSC
"""

import json
from date_functions.Query_Date import current_time, backend_period_date_check
from panda_service_desk.helpdesk_requests import helpdesk_new_ticket, organisation_info, get_userguid
from panda_service_desk.hardware_validator import cpu_checkpoint, ram_checkpoint, partition_checkpoint
from panda_service_desk.backup_validator import backup_checkpoint
from panda_service_desk.Transac_min_validator import min_transaction_validation


def validator_main(data, company_guid, outlet_name, outlet_code, threshold_json):
    # Parameters to be Changed    
    try:
        threshold_alert = threshold_json["threshold_alert"]
        #SET_PERCENTAGE_CPU = threshold_alert["CPU"]
        #SET_PERCENTAGE_RAM = threshold_alert["RAM"]
        #SET_PERCENTAGE_PARTITION = threshold_alert["PARTITION"]
        #FILESIZE_SET_VALUE = threshold_alert["FILESIZE"]
        #SET_MIN_TRANSAC_YEARS_BACK = threshold_alert["MIN_TRANSAC"]
    except:
        SET_PERCENTAGE_CPU = 90 # Redundant IN CASE OF FAILURE ONLY
        SET_PERCENTAGE_RAM = 90 # Redundant IN CASE OF FAILURE ONLY
        SET_PERCENTAGE_PARTITION = 90 # Redundant IN CASE OF FAILURE ONLY
        FILESIZE_SET_VALUE = 0.8 # Redundant IN CASE OF FAILURE ONLY
        SET_MIN_TRANSAC_YEARS_BACK = 10 # Redundant IN CASE OF FAILURE ONLY

    try:
        SET_PERCENTAGE_CPU = threshold_alert["CPU"]
    except:
        SET_PERCENTAGE_CPU = 90 # Redundant IN CASE OF FAILURE ONLY

    try:
        SET_PERCENTAGE_RAM = threshold_alert["RAM"]
    except:
        SET_PERCENTAGE_RAM = 90 # Redundant IN CASE OF FAILURE ONLY

    try:
        SET_PERCENTAGE_PARTITION = threshold_alert["PARTITION"]
    except:
        SET_PERCENTAGE_PARTITION = 90 # Redundant IN CASE OF FAILURE ONLY

    try:
        FILESIZE_SET_VALUE = threshold_alert["MIN_BACKUP_SIZE_KB"]
    except:
        FILESIZE_SET_VALUE = 0.8 # Redundant IN CASE OF FAILURE ONLY

    try:
        SET_MIN_TRANSAC_YEARS_BACK = threshold_alert["MIN_HISTORICAL_DATA_YEARS"]
    except:
        SET_MIN_TRANSAC_YEARS_BACK = 10 # Redundant IN CASE OF FAILURE ONLY

    ticket_status = False

    # print(FILESIZE_SET_VALUE)
    # print(json.dumps(data, indent = 4, sort_keys=True))
    hardware_info = data["hardware"]
    os_fullname = hardware_info["os"]
    my_sql_data = data["mysql"]
    database_info = my_sql_data["db_info"]

    if isinstance(database_info, list):
        database_info = ""

    # ====== Validate Min Transaction Date =====#
    # print(database_info)
    min_trans_date = my_sql_data["min_trans_date"]

    # ===== DISABLE BWY COMPANY ===== #
    """
    if company_guid == "380BC4E3EF2F11E9934ADED0BD1483FD":
        min_trans_date = [
                            {
                                "datatype": "pomain",
                                "MinPOdate": "2021-09-17",
                                "tablename": "backend"
                            }
                            ]
    """
    # ===== DISABLE BWY COMPANY ===== #

    min_transac_out = min_transaction_validation(min_trans_date, SET_MIN_TRANSAC_YEARS_BACK, company_guid)
    frontend_pos_trans_stat = min_transac_out["frontend_pos_trans_stat"]
    # print(frontend_pos_trans_stat)
    backend_pos_trans_stat = min_transac_out["backend_pos_trans_stat"]
    # print(backend_pos_trans_stat)
    backend_pos_trans_message = min_transac_out["backend_pos_trans_message"]
    # print(backend_pos_trans_message)
    frontend_pos_trans_message = min_transac_out["frontend_pos_trans_message"]
    # print(frontend_pos_trans_message)

    # === Validate daily process === #
    daily_process_json = my_sql_data["daily_process"]
    # print(daily_process_json)
    daily_backend_period = daily_process_json["backend.period"]
    if "doesn't exist" not in daily_backend_period and len(daily_backend_period) != 0 and "Error" not in daily_backend_period:
        daily_proc_period_msg = ""
        doclog_message_daily_proc = ""
        daily_progress_status = ""
        for period_i in range(len(daily_backend_period)):
            period_row = daily_backend_period[period_i]
            period_remark = period_row["Remark"]
            period_location_group = period_row["location_group"]
            period_remark_split = period_remark.split()[0]
            period_date = period_row["DateStart"]
            daily_process_status = backend_period_date_check(period_date, period_remark_split, period_location_group)
            # print(period_date,period_remark_split)
            # print(daily_process_status)
            daily_proc_msg = daily_process_status["message"]
            doclog_message_daily_proc = doclog_message_daily_proc + daily_proc_msg + "<br>"

            if "not" in daily_proc_msg:
                daily_proc_period_msg = daily_proc_period_msg + daily_proc_msg + "<br>"

        if daily_proc_period_msg == "":
            daily_progress_status = "OK"
    else:
        daily_progress_status = "NO"
        doclog_message_daily_proc = "backend.Period no records: " + str(daily_backend_period) 
        daily_proc_period_msg =  "backend.Period no records: " + str(daily_backend_period) 


    # os_formated_name = os_fullname.split() # Ensures that its only name
    # os_name = os_formated_name[0] # Ensures that its only name
    # print(os_name)

    # Ram Information
    ram_info = hardware_info["ram"]
    ram_used_total_msg = "RAM [Used/Total]: " + str(ram_info["used"]) + "/" +  str(ram_info["total"])
    # print(ram_used_total_msg)

    cpu_res = ''
    ram_res = ''
    # company_guid_msg = ''
    
    # CPU
    cpu_status = cpu_checkpoint(hardware_info["cpu"], SET_PERCENTAGE_CPU)
    cpu_res = cpu_status["response"]

    # RAM 
    ram_status = ram_checkpoint(hardware_info["ram"], SET_PERCENTAGE_RAM)
    ram_res = ram_status["response"]

    # Partition 
    partition_status = partition_checkpoint(hardware_info["hardisk"], SET_PERCENTAGE_PARTITION)
    partition_res = ""
    partition_message = ""
    for ptr_i in range(len(partition_status)):
        each_ptr = partition_status[ptr_i]
        if "OK" not in each_ptr["response"]:
            partition_message = partition_message + "\n" + each_ptr["response"] + "<br>"
            partiton_res = "Have issues"
        else:
            partition_message = partition_message + "\n" + each_ptr["response"] + "<br>"
    
    # Partiton Return Message to "OK" IF no issues
    if partition_res == "":
        partition_res = "OK"

    # Backup 
    backup_status = backup_checkpoint(data["backup"], FILESIZE_SET_VALUE)
    # print(backup_status)
    backup_msg_1 = backup_status["status"]
    backup_msg_2 = backup_status["end_month"]
    end_month_backup_msg = backup_status["end_month_message"]
    dailybackup_msg = backup_status["daily_backup_message"]
    validated_issue = ""

    # HelpDesk Message Section Below
    if "Linux" in  os_fullname: 
        if "OK" in ram_res and \
            "OK" in cpu_res and \
            partition_res == "OK" and \
            backup_msg_1 == "OK" and \
            backup_msg_2 == "OK" and \
            backend_pos_trans_stat == "OK" and \
            frontend_pos_trans_stat == "OK" and \
            daily_progress_status == "OK":            
            # Do not ceate Ticket if no issues
            # print("NO ISSUES")
            validated_issue = 0
            final_validator_opt = {"status":
                {"cpu": cpu_status,
                 "ram": ram_status,
                 "partition": partition_status,
                 "backup": backup_status,
                 "created_at": current_time(),
                 "validated_issue": validated_issue,
                 "backend_pos_trans": backend_pos_trans_message,
                 "frontend_pos_trans": frontend_pos_trans_message,
                 "daily_process": doclog_message_daily_proc
                }
           }
            return final_validator_opt
        else:
            linux_message = "Outlet Name: " + outlet_name + "<br>" \
                + "CPU :" + cpu_res + "<br>" \
                + "RAM: " + ram_res + "<br>" \
                + ram_used_total_msg + "<br>" \
                + partition_message + "<br>" \
                + dailybackup_msg + "<br>" + end_month_backup_msg + "<br>" \
                +  backend_pos_trans_message + "<br>" \
                + frontend_pos_trans_message + "<br>" \
                + doclog_message_daily_proc + "<br>" \
                + str(database_info)
            # print(linux_message)

            # Query Which Company based on company_guid
            company_info = organisation_info(company_guid) 
            
            # Query which user_guid to use
            user_info = get_userguid(company_info)
            # print("User_guid: ", user_info["user_guid"])
            # print(user_info)

            # Create Helpdesk Ticket
            helpdesk_response = helpdesk_new_ticket(linux_message, user_info["user_guid"], outlet_code)
            if helpdesk_response == 200:
               ticket_status = True
              #print("Ticket Status: " + str(ticket_status))
            
            validated_issue = 1

            final_validator_opt = {"status":
                {"cpu": cpu_status,
                 "ram": ram_status,
                 "partition": partition_status,
                 "backup": backup_status,
                 "created_at": current_time(),
                 "validated_issue": validated_issue,
                 "backend_pos_trans": backend_pos_trans_message,
                 "frontend_pos_trans": frontend_pos_trans_message,
                 "daily_process": doclog_message_daily_proc
                }
           }

    if "Windows" in os_fullname:
        if "OK" in ram_res and \
            "OK" in cpu_res and \
            partition_res == "OK" and \
            backup_msg_1 == "OK" and \
            backend_pos_trans_stat == "OK" and \
            frontend_pos_trans_stat == "OK" and \
            daily_progress_status == "OK":             
            # Do not ceate Ticket if no issues
            # print("NO ISSUES")
            validated_issue = 0
            final_validator_opt = {"status":
                {"cpu": cpu_status,
                 "ram": ram_status,
                 "partition": partition_status,
                 "backup": backup_status,
                 "created_at": current_time(),
                 "validated_issue": validated_issue,
                 "backend_pos_trans": backend_pos_trans_message,
                 "frontend_pos_trans": frontend_pos_trans_message,
                 "daily_process": doclog_message_daily_proc
                }
           }
            return final_validator_opt
        else:
            windows_message = "Outlet Name: " + outlet_name + "<br>" \
                + "CPU :" + cpu_res + "<br>" \
                + "RAM: " + ram_res + "<br>" \
                + ram_used_total_msg + "<br>" \
                + partition_message + "<br>" \
                + "Backup Info: " + backup_msg_1 + "<br>" \
                + backend_pos_trans_message + "<br>" \
                + frontend_pos_trans_message + "<br>" \
                + doclog_message_daily_proc + "<br>" \
                + str(database_info)
            # print(windows_message)

            # Query Which Company based on company_guid
            company_info = organisation_info(company_guid) 
            
            # Query which user_guid to use
            user_info = get_userguid(company_info)
            # print("User_guid: ", user_info["user_guid"])
            # print(user_info)

            # Create Helpdesk Ticket
            helpdesk_response = helpdesk_new_ticket(windows_message, user_info["user_guid"], outlet_code)
            if helpdesk_response == 200:
                ticket_status = True
            
            validated_issue = 1

            final_validator_opt = {"status":
                {"cpu": cpu_status,
                 "ram": ram_status,
                 "partition": partition_status,
                 "backup": backup_status,
                 "created_at": current_time(),
                 "validated_issue": validated_issue,
                 "backend_pos_trans_msg": backend_pos_trans_message,
                 "frontend_pos_trans_msg": frontend_pos_trans_message,
                 "daily_process": doclog_message_daily_proc
                }
           }
      
    return final_validator_opt


