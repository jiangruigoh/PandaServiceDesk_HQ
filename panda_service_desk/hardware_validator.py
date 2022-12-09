"""
# Functions to validate hardware information
Version No: 1
Release Date: 6 September 2021 
KKSC
"""

def cpu_checkpoint(cpu_info, SET_PERCENTAGE):
    current_cpu_usage = cpu_info["used_percentage"]
    if current_cpu_usage > SET_PERCENTAGE:
        return {"response": str(cpu_info["used_percentage"]) + " %" + "[ ALERT!! OVER " + str(SET_PERCENTAGE)+ "% ]" }
    else:
        return {"response": str(current_cpu_usage) + "% " +  "[OK]"}

def ram_checkpoint(ram_info, SET_PERCENTAGE):
    current_ram_usage = ram_info["used_percentage"]
    if current_ram_usage > SET_PERCENTAGE:
        # print("High RAM usage", str(ram_info["used_percentage"]))
        return {"response": str(ram_info["used_percentage"]) + " %" + "[ ALERT!! OVER " + str(SET_PERCENTAGE)+ "% ]"}
    else:
        return {"response": str(current_ram_usage) + "% " +  "[OK]" }

def partition_checkpoint(hardisk_info, SET_PERCENTAGE):
    hardisk_status = []
    for partition_i in range(len(hardisk_info)):
        each_partition = hardisk_info[partition_i]
        if ("loop" not in each_partition["device"]) and each_partition["used_percentage"] > SET_PERCENTAGE:
            # print(each_partition["device"], each_partition["used_percentage"])
            hardisk_status.append({"response": "Hardisk Usage: " + \
                each_partition["device"] + "    Current: " +  \
                    str(each_partition["used_percentage"]) + "% " +  "  [ ALERT!! OVER " + str(SET_PERCENTAGE)+ "% ]"})
        elif ("loop" not in each_partition["device"]) and each_partition["used_percentage"] < SET_PERCENTAGE:
            hardisk_status.append({"response": "Hardisk Usage: "  + each_partition["device"] + "    Current: " + str(each_partition["used_percentage"]) + "%" ",    Under " + str(SET_PERCENTAGE) + "% [OK]"})
    return hardisk_status