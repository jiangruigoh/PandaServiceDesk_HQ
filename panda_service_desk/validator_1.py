"""
Version No: 1
Release Date: 17 June 2021 
KKSC
"""

import json
from date_functions.Query_Date import current_time, current_date_only, previous_date_only, first_previous_date, last_previous_date
from panda_service_desk.helpdesk_requests import helpdesk_new_ticket, organisation_info, get_userguid


def cpu_checkpoint(cpu_info, SET_PERCENTAGE):
    if cpu_info["used_percentage"] >= SET_PERCENTAGE:
        # print(cpu_info["used_percentage"])
        # print("High CPU Usage", str(cpu_info["used_percentage"]))
        return {"response": "Cpu Usage exceeds " + str(cpu_info["used_percentage"]) + " %" }
    else:
        return {"response": "OK"}

def ram_checkpoint(ram_info, SET_PERCENTAGE):
    if ram_info["used_percentage"] >= SET_PERCENTAGE:
        # print("High RAM usage", str(ram_info["used_percentage"]))
        return {"response": "RAM Usage exceeds " + str(ram_info["used_percentage"]) + " %" }
    else:
        return {"response": "OK"}

def partition_checkpoint(hardisk_info, SET_PERCENTAGE):
    hardisk_status = []
    for partition_i in range(len(hardisk_info)):
        each_partition = hardisk_info[partition_i]
        if ("loop" not in each_partition["device"]) and each_partition["used_percentage"]>=SET_PERCENTAGE:
            # print(each_partition["device"], each_partition["used_percentage"])
            hardisk_status.append({"response": "Warning: " + \
                each_partition["device"] +  \
                    " total usage is at " + str(each_partition["used_percentage"]) + " %"})
        elif ("loop" not in each_partition["device"]) and each_partition["used_percentage"]<SET_PERCENTAGE:
            hardisk_status.append({"response": "Partition: "  + each_partition["device"] + " OK" })
    return hardisk_status


def backup_checkpoint(backup_info):
    backup_updated = []
    backup_not_update = []
    status_counter = "Backup did not run"
    current_file_list = []
    previous_file_list = []
    #counter_curr = 0
    #counter_prev = 0
    # print(operating_sys)
    backup_result = ""

    for path_i in range(len(backup_info)):
        # print(backup_info[path_i])
        each_dirs_items = backup_info[path_i]
        file_list = each_dirs_items["files"]
        backup_names = each_dirs_items["name"]
        status_counter = "Backup did not run"

        if file_list == False:
            # Invalid Path used
            return {"status": "Invalid Backup Path",
                    "end_month": "N/A"
                    }
            
        
        for file_i in range(len(file_list)):
            files_information = file_list[file_i]
            # print(files_information["date"], current_time())

            # Format datetime to date for each file
            files_date_opt = files_information["date"].split()
            files_date_only = files_date_opt[0]
            # print(files_date_only)

            if backup_names == "end_month" and \
                files_date_only in (first_previous_date(), last_previous_date()):
                # Check Monthly Backup 
                backup_result = "OK"
                
            if current_date_only() not in files_information["date"] and \
                backup_names != "end_month" and \
                    backup_names != "backup_logs":
                    # OLD Backup
                backup_not_update.append(files_information)
                # status_counter = "Backup did not run"

            # New Logic Section below
            if current_date_only() in files_information["date"] and \
                backup_names != "end_month" and \
                    backup_names != "backup_logs":
                current_file_list.append(files_information)
                # status_counter = "OK"
                status_json = {
                    "directory": backup_names,
                    "filename": files_information["filename"],
                    "message": "OK"
                }
                #counter_curr+=1
                #print(counter_curr)

            if previous_date_only() in files_information["date"] and \
                backup_names != "end_month" and \
                    backup_names != "backup_logs":
                previous_file_list.append(files_information)
                #counter_prev+=1
                #print(counter_prev)

    # print(len(current_file_list))
    # print(len(previous_file_list))
    if len(current_file_list) == 0 or len(previous_file_list) == 0:
        # No Last Modified data for current and previous
        status_counter = "No Previous or Current Backup"
        # print("No Previous or Current Backup")
        #return status_counter

    if len(current_file_list) != len(previous_file_list):
        # BASE CASE/VALIDATOR
        status_counter = "Number of previous and current backup no tally"
        # print("Number of previous and current backup no tally")
        return {"status": status_counter,
            "end_month": "N/A"
        }
        

    if (len(current_file_list) == len(previous_file_list) and \
        len(current_file_list) != 0 or len(previous_file_list) != 0):
        status_counter = "OK"
    
    backup_output= {"status": status_counter,
            "end_month": backup_result
            # "current": current_file_list,
            # "previous": previous_file_list,
            # "old": backup_not_update,
            }
    # print(backup_output)
    return backup_output


