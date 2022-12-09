"""
# Function to validate Min transaction Date
Version No: 1
Release Date: 12 September 2021 
KKSC
""" 

from date_functions.Query_Date import current_date_only, trans_previous_check

def min_transaction_validation(trans_date_input, no_years_back, company_guid):
    min_trans_date = trans_date_input
    backend_pos_trans_message = ""
    backend_pos_trans_stat = "OK"
    frontend_pos_trans_message = ""
    frontend_pos_trans_stat = "OK"
    # message_extreme_case = "" # Used when no table/database
    for trans_i in range(len(min_trans_date)):
        each_table_items = min_trans_date[trans_i]
        # message_extreme_case = message_extreme_case + str(each_table_items) + "<br>"
        try:
            min_transPO_date = each_table_items["MinPOdate"]
            trans_tablename = each_table_items["tablename"]
            # print(min_transPO_date)
            # GOT ISSUES 
            compared_date = trans_previous_check(current_date_only(), no_years_back)
            # print(compared_date)
            # print(min_transPO_date)

            # ===== DISABLE BWY COMPANY ===== #
            if company_guid == "380BC4E3EF2F11E9934ADED0BD1483FD" and \
                trans_tablename == "backend":
                min_transPO_date = "2021-09-17"
                backend_pos_trans_message = str(trans_tablename).upper() + " DISABLED " + "[ OK ] "
                backend_pos_trans_stat = "OK"
             # ===== DISABLE BWY COMPANY ===== #
            
            if min_transPO_date == "None" and \
                trans_tablename == "frontend":
                frontend_pos_trans_message = str(trans_tablename).upper() + " No Records, might be E-Store" + "<br>" \
                    "1st transdate: " + min_transPO_date + " [ ALERT!! N0000-00-00 or None Date Detected] "
                frontend_pos_trans_stat = "OK"
            
            elif min_transPO_date < compared_date and \
                trans_tablename == "frontend":
                frontend_pos_trans_message = str(trans_tablename).upper() + " data " \
                    "1st transdate: " + min_transPO_date + " [ ALERT!! Data more than " + str(no_years_back) + " years ] "
                frontend_pos_trans_stat = "NO"

            elif min_transPO_date > compared_date and \
                trans_tablename == "frontend":
                frontend_pos_trans_message = str(trans_tablename).upper() + " data store less than " + str(no_years_back) + " years, " \
                    "1st transdate: " + min_transPO_date + " [ OK ] "
                frontend_pos_trans_stat = "OK"

            if min_transPO_date == "None" and \
                trans_tablename == "backend":
                frontend_pos_trans_message = str(trans_tablename).upper() + ".pomain Min Transaction PODate issue, " \
                    "1st transdate: " + min_transPO_date + " [ ALERT!! N0000-00-00 or None Date Detected] "
                frontend_pos_trans_stat = "NO"

            elif min_transPO_date < compared_date and \
                trans_tablename == "backend":
                backend_pos_trans_message = str(trans_tablename).upper() + " data " + \
                    "1st transdate: " + min_transPO_date + " [ ALERT!! Data more than " + str(no_years_back) + "  years ] "
                backend_pos_trans_stat = "NO"
                        
            elif min_transPO_date > compared_date and \
                trans_tablename == "backend":
                backend_pos_trans_message = str(trans_tablename).upper() + " data store less than " + str(no_years_back) + "  years, " + \
                    " 1st transdate: " + min_transPO_date + " [ OK ] "
                backend_pos_trans_stat = "OK"
            
        except:
            frontend_pos_trans_stat = "NO"
            backend_pos_trans_stat = "NO"
            backend_pos_trans_message = backend_pos_trans_message + "<br>" + str(each_table_items)
            frontend_pos_trans_message = frontend_pos_trans_message + "<br>" + str(each_table_items)
            return {
                "frontend_pos_trans_stat": frontend_pos_trans_stat,
                "backend_pos_trans_stat": backend_pos_trans_stat,
                "backend_pos_trans_message": backend_pos_trans_message,
                "frontend_pos_trans_message": frontend_pos_trans_message
            }
    
    return {
                "frontend_pos_trans_stat": frontend_pos_trans_stat,
                "backend_pos_trans_stat": backend_pos_trans_stat,
                "backend_pos_trans_message": backend_pos_trans_message,
                "frontend_pos_trans_message": frontend_pos_trans_message
            }