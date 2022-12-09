"""
Version No: 1
Release Date: 22 September 2021 
KKSC
"""

from sqlalchemy import sql
import yaml
from main_lib import *

"""GET Configuration parameters"""
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    #print(cfg)

# UVICON Configuration Variables
uvicorn_host = cfg["uvicorn"]["host"]
uvicorn_port = cfg["uvicorn"]["port"]
uvicorn_reload_status = cfg["uvicorn"]["reload"]

# Closing File
ymlfile.close()
# Initialize APP
app = FastAPI( openapi_tags=tags_metadata(),
               title="Panda Server Cloud",
               description=""" """
              )

app.add_middleware(
    CORSMiddleware,#CORS ORIGIN
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Receive and Save Server information (JSON) to Database
@app.post("/server_info_get", tags=["POST"])
async def customerServerDetails(user_json:Receiver):
    """
    Receives Server Information from outlet server:
    - **JSON** Format \n
        IF: outlet_guid or company_guid not exist \n
            THEN save at the DocStoreUnassign Table \n
        ELSE: save at DocStore Table which has FK 
    """
    # print(user_json.output)
    # pretty_print = json.dumps(user_json.output, indent=4) # FOR VIEWING PURPOSE ONLY
    # print(pretty_print)

    panda_internal_guid = "8745268A0A7C11EA9AC6DED0BD1483FD"

    json_opt = user_json.output
    config_level = json_opt["config"]

    company_guid_json = config_level["company_guid"]
    # print(company_guid_json)
    outlet_guid_json = config_level["outlet_guid"]
    outlet_code_json = config_level["outlet_code"]
    # print(outlet_guid_json)
    

    try: # Check if concept and company ids exist
        check_guid_exist_cpy = check_company_guid_exist(company_guid_json)
        check_guid_exist_olt = check_outlet_guid_exist(outlet_guid_json)

        if (check_guid_exist_cpy == None):
            ticket_msg_ids = "Outlet Code: " +  str(config_level["outlet_code"]) + "<br>"  + "Company_name: " + str(config_level["company_name"]) +  "<br>"  + "Invalid Company_Guid"
            helpdesk_new_ticket(ticket_msg_ids, panda_internal_guid, outlet_code_json)
            raise HTTPException(status_code=404, detail="No Such company GUID")
        elif (check_guid_exist_olt == None):
            ticket_msg_ids = "Outlet Code: " +  str(config_level["outlet_code"]) + "<br>"  + "Company_name: " + str(config_level["company_name"]) +  "<br>" +  "Invalid Outlet_Guid"
            helpdesk_new_ticket(ticket_msg_ids, panda_internal_guid, outlet_code_json)
            raise HTTPException(status_code=404, detail="No Such outlet GUID")
        else:
            outlet_name = check_guid_exist_olt.name

            # Create
            doc_store_result = create_doc_store(company_guid_json, outlet_guid_json, \
                                    current_date_only(), current_time_only(), json_opt)
            doc_uid = doc_store_result["data"]

            # Get Validator Threshold parameter json to be given to validator
            threshold_json = get_threshold_mintransac(outlet_guid_json)

            # Validation Section
            validator_json = validator_main(json_opt, company_guid_json, outlet_name, outlet_code_json,\
                threshold_json)
            validator_status = validator_json["status"]
            validated_issue_opt = validator_status["validated_issue"]
            
            # Update Doc_Store Status to 1
            update_doc_store_status(doc_uid)
            
            # Doc Log Store Section
            create_doc_store_log(doc_uid, validator_status, validated_issue_opt)
            
    except exc.SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=422 , detail= "Incorrect column Format")

    return {'status_code': "200", 'data': user_json}

# Create New Company
@app.post("/create_new_company", tags=["POST"])
async def create_new_company(company_schem:Company_Master_in):
    return create_company(company_schem)


# Create New Concept
@app.post("/create_new_concept", tags=["POST"])
async def create_new_outlet(concept_schem:Company_Concept_in):
    """
    Creates New Concept for existing Company:
    - **Company_guid Must exist** \n
    Upon Success, save to database
    """
    return create_concept(concept_schem)

# Create New Outlet
@app.post("/create_new_outlet", tags=["POST"])
async def create_new_outlet(outlet_schem:Company_Outlet_in):
    """
    Creates New outlet:
    - **Outlet_guid/company_guid Must exist** \n
    Upon Success, Save to database
    """
    return create_outlet(outlet_schem)

# Flag outlet active column
@app.post("/flag_outlet", tags=["UPDATE"])
async def flag_outlet(flag_schem: Flag_in):
    """
    Update Flag for Outlet
    """
    return flag_outlet_update(flag_schem)

