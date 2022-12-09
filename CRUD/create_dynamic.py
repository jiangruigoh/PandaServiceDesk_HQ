"""
Version No: 1
Release Date: 14 September 2021 
KKSC
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
from sqlalchemy import (MetaData, inspect)
from sqlalchemy.schema import CreateTable
import uuid
from sqlalchemy import exc
from fastapi import HTTPException

from Fast_API_files.Database import create_scoped_session_dynamic, create_engine_dynamic
from date_functions.Query_Date import current_date_only, current_time


Base = declarative_base()
metadata = MetaData()

def getModel(name, engine):
    """Create and return a new model class based on name
         name: database table name
         engine: the object returned by create_engine, specifying the database connection to be operated, from sqlalchemy import create_engine
    """
    try:
        Base.metadata.reflect(bind=engine)
        table = Base.metadata.tables[name]
        # print(table)
        t = type(name,(object,),dict())
        mapper(t, table)
        Base.metadata.clear()
        engine.dispose()
        return t
    except KeyError as e:
        raise HTTPException(status_code=422 , detail= "Invalid Tablename: " + str(e))

def createTableFromTable(name, tableNam, engine):
    """copy the structure of an existing table and create a new table
    """
    metadata = MetaData(engine)
    Base.metadata.reflect(engine)
    # Get the original table object
    table = Base.metadata.tables[tableNam]
    # Get the original table creation statement
    c = str(CreateTable(table))
    # Replace table name
    c = c.replace("CREATE TABLE " + tableNam, "CREATE TABLE if not exists " + name)
    db_conn = engine.connect()
    db_conn.execute(c)
    db_conn.close()
    Base.metadata.clear()

def getNewModel(name, tableNam, engine):
    """copy the table structure of a table and create a new table named name and return the model class
         name: database table name
         tableNam: copy table name
         engine: the object returned by create_engine, which specifies the database connection to be operated, from sqlalchemy import create_engine
    """
    createTableFromTable(name, tableNam, engine)
    return getModel(name, engine)


# CREATE Functions below
# Panda_Upload/from outlet
def create_task_agent(database_name_in, tablename_in, task_type, store_code, date_code, \
                      hourly_code, sequence, task_status, source_database, source_tablename, \
                    uncompress_checksum, compress_checksum, error, resolve):
    try:
        session = create_scoped_session_dynamic(database_name_in)
        tablename_used = getModel(tablename_in,create_engine_dynamic(database_name_in))
        # print(type(tablename_used))
        obj = tablename_used() # Create Instance of an object
        UID_2 = uuid.uuid1()
        uid = UID_2.hex.upper()

        # Insert data parameters of instance which have been created
        obj.database_name = source_database
        obj.table_name = source_tablename
        obj.task_guid = uid
        obj.task_type = task_type
        obj.store_code = store_code
        obj.date_code = date_code
        obj.hour_code = hourly_code
        obj.sequence = sequence
        obj.task_status = task_status
        obj.created_at = current_time()
        obj.uncompress_checksum = uncompress_checksum
        obj.compress_checksum = compress_checksum
        obj.last_update = current_time()
        obj.error = error
        obj.resolve = resolve
        
        # insp = inspect(tablename_used).keys()
        # result = list(insp.columns)
        # item = type(tablename_used)
        # print(insp)
        # print(result)

        session.add(obj)
        session.commit()
        session.close()
    
        return {'status_code': "200", 'data': "Successfully Created New Task",
                'data': obj}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= str(e))


def create_task_list(task_type, enable, source_database_name, source_table_name, target_database_name, target_table_name, \
                      pre_execute_script, query_script, post_execute_script, save_file_pre_script,\
                    save_file_post_script, last_run, table_main, table_child1, table_child2, table_child3,\
                    table_child4, task_database_name, task_tablename, \
                    where_main, where_child1, where_child2, where_child3, where_child4):
    try:
        session = create_scoped_session_dynamic(task_database_name)
        tablename_used = getModel(task_tablename,create_engine_dynamic(task_database_name))
        # print(type(tablename_used))
        obj = tablename_used() # Create Instance of an object
        UID_2 = uuid.uuid1()
        uid = UID_2.hex.upper()

        # Insert data parameters of instance which have been created
        obj.task_guid = uid
        obj.task_type = task_type
        obj.enable = enable
        obj.source_database_name = source_database_name
        obj.source_table_name = source_table_name
        obj.target_database_name = target_database_name
        obj.target_table_name = target_table_name
        obj.pre_execute_script = pre_execute_script
        obj.query_script = query_script
        obj.post_execute_script = post_execute_script
        obj.save_file_pre_script = save_file_pre_script
        obj.save_file_post_script = save_file_post_script
        obj.last_run = last_run
        obj.created_at = current_date_only()
        obj.table_main = table_main
        obj.table_child1 = table_child1
        obj.table_child2 = table_child2
        obj.table_child3 = table_child3
        obj.table_child4 = table_child4
        obj.where_main = where_main
        obj.where_child1 = where_child1
        obj.where_child2 = where_child2
        obj.where_child3 = where_child3
        obj.where_child4 = where_child4
        
        # insp = inspect(tablename_used).keys()
        # result = list(insp.columns)
        # item = type(tablename_used)
        # print(insp)
        # print(result)

        session.add(obj)
        session.commit()
        session.close()
    
        return {'status_code': "200", 'data': "Successfully Created New Task List"}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= str(e))

"""
def create_panda_task_upload(store_code, date_code, hourly_code, sequence, database_name, \
                      table_name, task_type, task_status):
    try:
        session = create_scoped_session_dynamic(database_name)
        tablename_used = getModel(table_name,create_engine_dynamic(database_name))
        # print(type(tablename_used))
        obj = tablename_used() # Create Instance of an object

        obj.store_code = store_code
        obj.task_type = task_type
        obj.date_code = date_code
        obj.hourly_code = hourly_code
        obj.sequence = sequence
        obj.task_status = task_status
        obj.created_at = current_time()

        session.add(obj)
        session.commit()
    
        return {'status_code': "200", 'data': "Successfully Created New Task Upload",
                'data': obj}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= str(e))
"""