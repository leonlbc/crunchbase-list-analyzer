from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)


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

    def __repr__(self):
        return f"<Company(id={self.uuid!r}, name={self.name!r})>"

class Rank(Base):
    __tablename__ = 'ranks'
    id = Column(Integer, primary_key=True)
    crunchbase_rank = Column(Integer)
    date_req = Column(String)
    company_id = Column(Integer, ForeignKey("companies.uuid"))
    company = relationship("Company", back_populates="ranks")

    def __repr__(self):
        return f"<Rank(id={self.id!r}, rank={self.crunchbase_rank!r})>"

class Founder(Base):
    __tablename__ = 'founders'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    companies = relationship("Company", secondary=company_founder ,back_populates="founders")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    companies = relationship("Company", secondary=company_category ,back_populates="categories")

Base.metadata.create_all(engine)