# Update Outlet Concept
@app.post("/update_outlet_concept", tags=["UPDATE"])
async def update_outlet_concept(outlet_schem:Outlet_Update):
    """
    Creates New outlet:
    - **Outlet_guid/company_guid Must exist** \n
    Upon Success, Save to database
    """
    return outlet_concept_update(outlet_schem)

# Output master Table
@app.get("/get_master", tags=["READ"], response_model=Company_Master_List)
async def get_master():
    """
    Output Master Table:
    """
    return read_master()
    

# Output concept Table
@app.get("/get_concept", tags=["READ"])
async def get_concept():
    """
    Output concept Table:
    """
    return read_concept()


# Output Outlet Table
@app.get("/get_outlet", tags=["READ"])
async def get_outlet():
    """
    Output Outlet Table:
    """
    return read_outlet()


# Output Doc_Store Table
@app.get("/get_doc_store", tags=["READ"])
async def get_doc_store():
    """
    Output Doc_store Table:
    """
    return read_docstore()

# Output Doc_Store based on parameters
@app.get("/get_doc_store_item", tags=["READ"])
async def get_doc_store_item(company_guid:str, outlet_guid:str, created_date: str):
    """
    Get Doc Store information with parameters \n
    param_1: company_guid \n
    param_2: outlet_guid
    """
    return read_docstore_item(company_guid, outlet_guid, created_date)

# Output Doc_Store_Log Table
@app.get("/get_doc_store_log", tags=["READ"])
async def get_doc_store_log():
    """
    Output Doc_store_log Table:
    """
    return read_docstorelog()

@app.get("/get_doc_store_log_item", tags=["READ"])
async def get_doc_store_log_item(doc_store_guid: str):
    """
    Get Doc Store Log information with parameters \n
    param: doc_store_guid \n
    """
    return read_docstorelog_item(doc_store_guid)

# Script Agent Section Below
@app.post("/compress", tags=["File Compress/Decompress"])
async def compress(compress_model: Compress_Agent, compress_mode:str):
    """
    Compress files using b_zip \n
    compress_mode: bz2 or gz \n
    param_1: filename \n
    param_2: path_to_zip \n
    param_3: path_store_zip
    """
    if compress_mode == "bz2":
        zip_counter = 0
        result = bzip_zip_agent(
            compress_model.filename,
            compress_model.path_to_zip, 
            compress_model.path_store_zip
        )
        while result == "Corrupted":
            result = bzip_zip_agent(
            compress_model.filename,
            compress_model.path_to_zip, 
            compress_model.path_store_zip
            )
            zip_counter+=1
    elif compress_mode == "gz":
        zip_counter = 0
        result = zip_agent(
            compress_model.filename,
            compress_model.path_to_zip, 
            compress_model.path_store_zip
        )
        while result == "Corrupted" and zip_counter<=3:
            result = zip_agent(
            compress_model.filename,
            compress_model.path_to_zip, 
            compress_model.path_store_zip
            )
            zip_counter+=1
    else:
        result = HTTPException(status_code=404, detail="Invalid Mode for compression")
    
    return result

@app.post("/decompress", tags=["File Compress/Decompress"])
async def decompress(decompress_model: Decompress_Agent):
    """
    Decompress files gz or bz2 format only \n
    param_1: filename \n
    param_2: source_path \n
    param_3: path_store_zip
    """
    if decompress_model.filename.endswith(".gz"):
        result = unzipper_agent(
            decompress_model.filename,
            decompress_model.source_path,
            decompress_model.path_store_zip
        )
    elif decompress_model.filename.endswith(".bz2"):
        result = bzip_unzipper_agent(
            decompress_model.filename,
            decompress_model.source_path,
            decompress_model.path_store_zip
        )
    else:
        result = HTTPException(status_code=404, detail="Invalid file type for decompression")
    
    return result

@app.post("/download_sftp", tags=["SFTP Agent"])
async def download_sftp(sftp_config: Sftp_config):
    """
        Download via SFTP \n
        param_1: filename \n
        param_2: remoteFilePath \n
        param_3: localFilePath
    """
    sftp_obj = SFTP_Connection()
    sftp_obj.hostname = sftp_config.hostname
    sftp_obj.username = sftp_config.username
    sftp_obj.pwd = sftp_config.password
    sftp_obj.port = sftp_config.port

    # DOWNLOAD
    sftp_obj.connect() # Create Connection
    sftp_obj.filename = sftp_config.filename
    sftp_obj.remoteFilePath = sftp_config.remoteFilePath
    sftp_obj.localFilePath = sftp_config.localFilePath
    print(sftp_obj.dir_checkpoint_local())
    result = sftp_obj.download()

    print(sftp_obj.check_integrity_local())
    print(sftp_obj.check_integrity_remote())
    local_checksum = sftp_obj.check_integrity_local()
    remote_checksum = sftp_obj.check_integrity_remote()

    #REMEMBER TO MAKE LOOP FOR NOT THE SAME CHECKSUM
    download_counter = 0
    while local_checksum != remote_checksum and download_counter <= 3:
        sftp_obj.dir_checkpoint_remote()
        result = sftp_obj.download()
        download_counter +=1


    sftp_obj.close_session()
    return result

