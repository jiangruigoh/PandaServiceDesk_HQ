"""
# Function to validate Backup
Version No: 1
Release Date: 21 September 2021 
KKSC
""" 
from date_functions.Query_Date import current_date_only, previous_date_only, \
    first_previous_date, last_previous_date, current_date_first, last_day_of_month, \
    day_before_prev_date, after_current_date_first

from panda_service_desk.filesize_validator import size_checker

def backup_checkpoint(backup_info, FILESIZE_SET_VALUE):
    # print(FILESIZE_SET_VALUE)
    backup_not_update = []
    status_counter = "Backup did not run"
    current_file_list = []
    previous_file_list = []
    # print(operating_sys)
    end_month_previous_list = []
    end_month_current_list = []
    backup_result = "None"
    daily_conditional_list_curr = []
    daily_conditional_list_prev = []
    size_message = " "
    size_message2 = " "
    daily_backup_message = ""
    end_month_message = ""
    

    for path_i in range(len(backup_info)):
        # print(backup_info[path_i])
        each_dirs_items = backup_info[path_i]
        file_list = each_dirs_items["files"]
        backup_names = each_dirs_items["name"]
        # status_counter = "No" 

        if file_list == False:
            # Invalid Path used
            return {"status": "Invalid Backup Path",
                    "end_month": "N/A",
                    "end_month_message": "",
                    "daily_backup_message": "",
                    }
            
        for file_i in range(len(file_list)):
            files_information = file_list[file_i]
            # print(files_information["date"], current_time())

            # Format datetime to date for each file
            files_date_opt = files_information["date"].split()
            files_date_only = files_date_opt[0]
            # print(files_date_only)
            

            if backup_names == "end_month" and \
                first_previous_date() <= files_date_only <= last_previous_date():
                end_month_previous_list.append(files_information)
                # Check Monthly Backup
                # backup_result = "OK"
            
            if backup_names == "end_month" and \
                current_date_first() <= files_date_only <= last_day_of_month():
                end_month_current_list.append(files_information)
                
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
            
            """
            if files_date_only in (str(last_previous_date()),str(current_date_first())) and \
                    backup_names == "end_month":
                daily_conditional_list_curr.append(files_information)

            if files_date_only in (str(day_before_prev_date()), str(first_previous_date())) and \
                    backup_names == "end_month":
                daily_conditional_list_prev.append(files_information)
            """ 
    #print("daily_consitional_curr: " + str(len(daily_conditional_list_curr)))
    #print("daily_consitional_prev: " + str(len(daily_conditional_list_prev)))
    # print("current: " + str(len(current_file_list)))
    # print("previous: " + str(len(previous_file_list)))
    # print("end_month_current_list: "+ str(len(end_month_current_list)))
    # print("end_month_previous_list: " + str(len(end_month_previous_list)))

    #===== Daily backup Process Checking Below ====#
    # 1st of each month Check 
    if current_date_only() == current_date_first() and (len(current_file_list) == 0) and \
        (len(end_month_current_list) >= len(end_month_previous_list)) and \
        (len(end_month_current_list) !=0): # and len(end_month_previous_list)) !=0:
            status_counter = "OK"
            daily_backup_message = " Daily MySQL Backup: " \
                                   + " [ OK ] "
    
    # 2nd day of each month Check
    elif current_date_only() == after_current_date_first() and (len(previous_file_list) == 0) and \
        (len(end_month_current_list) >= len(end_month_previous_list)) and \
        (len(current_file_list) != 0) and \
        (len(end_month_current_list) !=0): #and len(end_month_previous_list)) !=0:
            current_size_info = size_checker(current_file_list, FILESIZE_SET_VALUE)
            file_size_list = current_size_info["filelist"]
            # print(previous_size_info)
            if current_size_info["status"] == False:
                status_counter = "FileSize Issue"
                for size_i in range(len(file_size_list)):
                    each_size_item = file_size_list[size_i]
                    each_size_filename = each_size_item["filename"]
                    size_message = size_message + str(each_size_filename) + " [ ALERT!! filesize value below " + str(FILESIZE_SET_VALUE) +   "KB ] " +  ", " +  "<br>"

                daily_backup_message = " Daily MySQL Backup Size Issue: " \
                                   + size_message \
                                   + "<br>" \
                                   + " Daily MySQL Backup TODAY QTY: " \
                                   + str(len(current_file_list)) \
                                   + " [ OK ] "
            else:
                status_counter = "OK"
                daily_backup_message = " Daily MySQL Backup TODAY QTY: " \
                                   + str(len(current_file_list)) \
                                   + " [ OK ] "

    # NO ISSUES PREVIOUS AND CURRENT THE SAME VALUES or MORE   
    elif (len(current_file_list) >= len(previous_file_list)) and \
        (len(current_file_list) != 0): #and len(previous_file_list) != 0):
        current_size_info = size_checker(current_file_list, FILESIZE_SET_VALUE)
        previous_size_info = size_checker(previous_file_list, FILESIZE_SET_VALUE)
        file_size_list = current_size_info["filelist"]
        file_size_list_prev = previous_size_info["filelist"]
        # print(previous_size_info)
        if current_size_info["status"] == False:
            status_counter = "FileSize Issue"
            for size_i in range(len(file_size_list)):
                each_size_item = file_size_list[size_i]
                each_size_filename = each_size_item["filename"]
                size_message = size_message + str(each_size_filename) + ", " + " [ ALERT!! filesize value below " + str(FILESIZE_SET_VALUE) +   "KB ] " +  "<br>"
        if previous_size_info["status"] == False:
            status_counter = "FileSize Issue"
            for size_j in range(len(file_size_list_prev)):
                each_size_item_prev = file_size_list_prev[size_j]
                each_size_filename_prev = each_size_item_prev["filename"]
                size_message2 = size_message2 + str(each_size_filename_prev) + ", " + " [ ALERT!! filesize value below " + str(FILESIZE_SET_VALUE) +   "KB ] " +  "<br>"

        daily_backup_message = " Daily MySQL Backup Size Issue: " \
                            + size_message \
                            + size_message2 \
                            +  "<br>" \
                            + " Daily MySQL Backup TODAY QTY VS YESTERDAY QTY: " \
                            + str(len(current_file_list)) \
                            + " VS " \
                            + str(len(previous_file_list)) \
                            + " [ OK ] "

        if current_size_info["status"] == True and previous_size_info["status"] == True:
            status_counter = "OK"
            daily_backup_message = " Daily MySQL Backup TODAY QTY VS YESTERDAY QTY: " \
                                        + str(len(current_file_list)) \
                                        + " VS " \
                                        + str(len(previous_file_list)) \
                                        + " [ OK ] "

    elif len(current_file_list) == 0 and len(previous_file_list) == 0:
        status_counter = "No Previous or Current Backup"
        daily_backup_message = " Daily MySQL Backup TODAY QTY VS YESTERDAY QTY: " \
                                    + str(len(current_file_list)) \
                                    + " VS " \
                                    + str(len(previous_file_list)) \
                                    + " [ ALERT!! No Previous or Current Backup ] "

    elif len(current_file_list) < len(previous_file_list):
        # BASE CASE/VALIDATOR
        status_counter = "Number of previous and current backup files not the same"
        daily_backup_message = " Daily MySQL Backup TODAY QTY VS YESTERDAY QTY: " \
                                    + str(len(current_file_list)) \
                                    + " VS " \
                                    + str(len(previous_file_list)) \
                                    + " [ ALERT!! Backup less than yesterday ] "
    else:
        status_counter = "Backup did not run"
        daily_backup_message = " Daily MySQL Backup TODAY QTY VS YESTERDAY QTY: " \
                                    + str(len(current_file_list)) \
                                    + " VS " \
                                    + str(len(previous_file_list)) \
                                    + " [ ALERT!! Backup Issue ] "
    
    #===== Backup END MONTH Process Checking Below ====#
    # print(end_month_current_list)
    # print(end_month_previous_list)
    if len(end_month_current_list) == 0: #and len(end_month_previous_list) == 0:
        backup_result = "End Month Backup THIS MONTH QTY VS LAST MONTH QTY: " \
                            + str(len(end_month_current_list)) \
                            + " VS " \
                            + str(len(end_month_previous_list)) \
                            + " [ ALERT!! End month backup not completed ] "
        end_month_message = backup_result

    elif len(end_month_current_list) >= len(end_month_previous_list) and \
        len(end_month_current_list) != 0:
        backup_result = "OK"
        end_month_message = "End Month MySQL Last Backup: " + str(current_date_first()) + " [ OK ]"

    elif len(end_month_current_list) < len(end_month_previous_list):
        backup_result = "End Month Backup THIS MONTH QTY VS LAST MONTH QTY: " \
                            + str(len(end_month_current_list)) \
                            + " VS " \
                            + str(len(end_month_previous_list)) \
                            + " [ ALERT!! End month backup not completed ] "
        end_month_message = backup_result
    
    backup_output= {"status": status_counter,
            "end_month": backup_result,
            "end_month_message": end_month_message,
            "daily_backup_message": daily_backup_message,
            # "old": backup_not_update,
            }
    # print(backup_output)
    return backup_output