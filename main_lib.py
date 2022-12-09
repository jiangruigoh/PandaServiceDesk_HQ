"""
Version No: 1
Release Date: 22 September 2021 
KKSC
"""


from Fast_API_files.tags import tags_metadata # Tag Descriptions
import yaml
import json

# Collections
import collections
from collections import OrderedDict
from collections import ChainMap

# FAST API .lib
from fastapi import FastAPI, Form, Body, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr, main
from typing import Optional, List
import uvicorn
import uuid

# Base Models
from Fast_API_files.Models import Receiver, Company_Master_M, Company_Concept_M, \
    Company_Outlet_M, Doc_Store_M, Company_Outlet_in, Company_Concept_in, \
    Flag_in, Company_Master_in, Outlet_Update, master_all, Compress_Agent, \
    Decompress_Agent, Sftp_config, Pending_Task, Company_Master_List, Task_List, \
    Task_Status_Update, Create_Task_Agent, SqlDump, Bash_Task_List, Last_Run, \
    Pre_script, Post_script, Status_task, Update_status_v2, GetSequenceFile, Md5_Check, \
    Compressed_md5_update, Restore_Param, File_Check_Exist

from date_functions.Query_Date import current_time, current_date_only, current_time_only

# Schemas
from Fast_API_files.schema import CompanyConcept, CompanyMaster, \
    CompanyOutlet, DocStore,  DocStoreLog

# Sessions/engine for SQL Alchemy
from Fast_API_files.Database import create_scoped_session

#SQL ALchemy .lib
from sqlalchemy import exc
from sqlalchemy import or_
from sqlalchemy.types import Unicode

# Validator
from panda_service_desk.validator import validator_main

# Helpdesk Functions
from panda_service_desk.helpdesk_requests import helpdesk_new_ticket

# Gzip functions
from panda_task_agent.compress_de_functions.g_zip import zip_agent, unzipper_agent

# Bz2 Functions
from panda_task_agent.compress_de_functions.b_zip import bzip_unzipper_agent, bzip_zip_agent

# SFTP functions
from panda_task_agent.SFTP.sftp_agent import SFTP_Connection

# READ
from CRUD.read import read_master, read_concept, read_outlet, read_docstore, read_docstore_item, \
    read_docstorelog, read_docstorelog_item, check_company_guid_exist, check_outlet_guid_exist, \
        get_threshold_mintransac

# CREATE
from CRUD.create import create_company, create_concept, create_outlet, create_doc_store, \
    create_doc_store_log

# UPDATE
from CRUD.update import flag_outlet_update, outlet_concept_update, update_doc_store_status

# Panda Task Agent CREATE
from CRUD.create_dynamic import create_task_agent, create_task_list

# Panda Task Agent READ
from CRUD.read_dynamic import task_listing, dynamic_test, get_active_task, get_status_task, get_task_upload_seq_no

# Panda Task Agent UPDATE
from CRUD.update_dynamic import update_task_status, update_task_status_v2, update_task_md5_checksum_compressed

# SQLDUMP 
from panda_task_agent.mysqldump.sql_dump import *

# PRE_append/append 
from panda_task_agent.mysqldump.script_append import pre_append, post_append

# MD5 Checksum
from panda_task_agent.md5_checksum import cal_checksum

# Restore SQL file
from panda_task_agent.restore_sqldump_agent import restore_agent

# File Check exist
from panda_task_agent.general_functions.file_exist_check import file_exist_checker