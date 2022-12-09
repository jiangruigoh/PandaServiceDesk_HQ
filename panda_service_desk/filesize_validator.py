"""
# Check FileSize
Version No: 1
Release Date: 15 September 2021 
KKSC
"""

def size_checker(file_lst, FILESIZE_SET_VALUE):
    # Handles B, KB, MB, GB
    status = True
    below_size_list = []
    print(FILESIZE_SET_VALUE)
    # FILESIZE_SET_VALUE = 0.8 # NEED CHECK

    for row in range(len(file_lst)):
        row_item = file_lst[row]
        # row_item["size"]
        # row_item["filename"]
        row_split = row_item["size"].split()
        size_unit_name = row_split[1]
        size_value = row_split[0]
        # print(size_unit_name)

        if "B" in size_unit_name and len(size_unit_name) == 1:
            # =========== NEW SECTION =============#
            if isinstance(FILESIZE_SET_VALUE, float) == True: # IF SET VALUE IS FLOAT
                BYTES_USED_VALUE = FILESIZE_SET_VALUE * 1000
                if size_value < BYTES_USED_VALUE:
                    below_size_list.append(row_item)
            # =========== NEW SECTION =============#
        elif "KB" in size_unit_name:
            if isinstance(FILESIZE_SET_VALUE, float) == True: # IF SET VALUE IS FLOAT
                continue
            # =========== NEW SECTION REMOVED =============#
            
            elif float(size_value) < FILESIZE_SET_VALUE and isinstance(FILESIZE_SET_VALUE, float) == False:
                below_size_list.append(row_item)
            else:
                continue
            
            # =========== NEW SECTION REMOVED =============#

        elif "MB" in size_unit_name:
            continue
        elif "GB" in size_unit_name:
            continue
    
    # Checks IF there are any files below set value
    if len(below_size_list) == 0:
        status = True
        return {"filelist": [],
                "status": status}
    else:
        status = False
        return {"filelist": below_size_list,
                "status": status}

    
