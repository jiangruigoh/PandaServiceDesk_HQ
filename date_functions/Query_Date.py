"""
Version No: 1
Release Date: 14 September 2021 
KKSC
"""

from datetime import datetime
import datetime as date_delta
# from dateutil.relativedelta import relativedelta
import decimal

def current_time():
    now = datetime.now() #Get Datetime input
    current_time = now.strftime("%H:%M:%S")
    current_date = datetime.today().strftime('%Y-%m-%d')
    created_at_input = current_date + " " + current_time # Format: YYYY-MM-DD HH:MM:SS
    return created_at_input

def current_date_only():
    now = datetime.now() #Get Datetime input
    current_date = datetime.today().strftime('%Y-%m-%d')
    return current_date

def converter_to_obj(date_str):
    current_obj = datetime.strptime(date_str, '%Y-%m-%d')
    res = datetime.date(current_obj)
    return res

def current_date_code():
    current_datecode = datetime.today().strftime('%Y%m%d')
    return current_datecode

def current_hourly_code():
    current_hourlycode = datetime.today().strftime('%H')
    return current_hourlycode

def current_time_only():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def previous_date_only():
    previous_Date = datetime.today() - date_delta.timedelta(days=1)
    previous_Date_Formatted = previous_Date.strftime ('%Y-%m-%d') # format the date to yyyy-mm-dd
    return previous_Date_Formatted

def first_previous_date():
    last_day_of_prev_month = datetime.today().replace(day=1) - date_delta.timedelta(days=1)
    start_day_of_prev_month = datetime.today().replace(day=1) - date_delta.timedelta(days=last_day_of_prev_month.day)
    date_only_opt = start_day_of_prev_month.strftime ('%Y-%m-%d')
    return date_only_opt

def day_before_prev_date():
    actual_date =  datetime.strptime(first_previous_date() , '%Y-%m-%d')
    result = actual_date.date()- date_delta.timedelta(days=1)
    return result

def last_previous_date():
    last_day_of_prev_month = datetime.today().replace(day=1) - date_delta.timedelta(days=1)
    date_only_opt = last_day_of_prev_month.strftime ('%Y-%m-%d')
    return date_only_opt

def current_date_first():
    current_date = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    return current_date

def after_current_date_first():
    actual_date =  datetime.strptime(current_date_first() , '%Y-%m-%d')
    result = actual_date.date() + date_delta.timedelta(days=1)
    result_formated = result.strftime ('%Y-%m-%d')
    return result_formated

def last_day_of_month():
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = datetime.today().replace(day=28) + date_delta.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    result = next_month - date_delta.timedelta(days=next_month.day)
    return result.strftime ('%Y-%m-%d')

def trans_previous_check(in_date, no_years_back):
    month_option = "1"
    day_option = "1"
    in_date_format = datetime.strptime(in_date, "%Y-%m-%d")
    in_date_year_altered = str(in_date_format.year - no_years_back)
    date_to_use = in_date_year_altered + "-" + month_option + "-" + day_option
    # formated_date_final = date_to_use.strftime ('%Y-%m-%d')
    return date_to_use

def backend_period_date_check(in_date, period_remark_split, period_location_group):
    """
    RETURNS TRUE then do not create Ticket
    RETURN FALSE then Create Ticket
    """
    in_date_format = datetime.strptime(in_date, "%Y-%m-%d")
    in_date_day = str(in_date_format.day)
    in_date_year = str(in_date_format.year)
    curr_status = None
    prev_status = None
    current_date = datetime.strptime(current_date_only(), "%Y-%m-%d")
    previous_date_month = str(current_date.month - 1)
    previous_date = in_date_year + "-" + previous_date_month + "-" + in_date_day
    previous_date_formated = datetime.strptime(previous_date, "%Y-%m-%d")
    
    # print(type(in_date_format))
    # print(type(current_date))
    if in_date_format.month == current_date.month: # CHECK CURRENT MONTH
        if period_remark_split != "7E":
            curr_status = False
        if period_remark_split == "7E":
            curr_status = True
    elif in_date_format.month == previous_date_formated.month:
        if period_remark_split != "3":
            prev_status = False
        if period_remark_split == "3":
            prev_status = True

    # print(in_date_format.month,previous_date_formated.month)
    # print(curr_status, prev_status)
    if curr_status == False:
        return {"message": "Current date " + str(in_date_format) +" Daily Recal Process: Not Completed [ ALERT!! stock recal not complete ] " + " location Group: " + str(period_location_group),
                "status": "NO"}
    if prev_status == False:
        return {"message": "Previous date " + str(previous_date_formated) + " Daily Recal Process: Not Completed[ ALERT!! stock recal not complete ]" + " location Group: " + str(period_location_group),
                "status": "NO"}

    if curr_status == True:
        return {"message": "Current date " + str(in_date_format) +" Daily Recal Process: Completed [ OK ]" + " location Group: " + str(period_location_group),
                "status": "OK"}
    if prev_status == True:
        return {"message": "Previous date " + str(previous_date_formated) +" Daily Recal Process: Completed [ OK ]" + " location Group: " + str(period_location_group),
                "status": "OK"}
    
    return {"message": "",
            "status": "OK"}

