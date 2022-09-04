import utils.file_utils as f_utils
import storage
from request import Request
from dotenv import load_dotenv

def api_main():
	load_dotenv() #Carrega variaveis de ambiente
	req = Request('crunchBaseList') #Constroi request a partir do nome
	if f_utils.already_saved_today(req.last_access) == False:
		print('> Acessando a API: ' + req.api_name + '...')
		json_response = req.call_api()
		if json_response != None:
			strg = storage.ChooseStorage().useStorage()
			strg.save(json_response, req.api_name)
			#f_utils.save(json_response, req.api_name)
	else:
		print("> A API " + req.api_name + " ja foi acessada hoje")

if __name__ == '__main__':
	api_main()
