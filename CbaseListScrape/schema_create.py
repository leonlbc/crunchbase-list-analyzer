from sqlalchemy import Column, Integer, String, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv("DB_PATH")

engine = create_engine('sqlite:///{db_path}', echo=True)
Base = declarative_base()

company_founder = Table("company_founder", Base.metadata,
    Column("company_uuid", ForeignKey("companies.uuid"), primary_key=True),
    Column("founder_id", ForeignKey("founders.id"), primary_key=True),
)
company_category = Table("company_category", Base.metadata,
    Column("company_uuid", ForeignKey("companies.uuid"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)

class Company(Base):
    __tablename__ = 'companies'

    uuid = Column(String, primary_key=True)
    name = Column(String)
    year_founded = Column(String)
    short_description = Column(String)
    num_employees = Column(Integer)
    last_funding_type = Column(String)
    last_funding_at = Column(String)
    acquirer = Column(String)
    announce_date = Column(String)
    funding_stage = Column(String)
    continent = Column(String)
    country = Column(String)
    region = Column(String)
    city = Column(String)

    founders = relationship("Founder", secondary=company_founder, back_populates="companies")
    categories = relationship("Category", secondary=company_category, back_populates="companies")
    ranks = relationship("Rank", back_populates="company")

    def __init__(self, uuid,name,year_founded,short_description,num_employees,
                last_funding_type,last_funding_at,acquirer,announce_date,funding_stage,
                continent,country,region,city):
        self.uuid = uuid
        self.name = name 
        self.year_founded = year_founded 
        self.short_description = short_description 
        self.num_employees = num_employees 
        self.last_funding_type = last_funding_type 
        self.last_funding_at = last_funding_at 
        self.acquirer = acquirer 
        self.announce_date = announce_date 
        self.funding_stage = funding_stage 
        self.continent = continent 
        self.country = country 
        self.region = region 
        self.city = city 

    def __repr__(self):
        return f"<Company(id={self.uuid!r}, name={self.name!r})>"

class Rank(Base):
    __tablename__ = 'ranks'
    id = Column(String, primary_key=True)
    crunchbase_rank = Column(Integer)
    date_req = Column(Date)
    company_id = Column(String, ForeignKey("companies.uuid"))
    company = relationship("Company", back_populates="ranks")

    def __init__(self, crunchbase_rank, date_req):
        self.id = uuid.uuid4().hex
        self.date_req = date_req
        self.crunchbase_rank = crunchbase_rank

    def __repr__(self):
        return f"<Rank(id={self.id!r}, rank={self.crunchbase_rank!r})>"

class Founder(Base):
    __tablename__ = 'founders'
    id = Column(String, primary_key=True)
    name = Column(String)
    companies = relationship("Company", secondary=company_founder ,back_populates="founders")

    def __init__(self, name):
        self.id = uuid.uuid4().hex
        self.name = name
        

class Category(Base):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    name = Column(String)
    companies = relationship("Company", secondary=company_category ,back_populates="categories")

    def __init__(self, name):
        self.id = uuid.uuid4().hex
        self.name = name

Base.metadata.create_all(engine)