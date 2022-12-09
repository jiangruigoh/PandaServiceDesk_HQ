# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, JSON, String, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class CompanyConcept(Base):
    __tablename__ = 'company_concept'

    company_guid = Column(String(32))
    concept_guid = Column(String(32), primary_key=True)
    concept_name = Column(String(60))
    concept_parameter = Column(JSON)


class CompanyMaster(Base):
    __tablename__ = 'company_master'

    company_guid = Column(String(32), primary_key=True)
    Name = Column(String(50), unique=True)
    reg_no = Column(String(10))
    address1 = Column(String(60), server_default=text("''"))
    address2 = Column(String(60), server_default=text("''"))
    address3 = Column(String(60), server_default=text("''"))
    address4 = Column(String(60), server_default=text("''"))
    postcode = Column(String(10), server_default=text("''"))
    active = Column(Integer)


class CompanyOutlet(Base):
    __tablename__ = 'company_outlet'

    company_guid = Column(ForeignKey('company_master.company_guid'), primary_key=True, nullable=False)
    concept_guid = Column(ForeignKey('company_concept.concept_guid'), index=True)
    outlet_guid = Column(String(32), primary_key=True, nullable=False, unique=True)
    code = Column(String(10))
    name = Column(String(50), server_default=text("''"))
    reg_no = Column(String(10), server_default=text("''"))
    add1 = Column(String(60), server_default=text("''"))
    add2 = Column(String(60), server_default=text("''"))
    add3 = Column(String(60), server_default=text("''"))
    add4 = Column(String(60), server_default=text("''"))
    postcode = Column(String(10), server_default=text("''"))
    active = Column(Integer)
    biz_date_start = Column(Date)
    biz_date_end = Column(Date)

    company_master = relationship('CompanyMaster')
    company_concept = relationship('CompanyConcept')


class DocStore(Base):
    __tablename__ = 'doc_store'

    doc_guid = Column(String(32), primary_key=True)
    company_guid = Column(ForeignKey('company_outlet.company_guid'), index=True)
    outlet_guid = Column(ForeignKey('company_outlet.outlet_guid'), index=True)
    doc_type = Column(String(10, 'latin1_swedish_ci'))
    document = Column(JSON)
    validated = Column(Integer)
    created_date = Column(Date)
    created_time = Column(Time)

    company_outlet = relationship('CompanyOutlet', primaryjoin='DocStore.company_guid == CompanyOutlet.company_guid')
    company_outlet1 = relationship('CompanyOutlet', primaryjoin='DocStore.outlet_guid == CompanyOutlet.outlet_guid')


class DocStoreLog(Base):
    __tablename__ = 'doc_store_log'

    log_guid = Column(String(32), primary_key=True)
    doc_store_guid = Column(String(32))
    log_type = Column(String(32))
    status = Column(Integer)
    message = Column(JSON)
    validated_issue = Column(Integer)
