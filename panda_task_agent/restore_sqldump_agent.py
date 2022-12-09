# MYSQL Restore Dump File Agent
"""
Version No: 1
Release Date: 15 September 2021 
KKSC
"""

# param_1: source_path
# param_2: filename
# param_3: database_name # Got USE database_name; in script hence no need to point to database
import os
import mysql.connector
import json
import yaml



def connect():
    """GET Configuration parameters"""
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        #print(cfg)

    # UVICON Configuration Variables
    #uvicorn_host = cfg["mysql"]["host"]
    #uvicorn_user = cfg["mysql"]["user"]
    #uvicorn_pass = cfg["mysql"]["passwd"]
    #uvicorn_db = cfg["mysql"]["db"]
    #uvicorn_port = cfg["mysql"]["port"]
    
    mydb = mysql.connector.connect(
            host = cfg["mysql"]["host"],
            user = cfg["mysql"]["user"],
            password=cfg["mysql"]["passwd"],
            port = cfg["mysql"]["port"]
        )

    ymlfile.close() # ALWAYS REMMEBER TO CLOSE FILE AFTER USE

    return mydb

def restore_agent(source_path, filename):
    mydb = connect()
    if isinstance(mydb, object):
        try:
            # Join various path components
            write_path_file = os.path.join(source_path, filename)
            # print("File Absolute Path: " + str(write_path_file))
            mycursor = mydb.cursor()
            with open(write_path_file, 'r') as sql_file:
                sql_file_content = sql_file.read()
                result_interation = mycursor.execute(sql_file_content, multi=True)
            for res in result_interation:
                print("Running query: ", res)
                if res.with_rows:
                    fetch_result = res.fetchall()
                    fetch_parsed = json.dumps(fetch_result, indent=4)
                elif res.rowcount > 0:
                    affected_rows = res.rowcount
                    print(f"Affected {res.rowcount} rows" )

            # mydb.commit()
            sql_file.close()
            mycursor.close()
            
            return {"status": "success",
                                "data": {
                                    "filename": filename,
                                    "filepath": source_path
                                },
                                "message": "Affected rows: " + str(affected_rows),
                                "code": 200
                    }

        except mysql.connector.Error as err:
            # error_msg = "Error: {}".format(err)
            return {"status": "fail",
                    "data": {
                        "filename": filename,
                        "filepath": source_path
                    },
                    "message": str(err),
                    "code": 422
            }

# restore_agent("/home/panda/test_SFTP/Test_dir/new", "PANDA_20210915_16_0001.sql")


