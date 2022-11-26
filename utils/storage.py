import json, os
from datetime import date
import sqlalchemy
import database.utils.hotTechCompanies.schema_create as schema_create
import database.utils.hotTechCompanies.store_companies as store_companies

parent_dirname = os.path.dirname(os.path.dirname(__file__))
today = date.today()

class StorageType():
    
    @staticmethod
    def choose(strg):
        if strg == 'file':
            strg = LocalStorage()
        elif strg == 'db':
            strg = DbStorage()
        return strg

class LocalStorage():

    def save(self, json_response, api_name):
        print('Salvando...')
        filename = self.format_filename()
        file = os.path.join(parent_dirname, api_name, 'saved', filename)
        with open(file, 'w') as outfile:
            json.dump(json_response, outfile)
        return

    def format_filename(self):
        time_format = today.strftime("%d%m%Y")
        return time_format + ".json"

class DbStorage():

    def set_db(self):
        if sqlalchemy.inspect(schema_create.engine).has_table("COMPANIES") == False:
            print("> Rodando o script de criacao da base de dados")
            schema_create.set_db()

    def save(self, api_name, json_response):
        self.set_db()
        time_format = today.strftime("%d%m%Y")
        store_companies.map_date(time_format, json_response, schema_create.engine)

