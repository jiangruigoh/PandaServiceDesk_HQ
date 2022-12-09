"""
# READ OPERATIONS
# SQLAlchemy
Version No: 1
Release Date: 20 August 2021 
KKSC
"""

from date_functions.Query_Date import current_date_only, current_date_code, current_hourly_code, converter_to_obj
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
from sqlalchemy import (MetaData, inspect)
from sqlalchemy.schema import CreateTable
from sqlalchemy import exc, asc, desc, cast, Date
from fastapi import HTTPException
from sqlalchemy.sql.expression import table

from Fast_API_files.Database import create_scoped_session_dynamic, create_engine_dynamic
from CRUD.create_dynamic import getModel

Base = declarative_base()
metadata = MetaData()

# Task 22 July 2021
def dynamic_test(database_name):
    session = create_scoped_session_dynamic(database_name)
    output = []
    try:
        inspector = inspect(create_engine_dynamic(database_name))
        schemas = inspector.get_schema_names()
        # print(schemas)
        for schema in schemas:
            if schema == database_name:
                # print("schema: %s" % schema)
                for table_name in inspector.get_table_names(schema=schema):
                    # print(table_name)
                    tablename_used = getModel(table_name, create_engine_dynamic(database_name))
                    result = session.query(tablename_used).all()
                    # output.append(result)

                    json_output = {
                        "table_name" : table_name,
                        "records": result
                    }
                    output.append(json_output)
                    #for column in inspector.get_columns(table_name, schema=schema):
                    #    print("Column: %s" % column)
        return output
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))


# Task 7: List Task
def task_listing(database_name, table_name, task_status, limit_counter, ascending):
    session = create_scoped_session_dynamic(database_name)
    tablename_used = getModel(table_name, create_engine_dynamic(database_name))
    
    #order = ascending
    #column_sorted = getattr(tablename_used.hourly_code, order)()
    # 1. store_code
    # 2. date_code
    # 3. hourly_code
    # 4. sequence 

    #sort_column = tablename_used.store_code, tablename_used.date_code,\
                   #tablename_used.hourly_code, tablename_used.sequence
    # print(ascending)
    # print(type(False))
    asc_uppercase = ascending.upper()

    if asc_uppercase == "FALSE":
        sort1 = desc(tablename_used.store_code)
        sort2 = desc(tablename_used.date_code)
        sort3 = desc(tablename_used.hourly_code)
        sort4 = desc(tablename_used.sequence)
    elif asc_uppercase == "TRUE":
        sort1 = asc(tablename_used.store_code)
        sort2 = asc(tablename_used.date_code)
        sort3 = asc(tablename_used.hourly_code)
        sort4 = asc(tablename_used.sequence)
    else:
        return { "Error" :  "ascending parameter can only be True or False"}
    
    # sort = asc(sort_column) if sort_dir == "desc" else desc(sort_column)
    # query = Query([...]).filter(...)
    # query = query.order_by(sort)
    # results = session.execute(query).fetchall()

    try:
        # print(sort1, sort2, sort3, sort4)
        result = session.query(tablename_used).\
            filter_by(task_status=task_status).\
            order_by(sort1, sort2, sort3, sort4).\
            limit(limit_counter).all()
        # print(result)
        session.close()
        """
        for i in range(len(result)):
            row = result[i]
            store_code = row.store_code
            date_code = row.date_code
            hourly_code = row.hourly_code
            sequence = row.sequence
            print(store_code, date_code, hourly_code, sequence)
        """
        return { "task_list" : result }
        
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))


def get_active_task(database_name, table_name, enable_in, task_type_in):
    session = create_scoped_session_dynamic(database_name)
    tablename_used = getModel(table_name, create_engine_dynamic(database_name))

    try:
        result = session.query(tablename_used).\
            filter_by(enable=enable_in,
                    task_type=task_type_in
                    ).\
            filter(tablename_used.last_run!=current_date_only()).all()
        # print(result)
        
        session.close()

        return { "active_task" : result }
        
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))


def get_status_task(database_name, table_name, status_val, ascending):
    session = create_scoped_session_dynamic(database_name)
    tablename_used = getModel(table_name, create_engine_dynamic(database_name))

    try:
        asc_uppercase = ascending.upper()

        if asc_uppercase == "FALSE":
            sort1 = desc(tablename_used.store_code)
            sort2 = desc(tablename_used.date_code)
            sort3 = desc(tablename_used.hour_code)
            sort4 = desc(tablename_used.sequence)
        elif asc_uppercase == "TRUE":
            sort1 = asc(tablename_used.store_code)
            sort2 = asc(tablename_used.date_code)
            sort3 = asc(tablename_used.hour_code)
            sort4 = asc(tablename_used.sequence)
        else:
            return { "Error" :  "ascending parameter can only be True or False"}

        result = session.query(tablename_used).\
            filter_by(task_status=status_val).\
            order_by(sort1, sort2, sort3, sort4).all()
        # print(result)
        
        session.close()

        return { "data" : result }
        
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()


# print(get_active_task("batch_script_agent", "task_list", 1, "2021-08-16","daily"))

def get_task_upload_seq_no(database_name, table_name, store_code_in, task_type_in):
    session = create_scoped_session_dynamic(database_name)
    tablename_used = getModel(table_name, create_engine_dynamic(database_name))
    date_code = current_date_code()
    hourly_code = current_hourly_code()
    current_date_string = current_date_only()
    current_date_obj = converter_to_obj(current_date_string)
    try:
        result = session.query(tablename_used).\
            filter_by(store_code=store_code_in,
                        task_type = task_type_in).\
            filter(tablename_used.created_at.cast(Date) == current_date_obj,
                    tablename_used.hour_code == hourly_code).all()
        session.close()
        # print(result)
        
        # 3-2 Assign today date 1st running number
        if (len(result) == 0):
            return {"last_sequence": "0001",
                    "date_code": date_code,
                    "hourly_code": hourly_code,
                    "branch_code": store_code_in
                    }
        else:
            # 3-1 Get today date last running number +1
            sequence_list = []
            for i in range(len(result)):
                row = result[i]
                # print(row.sequence)
                sequence_list.append(row.sequence) # REMEMBER DON'T CHANGE TO STRING WHEN CHECK MAX
            last_sequence = max(sequence_list) 
            add_last_sequence = str(int(last_sequence) + 1).zfill(4)
            # print(add_last_sequence)
            return { "last_sequence": str(add_last_sequence),
                     "date_code": date_code,
                     "hourly_code": hourly_code,
                     "branch_code": store_code_in 
                    }

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))

# print(get_task_upload_seq_no("batch_script_agent", "task_upload", "SB01", "daily"))

