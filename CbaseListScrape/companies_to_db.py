import json_to_companies
from datetime import date
from dotenv import load_dotenv
from storage import StorageType

def storeCompanies():
    load_dotenv()
    companies = json_to_companies.companies_array('01092022')
    
    dbStorage = StorageType().choose(strg='db')
    dbStorage.save(companies)
    #Para salvar na db
    #1) pesquisa se ja nao existe empresa com o uuid na db

    #2) se ja tiver, atualiza ranking da empresa

    #3) verifica se outros dados mudaram, e da update neles 

storeCompanies()