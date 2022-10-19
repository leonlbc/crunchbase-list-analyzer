import json, os
from datetime import date
from sqlalchemy import create_engine
import sqlalchemy

dirname = os.path.dirname(os.path.dirname(__file__))

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
        filename = self.format_filename(api_name)
        file = os.path.join(dirname, 'saved', api_name, filename)
        with open(file, 'w') as outfile:
            json.dump(json_response, outfile)
        return

    def format_filename(self, filename):
        today = date.today()
        time_format = today.strftime("%d%m%Y")
        return filename + time_format + ".json"


class DbStorage():

    def set_db(self):
        engine = create_engine('sqlite:///db.sqlite3', echo=True)
        if sqlalchemy.inspect(engine).has_table("COMPANIES") == False:
            print("> Rodando o script de criacao da base de dados")
            #TODO Importar arquivo de schema e rodar

    def save(self, companies):
        pass