@app.post("/upload_sftp", tags=["SFTP Agent"])
async def upload_sftp(sftp_config: Sftp_config):
    """
        Upload via SFTP \n
        param_1: filename \n
        param_2: remoteFilePath \n
        param_3: localFilePath
    """
    sftp_obj = SFTP_Connection()
    sftp_obj.hostname = sftp_config.hostname
    sftp_obj.username = sftp_config.username
    sftp_obj.pwd = sftp_config.password
    sftp_obj.port = sftp_config.port

    # UPLOAD
    sftp_obj.connect()
    sftp_obj.filename = sftp_config.filename
    sftp_obj.remoteFilePath = sftp_config.remoteFilePath
    sftp_obj.localFilePath = sftp_config.localFilePath
    
    filename_local_existence = sftp_obj.filename_checkpoint_local()
    if "No such file or directory" in filename_local_existence:
        raise HTTPException(status_code=422, detail=str(filename_local_existence))

    print(sftp_obj.dir_checkpoint_remote())
    print(sftp_obj.file_checkpoint_remote())
    result = sftp_obj.upload()

    print(sftp_obj.check_integrity_local())
    sftp_obj.check_integrity_remote()
    local_checksum = sftp_obj.check_integrity_local()
    remote_checksum = sftp_obj.check_integrity_remote()

    # Runs 3 times before termination upon failure
    upload_counter = 0
    while local_checksum != remote_checksum and upload_counter <= 3:
        sftp_obj.dir_checkpoint_remote()
        result = sftp_obj.upload()
        upload_counter +=1

    sftp_obj.close_session()
    return result

@app.post("/sqldump", tags=["MySqlDump"], status_code=201)
async def sqldump(dump_mdl: SqlDump):
    sql_dump = SqlDumper()
    sql_dump.hostname = dump_mdl.hostname
    sql_dump.port = dump_mdl.port
    sql_dump.db_user = dump_mdl.db_user 
    sql_dump.db_pwd = dump_mdl.db_pwd 
    sql_dump.database_name = dump_mdl.database_name
    sql_dump.table_main = dump_mdl.table_main 
    sql_dump.where_clause_main = dump_mdl.main_where_clause
    sql_dump.dump_path = dump_mdl.dump_path 
    sql_dump.pre_item = dump_mdl.pre_execute_script
    sql_dump.end_item = dump_mdl.post_execute_script
    sql_dump.branch_code = dump_mdl.branch_code
    sql_dump.date_code = dump_mdl.date_code
    sql_dump.hourly_code = dump_mdl.hourly_code
    sql_dump.sequence_no = dump_mdl.sequence_no
    sql_dump.table_child1 = dump_mdl.table_child1
    sql_dump.table_child2 = dump_mdl.table_child2
    sql_dump.table_child3 = dump_mdl.table_child3
    sql_dump.table_child4 = dump_mdl.table_child4
    sql_dump.where_clause_child1 = dump_mdl.where_child1
    sql_dump.where_clause_child2 = dump_mdl.where_child2
    sql_dump.where_clause_child3 = dump_mdl.where_child3
    sql_dump.where_clause_child4 = dump_mdl.where_child4

    # STEP 2: Check if dump path exist
    path_status = sql_dump.path_checkpoint() # Creates new directory if not exist'

    if path_status != True:
        HTTPException(status_code=422, detail=path_status)

    # print(sql_dump.file_checkpoint())
    sql_dump.abs_path_join() # Get the absolute path for sqldump
    
    sqldump_status = sql_dump.run() # Creates Backup file Raw

    return {
                "dump_path_status": path_status,
                "sqldump_status": sqldump_status,
                "dump_path_abs": sql_dump.abs_dump_path
            }

@app.post("/pre_script_append", tags=["Panda Task Agent"])
async def pre_script_append(pre_mdl: Pre_script):
    """
        Pre-Append Script to file
    """
    return pre_append(pre_mdl.abs_path, pre_mdl.pre_script, pre_mdl.database_name)


@app.post("/post_script_append", tags=["Panda Task Agent"])
async def post_script_append(post_mdl: Post_script):
    """
        Pre-Append Script to file
    """
    return post_append(post_mdl.abs_path, post_mdl.post_script)


