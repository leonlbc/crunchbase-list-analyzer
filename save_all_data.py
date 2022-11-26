import os
from datetime import date
import sqlalchemy
import database.utils.hotTechCompanies.schema_create as schema_create
import database.utils.hotTechCompanies.store_companies as store_companies

parent_dirname = os.path.dirname(os.path.dirname(__file__))
today = date.today()

class DbStorage():

    @staticmethod
    def set_db():
        if sqlalchemy.inspect(schema_create.engine).has_table("COMPANIES") == False:
            print("> Rodando o script de criacao da base de dados")
            schema_create.set_db()

    @staticmethod
    def save(api_name):
        DbStorage().set_db()
        store_companies.store_by_filenames(api_name, schema_create.engine)
        print("> Os dados foram salvados")

if __name__ == '__main__':
    DbStorage().save('hotTechCompanies')