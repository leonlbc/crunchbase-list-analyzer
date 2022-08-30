from __future__ import annotations
from abc import ABC, abstractmethod
import json, os

dirname = os.path.dirname(os.path.dirname(__file__))

def ChooseStorage(filename, json_file, strg = 'file'):

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
    def save(self):
        pass


class LocalStorage(StorageType):

    #json_file, api_name(filename)
    def save(self):
        print('Salvando...')
        filename = LocalStorage.format_filename(filename)
        file = os.path.join(dirname, 'saved', filename)
        with open(file, 'w') as outfile:
            json.dump(json_response, outfile)
        return
    
    #Formata nome do arquivo para ficar no formato (...)ddmmyy.json
    @staticmethod
    def format_filename(filename):
        time_format = today.strftime("%d%m%Y")
        return filename + time_format + ".json"


class DbStorage(StorageType):

    def save(self):
        #TODO: Implement save
        return


class SaveResponse(ABC):

    @abstractmethod
    def save(self):
        pass


class SaveFile(SaveResponse):

    def __init__(self, json_response, filename):
        return

    def save(self):
        print('Salvando...')
        filename = format_filename(filename)
        file = os.path.join(dirname, 'saved', filename)
        with open(file, 'w') as outfile:
            json.dump(json_response, outfile)


class SaveDB(SaveResponse):

    def __init__(self, json_response, filename):
        self.json_response = json_response
        self.filename = filename
        return

    def save(self):
        print('Salvando...')
        return
    
    def connect_db(self):
        pass

