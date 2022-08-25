import request_api as api
import utils.file_utils as f_utils
import request_settings
import os

def api_main(requests = ['crunchBaseList_request.json']):
	#Confere se ja acessou hj -> Faz a chamada da API -> Salva a resposta

	for json_file in requests:
		_headers, url, payload, api_name, last_access = request_settings.load(json_file)
		print('> Acessando a API: ' + api_name + '...')
		if f_utils.already_saved_today(last_access) == False:
			try:
				json_response = api.request_api(url, payload, _headers)
			except ConnectionError():
				print('> Nao conseguiu acessar a API: '+ api_name + '!')
			else:
				f_utils.save_response(json_response, api_name)
		else:
			print("> A API " + api_name + " ja foi acessada hoje")

if __name__ == '__main__':
	api_main()