@app.post("/list_task", tags=["Panda Task Agent"])
async def list_task(task_list: Task_List):
    """
        7: List Task for Panda Task Agent --TEST USAGE
    """
    return task_listing(task_list.database_name, task_list.table_name,\
         task_list.task_status, task_list.limit_record, task_list.ascending)


@app.post("/create_task_agent", tags=["Panda Task Agent"])
async def create_task(create_task: Create_Task_Agent):
    """
        Create Panda Task: PandaUpload/from_outlet
    """
    return create_task_agent(create_task.database_name, create_task.tablename,\
            create_task.task_type, create_task.store_code,
            create_task.date_code, create_task.hourly_code, create_task.sequence,
            create_task.task_status, create_task.source_database_name, create_task.source_table_name,\
            create_task.uncompress_checksum, create_task.compress_checksum,
            create_task.error, create_task.resolve)

@app.post("/dynamic_database_read", tags=["Panda Task Agent"])
async def dynamic_database_read(database_name: str):
    """
        List Whole Database items
    """
    return dynamic_test(database_name)

@app.post("/create_task_list_record", tags=["Panda Task Agent"])
async def create_task_list_record(mdl: Bash_Task_List):
    """
        Create New entry for Task List
    """
    return create_task_list(mdl.task_type, mdl.enable, mdl.source_database_name, mdl.source_table_name, \
    mdl.target_database_name, mdl.target_table_name, mdl.pre_execute_script, mdl.query_script, mdl.post_execute_script,\
    mdl.save_file_pre_script, mdl.save_file_post_script, mdl.last_run, mdl.table_main, mdl.table_child1, mdl.table_child2,\
    mdl.table_child3, mdl.table_child4, mdl.task_database_name, mdl.task_tablename,\
    mdl.where_main, mdl.where_child1, mdl.where_child2, mdl.where_child3, mdl.where_child4)

@app.post("/get_task_last_run", tags=["Panda Task Agent"])
async def get_task_last_run(mdl: Last_Run):
    return get_active_task(mdl.database_name, mdl.table_name, mdl.enable_in, mdl.task_type_in)

@app.post("/get_task_status", tags=["Panda Task Agent"])
async def get_task_status(mdl: Status_task):
    return get_status_task(mdl.database_name, mdl.table_name, mdl.task_status_value, mdl.ascending)

@app.post("/task_status_update", tags=["Panda Task Agent"])
async def task_status_update(task_update: Task_Status_Update):
    """
        6: Update batch_script_agent.task_list table.last_run to latest datetime
    """
    return update_task_status(task_update.database_name, task_update.table_name,task_update.task_guid, task_update.execute_time)

@app.post("/get_sequence_no", tags=["Panda Task Agent"])
async def get_sequence_no(mdl: GetSequenceFile):
    """
        6: Get Sequence No
    """
    return get_task_upload_seq_no(mdl.database_name, mdl.table_name, mdl.store_code_in, mdl.task_type_in)

@app.post("/task_status_update_v2", tags=["Panda Task Agent"])
async def task_status_update_v2(mdl: Update_status_v2):
    """
        6: Update Task Status 
    """
    return update_task_status_v2(mdl.database_name, mdl.table_name, mdl.task_status,mdl.store_code,\
        mdl.date_code, mdl.hour_code, mdl.sequence)

@app.post("/cal_MD5_checksum", tags=["Panda Task Agent"])
async def cal_MD5_checksum(mdl: Md5_Check):
    """
        6: Calculates MD5_CHECKSUM
    """
    return cal_checksum(mdl.filename_path, mdl.filename)


@app.post("/update_compressed_MD5_checksum", tags=["Panda Task Agent"])
async def update_compressed_MD5_checksum(mdl: Compressed_md5_update):
    """
        6: Update MD5 Checksum 
    """
    return update_task_md5_checksum_compressed(mdl.database_name, mdl.table_name, mdl.compressed_md5, mdl.store_code,\
        mdl.date_code, mdl.hour_code, mdl.sequence)

@app.post("/restore_sql", tags=["Panda Task Agent"])
async def restore_sql(mdl: Restore_Param):
    """
        6: Restore SQL SCRIPT
    """
    return restore_agent(mdl.file_source_path, mdl.filename)

@app.post("/file_exist_checker", tags=["Panda Task Agent"])
async def file_exist_check(mdl: File_Check_Exist):
    """
        Check File Exist on path
    """
    return file_exist_checker(mdl.file_path, mdl.file_name)

"""
if __name__ == "__main__":
    uvicorn.run('main:app', host = uvicorn_host, port = uvicorn_port, reload=True) #, workers=multiprocessing.cpu_count())
"""