def validator_main(data, company_guid, outlet_name, outlet_code):
    # Parameters to be Changed
    SET_PERCENTAGE = 80
    ticket_status = False

    # print(json.dumps(data, indent = 4, sort_keys=True))
    hardware_info = data["hardware"]
    os_fullname = hardware_info["os"]

    # os_formated_name = os_fullname.split() # Ensures that its only name
    # os_name = os_formated_name[0] # Ensures that its only name
    # print(os_name)

    # Ram Information
    ram_info = hardware_info["ram"]
    ram_used_total_msg = "RAM (Used/Total): " + str(ram_info["used"]) + "/" +  str(ram_info["total"])
    # print(ram_used_total_msg)

    cpu_res = ''
    ram_res = ''
    # company_guid_msg = ''
    
    # CPU
    cpu_status = cpu_checkpoint(hardware_info["cpu"], SET_PERCENTAGE)
    cpu_res = cpu_status["response"]

    # RAM 
    ram_status = ram_checkpoint(hardware_info["ram"], SET_PERCENTAGE)
    ram_res = ram_status["response"]

    # Partition 
    partition_status = partition_checkpoint(hardware_info["hardisk"], SET_PERCENTAGE)
    partition_res = ""
    for ptr_i in range(len(partition_status)):
        each_ptr = partition_status[ptr_i]
        if "OK" not in each_ptr["response"]:
            partition_res = partition_res + "\n" + each_ptr["response"] + "<br>"
    
    # Partiton Return Message to "OK" IF no issues
    if partition_res == "":
        partition_res = "OK"

    # Backup 
    backup_status = backup_checkpoint(hardware_info["backup"])
    # print(backup_status)
    backup_msg_1 = backup_status["status"]
    backup_msg_2 = backup_status["end_month"]
    validated_issue = ""

    # HelpDesk Message Section Below
    if "Linux" in  os_fullname: 
        if "OK" in ram_res and \
            "OK" in cpu_res and \
            partition_res == "OK" and \
            backup_msg_1 == "OK" and \
            backup_msg_2 == "OK":            
            # Do not ceate Ticket if no issues
            # print("NO ISSUES")
            validated_issue = 0
            final_validator_opt = {"status":
                {"cpu": cpu_status,
                 "ram": ram_status,
                 "partition": partition_status,
                 "backup": backup_status,
                 "created_at": current_time(),
                 "validated_issue": validated_issue
                }
           }
            return final_validator_opt
        else:
            linux_message = "Outlet Name: " + outlet_name + "<br>" \
                + "CPU :" + cpu_res + "<br>" \
                + "RAM: " + ram_res + "<br>" \
                + ram_used_total_msg + "<br>" \
                + "Hardisk Partition Info: " + "<br>" + partition_res + "<br>" \
                + "Backup Info: " + backup_msg_1 + "<br>" + "Monthly backup Status: " +  backup_msg_2
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
            
            validated_issue = 1

            final_validator_opt = {"status":
                {"cpu": cpu_status,
                 "ram": ram_status,
                 "partition": partition_status,
                 "backup": backup_status,
                 "created_at": current_time(),
                 "validated_issue": validated_issue
                }
           }

    if "Windows" in os_fullname:
        if "OK" in ram_res and \
            "OK" in cpu_res and \
            partition_res == "OK" and \
            backup_msg_1 == "OK":            
            # Do not ceate Ticket if no issues
            # print("NO ISSUES")
            validated_issue = 0
            final_validator_opt = {"status":
                {"cpu": cpu_status,
                 "ram": ram_status,
                 "partition": partition_status,
                 "backup": backup_status,
                 "created_at": current_time(),
                 "validated_issue": validated_issue
                }
           }
            return final_validator_opt
        else:
            windows_message = "Outlet Name: " + outlet_name + "<br>" \
                + "CPU :" + cpu_res + "<br>" \
                + "RAM: " + ram_res + "<br>" \
                + ram_used_total_msg + "<br>" \
                + "Hardisk Partition Info: " + "<br>" + partition_res + "<br>" \
                + "Backup Info: " + backup_msg_1
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
                 "validated_issue": validated_issue
                }
           }
      
    return final_validator_opt


