"""
Version No: 1
Release Date: 22 September 2021 
KKSC
"""

# Pydantic Base Models
from datetime import datetime
from pydantic import BaseModel, constr, ValidationError, validator
from fastapi import HTTPException
from typing import Optional, List, Sequence

from sqlalchemy.sql.sqltypes import Boolean

class Receiver(BaseModel):
    output: dict

    class Config:
        orm_mode = True

"""
Below are full column models for the Panda Cloud Database
"""
class Company_Master_M(BaseModel):
    company_guid: str
    Name: str
    reg_no: Optional[str] = None
    address1: str
    address2: str
    address3: str
    address4: str
    postcode: str
    active: int

    class Config:
        orm_mode = True

class Company_Master_List(BaseModel):
    company_list: List[Company_Master_M]

class Company_Concept_M(BaseModel):
    company_guid: str
    concept_guid: str
    concept_name: str
    concept_parameter: str

    class Config:
        orm_mode = True

class Company_Outlet_M(BaseModel):
    company_guid: str
    concept_guid: str
    outlet_guid: str
    code: str
    name: str
    reg_no: str
    add1: str
    add2: str
    add3: str
    add4: str
    postcode: str
    active: int
    biz_date_start: datetime
    biz_date_end: datetime

    class Config:
        orm_mode = True


class Doc_Store_M(BaseModel):
    doc_guid: str
    company_guid: str
    outlet_guid: str
    doc_type: str
    document: dict
    created_at: datetime
    filter_stat: int

    class Config:
        orm_mode = True

"""
Input models below
"""

class Company_Outlet_in(BaseModel):
    company_guid: str
    concept_guid: str
    code: str
    name: str
    reg_no: str
    add1: str
    add2: str
    add3: str
    add4: str
    postcode: str
    active: int
    biz_date_start: datetime
    biz_date_end: datetime

    class Config:
        orm_mode = True

class Company_Concept_in(BaseModel):
    company_guid: str
    concept_name: str
    concept_parameter: dict

    class Config:
        orm_mode = True

class Flag_in(BaseModel):
    active_status: int
    outlet_guid: str

    class Config:
        orm_mode = True

class Company_Master_in(BaseModel):
    Name: str
    reg_no: str
    address1: str
    address2: str
    address3: str
    address4: str
    postcode: str
    active: int

    class Config:
        orm_mode = True

class Outlet_Update(BaseModel):
    company_guid: str
    concept_guid: str
    outlet_guid: str

    class Config:
        orm_mode = True

"""
Create New Customer
"""
class concept_all(BaseModel):
    concept_name: str
    class Config:
        orm_mode = True

class outlet_all(BaseModel):
    code: str
    name: str
    reg_no: str
    add1: str
    add2: str
    add3: str
    add4: str
    postcode: str
    active: int
    biz_date_start: datetime
    biz_date_end: datetime

    class Config:
        orm_mode = True

class master_all(BaseModel):
    master: Company_Master_in
    concept: concept_all
    outlet: outlet_all

    class Config:
        orm_mode = True

"""
Panda Agent Models Below
"""

class Compress_Agent(BaseModel):
    filename: str
    path_to_zip: str
    path_store_zip: str

    class Config:
        orm_mode = True

class Decompress_Agent(BaseModel):
    filename: str
    source_path: str
    path_store_zip: str

    class Config:
        orm_mode = True

class Sftp_config(BaseModel):
    hostname: str
    username: str
    password: str
    remoteFilePath: str
    localFilePath: str
    filename: str
    port: int

    class Config:
        orm_mode = True

class SqlDump(BaseModel):
    hostname: str
    port: str
    db_user: str
    db_pwd: str
    database_name: str
    dump_path: str
    pre_execute_script: str
    post_execute_script: str
    branch_code: str
    date_code: str
    hourly_code: str
    sequence_no: str
    table_main: str
    main_where_clause: str
    table_child1: str
    where_child1: str
    table_child2: str
    where_child2: str
    table_child3: str
    where_child3: str
    table_child4: str
    where_child4: str
    
    class Config:
        orm_mode = True

class Pending_Task(BaseModel):
    date_code: str
    hour: str
    sequence: str
    branch: str
    status: str

    class Config:
        orm_mode = True


# Task 5 6 7
class Task_List(BaseModel):
    database_name: str
    table_name: str
    task_status: str
    limit_record: int
    ascending: str

    @validator('ascending')
    def set_name(cls, name):
        return name or True

class Task_Status_Update(BaseModel):
    database_name: str
    table_name: str
    task_guid: str
    execute_time: str

class Create_Task_Agent(BaseModel):
    database_name: str
    tablename: str
    task_type: str
    store_code: str
    date_code: str
    hourly_code: str
    sequence: int
    task_status: int
    source_database_name: str
    source_table_name: str
    uncompress_checksum: str
    compress_checksum: str
    error: int
    resolve: int

class Bash_Task_List(BaseModel):
    task_type: str
    enable: int
    source_database_name: str
    source_table_name: str
    target_database_name: str
    target_table_name: str
    pre_execute_script: str
    query_script: str
    post_execute_script: str
    save_file_pre_script: str
    save_file_post_script: str
    last_run: datetime
    table_main: str
    table_child1: str
    table_child2: str
    table_child3: str
    table_child4: str
    task_database_name: str
    task_tablename: str
    where_main: str
    where_child1: str
    where_child2: str
    where_child3: str
    where_child4: str

class Last_Run(BaseModel):
    database_name: str
    table_name: str
    enable_in: str
    task_type_in: str

class Status_task(BaseModel):
    database_name: str
    table_name: str
    task_status_value: int
    ascending: str

class Pre_script(BaseModel):
    abs_path: str
    pre_script: str
    database_name: str

class Post_script(BaseModel):
    abs_path: str
    post_script: str

class Update_status_v2(BaseModel):
    database_name: str
    table_name: str
    task_status: str
    store_code: str
    date_code: str
    hour_code: str
    sequence: int

class GetSequenceFile(BaseModel):
    database_name: str
    table_name: str 
    store_code_in: str 
    task_type_in: str

class Md5_Check(BaseModel):
    filename_path: str
    filename: str

class Compressed_md5_update(BaseModel):
    database_name: str
    table_name: str
    compressed_md5: str
    store_code: str
    date_code: str
    hour_code: str
    sequence: str

class Restore_Param(BaseModel):
    file_source_path: str
    filename: str

class File_Check_Exist(BaseModel):
    file_path: str
    file_name: str