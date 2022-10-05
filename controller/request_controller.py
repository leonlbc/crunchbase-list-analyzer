from models.request import Request
from datetime import date

today = date.today()

class RequestController:

    def __init__(self):
        self.request = Request('crunchBaseList')
        self.already_saved_today()
    
    def already_saved_today(self):
        if (self.request.last_access != today.strftime("%d%m%Y")):
            return False
        return True
    
    def call(self):
        print('> Acessando a API: ' + self.request.api_name + '...')
        self.request.call_api()
        
