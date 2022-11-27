import os, sys
from datetime import date
import sqlalchemy
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import database.utils.hotTechCompanies.schema_create as schema_create
import database.utils.hotTechCompanies.store_companies as store_companies

today = date.today()

if __name__ == '__main__':
    if sqlalchemy.inspect(schema_create.engine).has_table("COMPANIES") == False:
            print("> Rodando o script de criacao da base de dados")
            schema_create.set_db()
    store_companies.store_by_filenames('hotTechCompanies', schema_create.engine)
    print("> Os dados foram salvados")