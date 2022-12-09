"""
# CREATE OPERATIONS
# SQLAlchemy
Version No: 1
Release Date: 8 July 2021 
KKSC
"""

from Fast_API_files.Database import create_scoped_session
from Fast_API_files.Models import Receiver, Company_Master_M, Company_Concept_M, \
    Company_Outlet_M, Doc_Store_M, Company_Outlet_in, Company_Concept_in, \
    Flag_in, Company_Master_in, Outlet_Update, master_all, Compress_Agent, \
    Decompress_Agent, Sftp_config, Pending_Task, Company_Master_List
from Fast_API_files.schema import CompanyConcept, CompanyMaster, \
    CompanyOutlet, DocStore,  DocStoreLog

import uuid
from sqlalchemy import exc
from fastapi import HTTPException

def create_company(company_schem):
    session = create_scoped_session()
    try:    
        if (company_schem.active > 1) or (company_schem.active < 0):
            raise HTTPException(status_code=404, detail="active status can only be 1 or 0")
        else:
            # New outlet UUID
            UID = uuid.uuid1()
            main_uid = UID.hex.upper()

            item = [CompanyMaster(company_guid = main_uid,
            Name = company_schem.Name,
            reg_no = company_schem.reg_no,
            address1 = company_schem.address1,
            address2 = company_schem.address2,
            address3 = company_schem.address3,
            address4 = company_schem.address4,
            postcode = company_schem.postcode,
            active = company_schem.active
            )]
            # print(item)
            session.add_all(item)
            session.commit()

            # Response_model
            response = {}
            response["company_guid"] = main_uid
            response["Name"] = company_schem.Name
            response["reg_no"] = company_schem.reg_no
            response["address1"] = company_schem.address1
            response["address2"] = company_schem.address2
            response["address3"] = company_schem.address3
            response["address4"] = company_schem.address4
            response["postcode"] = company_schem.postcode
            response["active"] = company_schem.active

    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLALchemy Error")
    session.close()

    return {'status_code': "200", 'data': response}

def create_concept(concept_schem):
    session = create_scoped_session()
    
    try: # Check if concept  exist
        check_guid_exist_cpy = session.query(CompanyMaster).\
                              filter(CompanyMaster.company_guid == concept_schem.company_guid).first()
        if check_guid_exist_cpy == None:
            raise HTTPException(status_code=404, detail="company_guid does not exist")
        else:
            # New outlet UUID
            UID = uuid.uuid1()
            main_uid = UID.hex.upper()

            item = [CompanyConcept(company_guid = concept_schem.company_guid,
            concept_guid = main_uid,
            concept_name = concept_schem.concept_name,
            concept_parameter = concept_schem.concept_parameter
            )]
            session.add_all(item)
            session.commit()

            # Response_model
            response = {}
            response["concept_guid"] = main_uid
            response["company_guid"] = concept_schem.company_guid
            response["concept_name"] = concept_schem.concept_name
        
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "Incorrect column Format")
    session.close()

    return {'status_code': "200", 'data': response}

def create_outlet(outlet_schem):
    session = create_scoped_session()
    
    try: # Check if concept and company ids exist
        check_guid_exist_cpy = session.query(CompanyMaster).\
                              filter(CompanyMaster.company_guid == outlet_schem.company_guid).first()
        check_guid_exist_cpt = session.query(CompanyConcept).\
                              filter(CompanyConcept.concept_guid == outlet_schem.concept_guid).first()
        if (check_guid_exist_cpy == None) or (check_guid_exist_cpt == None):
            raise HTTPException(status_code=404, detail="company_guid or concept_id does not exist")
        else:
            # New outlet UUID
            UID = uuid.uuid1()
            main_uid = UID.hex.upper()

            item = [CompanyOutlet(company_guid = outlet_schem.company_guid,
            concept_guid = outlet_schem.concept_guid,
            outlet_guid = main_uid,
            code = outlet_schem.code,
            name = outlet_schem.name,
            reg_no = outlet_schem.reg_no,
            add1 = outlet_schem.add1,
            add2 = outlet_schem.add2,
            add3 = outlet_schem.add3,
            add4 = outlet_schem.add4,
            postcode = outlet_schem.postcode,
            active = outlet_schem.active,
            biz_date_start = outlet_schem.biz_date_start,
            biz_date_end = outlet_schem.biz_date_end
            )]
            session.add_all(item)
            session.commit()

            # Response_model
            response = {}
            response["company_guid"] = outlet_schem.company_guid,
            response["concept_guid"] = outlet_schem.concept_guid,
            response["outlet_guid"] = main_uid,
            response["code"] = outlet_schem.code,
            response["name"] = outlet_schem.name,
            response["reg_no"] = outlet_schem.reg_no,
            response["add1"] = outlet_schem.add1,
            response["add2"] = outlet_schem.add2,
            response["add3"] = outlet_schem.add3,
            response["add4"] = outlet_schem.add4,
            response["postcode"] = outlet_schem.postcode,
            response["active"] = outlet_schem.active,
            response["biz_date_start"] = outlet_schem.biz_date_start,
            response["biz_date_end"] = outlet_schem.biz_date_end
        
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "Incorrect column Format")
    session.close()

    return {'status_code': "200", 'data': response}

def create_doc_store(company_guid_json, outlet_guid_json, \
                        current_date_only, current_time_only, json_opt):
    session = create_scoped_session()
    try:
        UID_1 = uuid.uuid1()
        doc_uid = UID_1.hex.upper()

        item = [DocStore(doc_guid = doc_uid,
                company_guid = company_guid_json,
                outlet_guid = outlet_guid_json,
                created_date = current_date_only,
                created_time = current_time_only,
                validated = 0,
                doc_type = "ServerInfo",
                document = json_opt,
                )]
        session.add_all(item)
        session.commit()
        session.close()
        return {'status_code': "200", 'data': doc_uid}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemy Error")

def create_doc_store_log(doc_uid, validator_status, validated_issue_opt):
    session = create_scoped_session()
    try:
        UID_2 = uuid.uuid1()
        doc_log_uid = UID_2.hex.upper()
        item2 = [DocStoreLog(log_guid = doc_log_uid,
        doc_store_guid = doc_uid,
        log_type = "ServerInfo",
        status = 1,
        message = validator_status,
        validated_issue = validated_issue_opt
        )]
        session.add_all(item2)
        session.commit()
        return {'status_code': "200", 'data': "Sucessfully Created record at Doc Store Log"}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemy Error")



    