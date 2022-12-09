# Create New Panda Helpdesk Ticket
"""
Data_param: RAM, CPU, dailybackup
Version No: 1
Release Date: 22 June 2021 
KKSC
"""

import requests
from date_functions.Query_Date import current_time

def helpdesk_new_ticket(message, user_guid, outlet_code):
    # NEED TO CHANGE USER_GUID TO DYNAMIC #
    """
    STEP 3: Create new ticket based on the user_guid queried
    """
    # PARAMETERS
    URL = """https://helpdesk.panda-eco.com/app/admin_ticket/new_ticket_create?token=9001653282FA11EB85D6DED0BD1483FD"""
    USERNAME = "PandaHelpdesk"
    PWD = "7b6496618ae4ce853a26a3219478ddd0"
    myobj = {
            'assigned_to': '',
            'user_guid': user_guid, #'5583163CC7E811E993063CA0676091C4',
            'status_guid': '1',
            'priority_guid': '3',
            'department_guid': '1',
            'topic_guid': '94E49461B1D211EABDE5DED0BD1483FD',
            'subtopic_guid': 'ED3FD0F5D24011EBAECA42010A940064',
            'assigned_to_type': 'u', # u dedicated to open ticket
            'duedate': '',
            'source': 'APP',
            'contact_name': '',
            'phone_no': '0000',
            'resolved_reason_guid': '',
            'root_cause_guid': '',
            'outlet_code': outlet_code,
            'sys_ver': '',
            'doc_no': '',
            'pos_counter': '',
            'incident_date': current_time(),
            'message': message,
            'internal_note': '',
            'alertuser': '',
            'staff_guid': 'F5A47BB8CA5911EBAECA42010A940064'
            }

    try:
        response = requests.post(
                URL, 
                # json = {"output": ""},
                # headers = {},
                auth = (USERNAME, PWD),
                data = myobj
            )
        if response.status_code == 200:
            return response.status_code

    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        return "Timeout Error"
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        return "Too Many Redirects"
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)

def organisation_info(company_guid):
    """
    STEP 1: GET Organization/Company information based on company_guid
    """
    USERNAME = "PandaHelpdesk"
    PWD = "7b6496618ae4ce853a26a3219478ddd0"
    URL = """https://helpdesk.panda-eco.com/app/admin_user/organization_info?token=8F33F9E2CA6911EBAECA42010A940064"""
    myobj = {
        "staff_guid": "D4150C86496211EAA915DED0BD1483FD",
        "organization_guid": company_guid # backend.company_profile.company_guid
    }

    try:
        response = requests.post(
                URL, 
                # json = {"output": ""},
                # headers = {},
                auth = (USERNAME, PWD),
                data = myobj
            )
        if response.status_code == 200:
            return response.json()

    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        return "Timeout Error"
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        return "Too Many Redirects"
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)

def get_userguid(response_item):
    """
    STEP 2: GET user_guid to be used to create new ticket 
    """
    organization_user_list = response_item["organization_user_list"] 
    # print("Organization List Length: ", len(organization_user_list))
    exist_counter = False

    default_user_guid = "5583163CC7E811E993063CA0676091C4"
    if len(organization_user_list) == 0:
        # IF Invalid company/organization guid used then use default guid
        return {
                "status": "NO",
                "user_guid": default_user_guid
            }

    for user_i in range(len(organization_user_list)):
        each_user = organization_user_list[user_i]
        # print(each_user["user_name"],each_user["user_email"])
        
        if "internaluse.com" in each_user["user_email"]:
            output =  {
                "status": "YES",
                "user_guid": each_user["user_guid"]
            }
            exist_counter = True
    
    if exist_counter != True:
            output =  {
                "status": "NO",
                "user_guid": default_user_guid
            }
    
    # print(output)
    return output


# company_info = organisation_info("05B9C525F99211EA8646DED0BD1483FD") # Original
# company_info = organisation_info('05B9C525F99211EA8646DED0BD1483FA') # Testing Department
# print(company_info)
# print(get_userguid(company_info))
# print(helpdesk_new_ticket(message))