"""
# READ OPERATIONS
# SQLAlchemy
Version No: 1
Release Date: 14 September 2021 
KKSC
"""
from sqlalchemy import exc
from fastapi import HTTPException

from Fast_API_files.Database import create_scoped_session_dynamic, create_engine_dynamic
from CRUD.create_dynamic import getModel
from date_functions.Query_Date import current_time, current_date_only


def update_task_status(database_name_in, tablename_in, task_guid, execute_time):
    # FOR TESTING
    try:
        session = create_scoped_session_dynamic(database_name_in)
        tablename_used = getModel(tablename_in,create_engine_dynamic(database_name_in)) 
        
        session.query(tablename_used).filter(
        tablename_used.task_guid == task_guid).update(
            {
             tablename_used.last_run: current_date_only(),
             tablename_used.execute_time: execute_time
            },
            synchronize_session = False)
        session.commit()
        session.close()
        return {'status_code': "200", 'data': "Succesfully updated Task Status"}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))


def update_task_status_v2(database_name_in, tablename_in, task_status, \
    store_code, date_code, hour_code, sequence):
    # FOR batch_script_agent
    try:
        session = create_scoped_session_dynamic(database_name_in)
        tablename_used = getModel(tablename_in,create_engine_dynamic(database_name_in)) 
        
        session.query(tablename_used).filter(
        tablename_used.store_code == store_code,
        tablename_used.date_code == date_code,
        tablename_used.hour_code == hour_code,
        tablename_used.sequence == sequence).update(
            {
             tablename_used.task_status: task_status,
             tablename_used.last_update: current_time()
            },
            synchronize_session = False)
        session.commit()
        session.close()
        return {'status_code': "200", 'data': "Succesfully updated Task Status"}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))

def update_task_md5_checksum_compressed(database_name_in, tablename_in, md5_checksum, \
    store_code, date_code, hour_code, sequence):
    # FOR batch_script_agent
    try:
        session = create_scoped_session_dynamic(database_name_in)
        tablename_used = getModel(tablename_in,create_engine_dynamic(database_name_in)) 
        
        session.query(tablename_used).filter(
        tablename_used.store_code == store_code,
        tablename_used.date_code == date_code,
        tablename_used.hour_code == hour_code,
        tablename_used.sequence == sequence).update(
            {
             tablename_used.compress_checksum: md5_checksum,
             tablename_used.last_update: current_time()
            },
            synchronize_session = False)
        session.commit()
        session.close()
        return {'status_code': "200", 'data': "Succesfully updated Task Compressed MD5"}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))