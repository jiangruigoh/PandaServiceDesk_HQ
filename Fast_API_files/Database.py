"""
Version No: 1
Release Date: 16 July 2021 
KKSC
"""

import yaml # YAML config file
from sqlalchemy.orm import sessionmaker, relationship, selectinload
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.pool import NullPool


def create_engine():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        #print(cfg)

    # SQL Configuration Variables
    sql_username = cfg["mysql"]["user"]
    sql_pwd = cfg["mysql"]["passwd"]
    hostname = cfg["mysql"]["host"]
    database_name = cfg["mysql"]["db"]
    database_port = cfg["mysql"]["port"]

    # Closing File
    ymlfile.close()

    # mysqldb | pymysql | aiomysql
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://' + sql_username + ':' + sql_pwd + '@' + hostname + ":" + str(database_port) + '/' + database_name

    engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL, echo=False, poolclass=NullPool)
    # engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
    engine.dispose()
    #print(engine)
    return engine

def create_engine_dynamic(database_name):
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        #print(cfg)

    # SQL Configuration Variables
    sql_username = cfg["mysql"]["user"]
    sql_pwd = cfg["mysql"]["passwd"]
    hostname = cfg["mysql"]["host"]
    database_port = cfg["mysql"]["port"]

    # Closing File
    ymlfile.close()

    # mysqldb | pymysql | aiomysql
    try:
        SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://' + sql_username + ':' + sql_pwd + '@' + hostname + ":" + str(database_port) + '/' + database_name

        engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL, echo=False, poolclass=NullPool)
        # engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
        #print(engine)
        engine.dispose()
        return engine
    except exc.SQLAlchemyError as e:
        # print(e)
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))

def create_scoped_session_dynamic(database_name):
    try:
        session_factory = sessionmaker(bind=create_engine_dynamic(database_name))
        session = scoped_session(session_factory)
        
        # now all calls to Session() will create a thread-local session
        # some_session = Session()

        # you can now use some_session to run multiple queries, etc.
        # remember to close it when you're finished!
        return session
    except exc.SQLAlchemyError as e:
        # print(e)
        raise HTTPException(status_code=422 , detail= "SQLAlchemyError-" + str(e))

def engine_master():
    return create_engine()

def session_master():
    """Creates a Session for SQL Alchemy Operations"""
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=create_engine())
    session = Session()
    return session

def create_scoped_session():
    session_factory = sessionmaker(bind=create_engine())
    session = scoped_session(session_factory)
    
    # now all calls to Session() will create a thread-local session
    # some_session = Session()

    # you can now use some_session to run multiple queries, etc.
    # remember to close it when you're finished!
    # session.remove()
    return session


# Dependency
async def get_db():
    session = create_scoped_session()
    try:
        yield session
    finally:
        session.close()

#session = create_scoped_session()
#print(session)

