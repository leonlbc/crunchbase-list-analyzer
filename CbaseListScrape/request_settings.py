import json
import os

dirname = os.path.dirname(__file__)

def load(params_filename):
	request = load_request_params(params_filename)
	return set_params(request)

#Carrega os parametros do request do arquivo request_params.json
def load_request_params(params_filename):
	request_path = os.path.join(dirname, params_filename)

	with open(request_path, 'r') as f:
	    request = json.load(f)
	req = ['api_name', 'url', 'payload', 'headers', 'ultimo_acesso']

	for i in req:
		if i not in req:
			raise Exception("> O arquivo "+ params_filename +" precisa do parametro: \"" + i + "\"")
	return request

#Seta os parametros
def set_params(request):
	_headers = request['headers']
	cookies_path = os.path.join(dirname, 'cookies')
	try:
		cookies = open(cookies_path).readline()
	except FileNotFoundError:
		print("> Arquivo de cookies nao encontrado") 
	else:
		_headers['cookies'] = cookies;

	url = request['url']
	payload = request['payload']
	api_name = request['api_name']
	last_access = request['ultimo_acesso']
	return _headers, url, payload, api_name, last_access
