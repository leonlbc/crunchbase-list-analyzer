from __future__ import annotations
from abc import ABC, abstractmethod
import json, os
#from sqlalchemy import create_engine, sessionmaker
from datetime import date
from dotenv import load_dotenv

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

    #json_file, api_name(filename)
    def save(self, json_response, filename):
        print('Salvando...')
        filename = self.format_filename(filename)
        file = os.path.join(dirname, 'CbaseListScrape', 'saved', filename)
        with open(file, 'w') as outfile:
            json.dump(json_response, outfile)
        return
    
    #Formata nome do arquivo para ficar no formato (...)ddmmyy.json
    def format_filename(self, filename):
        today = date.today()
        time_format = today.strftime("%d%m%Y")
        return filename + time_format + ".json"


class DbStorage():

    def set_db(self):
        #engine = create_engine("mysql+pymysql://"+ USER +":" + PASSW +"@" + IP + "/" + DBNAME + "?charset=utf8mb4")
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        conn = engine.connect()
        #Session = sessionmaker(bind=engine)
        #session = Session()

    def save(self, companies):
        
        return

