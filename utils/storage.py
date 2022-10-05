from __future__ import annotations
import json, os
from datetime import date

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

    def save(self, json_response, filename):
        print('Salvando...')
        filename = self.format_filename(filename)
        file = os.path.join(dirname, 'saved', filename)
        with open(file, 'w') as outfile:
            json.dump(json_response, outfile)
        return
    
    def format_filename(self, filename):
        today = date.today()
        time_format = today.strftime("%d%m%Y")
        return filename + time_format + ".json"


class DbStorage():

    def set_db(self):
        pass

    def save(self, companies):
        return

