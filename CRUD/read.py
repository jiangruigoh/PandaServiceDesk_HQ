"""
# READ OPERATIONS
# SQLAlchemy
Version No: 1
Release Date: 9 July 2021 
KKSC
"""

from Fast_API_files.Database import create_scoped_session
from Fast_API_files.Models import Receiver, Company_Master_M, Company_Concept_M, \
    Company_Outlet_M, Doc_Store_M, Company_Outlet_in, Company_Concept_in, \
    Flag_in, Company_Master_in, Outlet_Update, master_all, Compress_Agent, \
    Decompress_Agent, Sftp_config, Pending_Task, Company_Master_List
from Fast_API_files.schema import CompanyConcept, CompanyMaster, \
    CompanyOutlet, DocStore,  DocStoreLog

from sqlalchemy import exc
from fastapi import HTTPException

def read_master():
    session = create_scoped_session()
    company_list = []
    try:
        for row in session.query(CompanyMaster).all():
            row_output = Company_Master_M (
                company_guid = row.company_guid,
                Name = row.Name,
                reg_no = row.reg_no,
                address1 = row.address1,
                address2 = row.address2,
                address3 = row.address3,
                address4 = row.address4,
                postcode = row.postcode,
                active = row.active
            )
            company_list.append(row_output)

        session.close()
        return { "company_list" : company_list }

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")

def read_concept():
    session = create_scoped_session()
    concept_list = []
    try:
        for row in session.query(CompanyConcept).all():
            row_output = CompanyConcept(
                company_guid = row.company_guid,
                concept_guid = row.concept_guid,
                concept_name = row.concept_name,
                concept_parameter = row.concept_parameter
            )
            concept_list.append(row_output)

        session.close()
        return { "concept_list" : concept_list }

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")

def read_outlet():
    session = create_scoped_session()
    outlet_list = []
    try:
        for row in session.query(CompanyOutlet).all():
            row_output = CompanyOutlet(
                company_guid = row.company_guid,
                concept_guid = row.concept_guid,
                outlet_guid = row.outlet_guid,
                code = row.code,
                name = row.name,
                reg_no = row.reg_no,
                add1 = row.add1,
                add2 = row.add2,
                add3 = row.add3,
                add4 = row.add4,
                postcode = row.postcode,
                active = row.active,
                biz_date_start = row.biz_date_start,
                biz_date_end = row.biz_date_end,
            )
            outlet_list.append(row_output)

        session.close()
        return { "outlet_list" : outlet_list }

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")
    
def read_docstore():
    session = create_scoped_session()
    doc_store_list = []
    try:
        for row in session.query(DocStore).all():
            row_output = DocStore(
                doc_guid = row.doc_guid,
                company_guid = row.company_guid,
                outlet_guid = row.outlet_guid,
                doc_type = row.doc_type,
                document =  row.document,
                created_date =  row.created_date,
                created_time = row.created_time
            )
            doc_store_list.append(row_output)

        session.close()
        return { "doc_store_list" : doc_store_list }
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")
    
def read_docstore_item(company_guid, outlet_guid, created_date):
    session = create_scoped_session()
    doc_store_list = []
    try:
        result = session.query(DocStore).filter(DocStore.company_guid == company_guid,
                                                DocStore.outlet_guid == outlet_guid,
                                                DocStore.created_date == created_date)
        for row in result:
            doc_store_json = DocStore(
                doc_guid = row.doc_guid,
                company_guid = row.company_guid,
                outlet_guid = row.outlet_guid,
                doc_type = row.doc_type,
                document = row.document,
                created_date = row.created_date,
                created_time = row.created_time
            )
            doc_store_list.append(doc_store_json)
        
        session.close()
        return { "doc_store_list" : doc_store_list }

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")


def read_docstorelog():
    session = create_scoped_session()
    doc_store_log_list = []
    try:
        for row in session.query(DocStoreLog).all():
            row_output = DocStoreLog(
                log_guid = row.log_guid,
                doc_store_guid = row.doc_store_guid,
                log_type = row.log_type,
                status = row.status,
                message = row.message,
                validated_issue = row.validated_issue
            )
            doc_store_log_list.append(row_output)

        session.close()
        return { "doc_store_log_list" : doc_store_log_list }

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")
    
   
def read_docstorelog_item(doc_store_guid):
    session = create_scoped_session()
    doc_store_log_list = []
    try:
        result = session.query(DocStoreLog).filter(DocStoreLog.doc_store_guid == doc_store_guid)
        for row in result:
            row_output = DocStoreLog(
                log_guid = row.log_guid,
                doc_store_guid = row.doc_store_guid,
                log_type = row.log_type,
                status = row.status,
                message = row.message
            )
            doc_store_log_list.append(row_output)

        session.close()
        return { "doc_store_log_list" : doc_store_log_list }

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")

def check_company_guid_exist(company_guid_json):
    session = create_scoped_session()
    try:
        result = session.query(CompanyMaster).\
                              filter(CompanyMaster.company_guid == company_guid_json).first()
        session.close()
        return result

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")

def check_outlet_guid_exist(outlet_guid_json):
    session = create_scoped_session()
    try:
        result = session.query(CompanyOutlet).\
                              filter(CompanyOutlet.outlet_guid == outlet_guid_json).first()
        session.close()
        return result

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQL AlchemyError")

def get_threshold_mintransac(outlet_guid_json):
    session = create_scoped_session()

    default_json_opt = { 
        "threshold_alert": {
            "CPU": 90,
            "RAM": 90,
            "PARTITION": 90,
            "MIN_BACKUP_SIZE_KB": 0.8,
            "MIN_HISTORICAL_DATA_YEARS": 10
            }
    }

    try:
        # STEP 1: GET concept GUID
        result = session.query(CompanyOutlet).\
            filter(CompanyOutlet.outlet_guid == outlet_guid_json).one()
        concept_guid = result.concept_guid

        # STEP 2: GET threshold parameters based on CONCEPT GUID
        concept_result = session.query(CompanyConcept).\
            filter(CompanyConcept.concept_guid == concept_guid).one()
        threshold_params = concept_result.concept_parameter 
        
        session.close()
        if threshold_params == None or \
            threshold_params == "Null" or \
            threshold_params == "":
            return default_json_opt
        else:
            return threshold_params

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        # raise HTTPException(status_code=422 , detail= "SQL AlchemyError")
        return default_json_opt

# import sys
# import os
# sys.path.append('../')
# print(sys.path)


