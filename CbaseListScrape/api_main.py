import utils.file_utils as f_utils
from request import Request
import os

def api_main(requests = ['crunchBaseList']):

	for json_file in requests:
		req = Request(json_file)
		if f_utils.already_saved_today(req.last_access) == False:
			print('> Acessando a API: ' + req.api_name + '...')
			json_response = req.call_api()
			if json_response != None:
				f_utils.save_response(json_response, req.api_name)
				#Factory de Salvar
		else:
			print("> A API " + req.api_name + " ja foi acessada hoje")

if __name__ == '__main__':
	api_main()