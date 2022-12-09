"""
# UPDATE OPERATIONS
# SQLAlchemy
Version No: 1
Release Date: 6 July 2021 
KKSC
"""

from Fast_API_files.Database import create_scoped_session
from Fast_API_files.schema import CompanyConcept, CompanyMaster, \
    CompanyOutlet, DocStore,  DocStoreLog

# import uuid
from sqlalchemy import exc
from sqlalchemy import or_
from fastapi import HTTPException

def flag_outlet_update(flag_schem):
    session = create_scoped_session()

    try: 
        if (flag_schem.active_status > 1) or (flag_schem.active_status < 0):
            raise HTTPException(status_code=404, detail="active status can only be 1 or 0")
        check_guid_exist_cpy = session.query(CompanyOutlet).\
                              filter(CompanyOutlet.outlet_guid == flag_schem.outlet_guid).first()
        if check_guid_exist_cpy == None:
            raise HTTPException(status_code=404, detail="outlet_guid does not exist")
        else:
            session.query(CompanyOutlet).filter(
                CompanyOutlet.outlet_guid == flag_schem.outlet_guid).update(
                    {CompanyOutlet.active: flag_schem.active_status},
                    synchronize_session = False)
            session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemy Error")
    session.close()

    return {'status_code': "200", 'data': flag_schem}

def outlet_concept_update(outlet_schem):
    session = create_scoped_session()
    
    try: # Check if concept and company ids exist
        check_guid_exist_cpy = session.query(CompanyConcept).\
                              filter(CompanyConcept.company_guid == outlet_schem.company_guid).first()
        check_guid_exist_cpt = session.query(CompanyConcept).\
                              filter(CompanyConcept.concept_guid == outlet_schem.concept_guid).first()
        if (check_guid_exist_cpy == None) or (check_guid_exist_cpt == None):
            raise HTTPException(status_code=404, detail="company_guid or concept_id does not exist")
        else:
            session.query(CompanyOutlet).filter(or_(
                CompanyOutlet.company_guid == outlet_schem.company_guid,
                CompanyOutlet.outlet_guid == outlet_schem.outlet_guid)).update(
                    {CompanyOutlet.concept_guid: outlet_schem.concept_guid},
                    synchronize_session = False)
            session.commit()
    
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "Incorrect column Format")
    session.close()

    return {'status_code': "200", 'data': outlet_schem}

def update_doc_store_status(doc_uid):
    try:
        session = create_scoped_session() 
        session.query(DocStore).filter(
        DocStore.doc_guid == doc_uid).update(
            {DocStore.validated: 1},
            synchronize_session = False)

        session.commit()
        session.close()
        return {'status_code': "200", 'data': "Succesfully update doc_store Status"}
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        raise HTTPException(status_code=422 , detail= "SQLAlchemy Error")
    

    