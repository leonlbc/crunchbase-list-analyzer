import utils.file_utils as f_utils
from request import Request
import os

def api_main(requests = ['crunchBaseList']):

	for json_file in requests:
		req = Request(json_file)
		if f_utils.already_saved_today(req.last_access) == False:
			print('> Acessando a API: ' + req.api_name + '...')
			try:
				json_response = req.call_api()
			except ConnectionError:
				print('> Nao conseguiu acessar a API: '+ req.api_name + '!')
			else:
				f_utils.save_response(json_response, req.api_name)
		else:
			print("> A API " + req.api_name + " ja foi acessada hoje")

if __name__ == '__main__':
	api_main()