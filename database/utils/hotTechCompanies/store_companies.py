import os
from sqlalchemy.orm import sessionmaker
from utils.json_to_response import response_array, get_res
from database.utils.hotTechCompanies.schema_create import Company, Rank, Founder, Category, company_category, company_founder

#Script para converter json salvo localmente em objetos da ORM
#e salva-los na base de dados

def map_to_db(company_to_add, session):
    #Company
    mapped_comp = session.query(Company).filter_by(uuid=company_to_add.uuid).first()
    if (mapped_comp == None):
        mapped_comp = Company(
            uuid = company_to_add.uuid,
            name = company_to_add.name,
            year_founded = company_to_add.year_founded,
            short_description = company_to_add.short_description,
            num_employees = company_to_add.num_employees,
            last_funding_type = company_to_add.last_funding_type,
            last_funding_at = company_to_add.last_funding_at,
            acquirer = company_to_add.acquirer,
            announce_date = company_to_add.announce_date,
            funding_stage = company_to_add.funding_stage,
            continent = company_to_add.continent,
            country = company_to_add.country,
            region = company_to_add.region,
            city = company_to_add.city
        )

    #Rank
    exist_rank_with_date = session.query(Rank.id).filter_by(date_req = company_to_add.date_request).filter_by(company_id = company_to_add.uuid).first() is not None
    if (exist_rank_with_date == False):
        rank = Rank(crunchbase_rank = company_to_add.crunchbase_rank,
                    date_req = company_to_add.date_request)
        rank.company = mapped_comp
        mapped_comp.ranks.append(rank)

    #Founders
    def founder_exist_by_name(founder):
        return session.query(Founder).filter_by(name = founder).first()
    def founder_exist_in_company(founder):
        return session.query(company_founder).filter_by(founder_id = founder.id).filter_by(company_uuid = company_to_add.uuid).first()
    if (company_to_add.founders != None):
        for founder in company_to_add.founders:
            founder_retrieved = founder_exist_by_name(founder)
            if (founder_retrieved == None):
                founder_retrieved = Founder(
                    name = founder
                )
                mapped_comp.founders.append(founder_retrieved)
            elif (founder_exist_in_company(founder_retrieved) == False):
                mapped_comp.founders.append(founder_retrieved)

    #Categories
    def category_exist_by_name(category):
        return session.query(Category).filter_by(name = category).first()
    def category_exist_in_company(category):
        return session.query(company_category).filter_by(category_id = category.id).filter_by(company_uuid = company_to_add.uuid).first()
    if (company_to_add.categories != None):
        for category in company_to_add.categories:
            category_retrieved = category_exist_by_name(category)
            if (category_retrieved == None):
                category_retrieved = Category(
                    name = category
                )
                mapped_comp.categories.append(category_retrieved)
            elif (category_exist_in_company(category_retrieved) == False):
                mapped_comp.categories.append(category_retrieved)
    return mapped_comp

def map_date(dia, json_response, engine):
    Session = sessionmaker(bind=engine)
    companies = response_array(dia, json_response)
    for i in companies:
        with Session.begin() as session:
            session.add(map_to_db(i, session))


# Codigo usado no comeco do desenvolvimento
# para transferir todos os arquivos json da pasta saved para a base de dados

def store_by_filenames(api_name, engine):
    dates = date_list(api_name)
    for date in dates:
        response_json = get_res(date, api_name)
        map_date(date, response_json, engine)

def date_list(api_name):
    datas = []
    pasta = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + '/{0}/saved'.format(api_name)
    for diretorio, dir_names, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            datas.append(''.join(c for c in arquivo if c.isdigit()))
    return datas
