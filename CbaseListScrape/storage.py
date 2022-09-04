from __future__ import annotations
from abc import ABC, abstractmethod
import json, os
from sqlalchemy import create_engine
from datetime import date

dirname = os.path.dirname(os.path.dirname(__file__))

def ChooseStorage(strg = 'file'):

    strg_types = [ResponseLocalStorage(), ResponseDBStorage()]
    if strg == 'file':
        strg = strg_types[0]
    elif strg == 'db':
        strg = strg_types[1]
    return strg


class ResponseStorage(ABC):

    @abstractmethod
    def useStorage(self):
        pass

    def storage_type(self):
        storage = self.useStorage()
        return storage


class ResponseLocalStorage(ResponseStorage):

    def useStorage(self):
        return LocalStorage()


class ResponseDBStorage(ResponseStorage):

    def useStorage(self):
        return DbStorage()


class StorageType(ABC):

    @abstractmethod
    def save(self, json_response, filename):
        pass


class LocalStorage(StorageType):

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


class DbStorage(StorageType):

    def set_db(self):
        engine = create_engine("mysql+pymysql://"+ USER +":" + PASSW +"@" + IP + "/" + DBNAME + "?charset=utf8mb4")
        conn = engine.connect()

    def save(self, json_response, filename):
        #TODO: Implement save
        return

