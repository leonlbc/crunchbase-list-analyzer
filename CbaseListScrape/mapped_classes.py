from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    uuid = Column(String, primary_key=True)
    name = Column(String)
    year_founded = Column(String)
    founders = relationship("Founder", back_populates="companies")
    categories = relationship("Category", back_populates="companies")
    rank = relationship("Rank", back_populates="companies")
    short_description = Column(String)
    num_employees = Column(int)
    last_funding_type = Column(String)
    last_funding_at = Column(String)
    acquirer = Column(String)
    announce_date = Column(String)
    funding_stage = Column(String)
    continent = Column(String)
    country = Column(String)
    region = Column(String)
    city = Column(String)

    def __repr__(self):
        return f"<Company(id={self.uuid!r}, name={self.name!r})>"

class Rank(Base):
    __tablename__ = 'ranks'
    crunchbase_rank = Column(int)
    date_req = Column(String)

    def __repr__(self):
        return f"<Rank(id={self.id!r}, rank={self.crunchbase_rank!r})>"
