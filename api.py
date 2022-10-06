from datetime import date
import json
import requests
import os

class Api:
	dirname = os.path.dirname(__file__)
	params_keys = ['api_name', 'url', 'payload', 'headers', 'last_access']
	
	def __init__(self, api_name) -> None:
		self.name = api_name
		self.request_path = os.path.join(self.dirname, 'request_parameters', self.name, self.name + '_request.json')
		self.cookies_path = os.path.join(self.dirname, 'request_parameters', self.name, self.name + '_cookies')
		json_request_params = self.set_json()
		self.set_request(json_request_params)

	def set_json(self) -> dict:
		'''Orquestra a chamada dos metodos para preparar e verificar o request'''
		json_request_params = self.load_json_params()
		self.insert_cookies(json_request_params)
		self.check_params(json_request_params)
		return json_request_params

	def load_json_params(self) -> dict:
		'''Carrega o arquivo json do request'''
		try:
			with open(self.request_path, 'r') as f:
				json_request = json.load(f)
		except FileNotFoundError:
			raise FileNotFoundError('> Arquivo de request nao encontrado')
		else:
			return json_request

	def check_params(self, json_request) -> None:
		'''Verifica a presenca dos parametros necessarios'''
		for i in self.params_keys:
			if i not in json_request.keys():
				raise Exception("> O arquivo "+ self.name +" precisa do parametro: \"" + i + "\"")
	
	def insert_cookies(self, json_request) -> None:
		'''Insere os cookies'''
		json_request['headers']['cookie'] = self.get_cookies()

	def get_cookies(self) -> dict:
		'''Carrega os cookies'''
		try:
			cookies = open(self.cookies_path).readline()
		except FileNotFoundError:
			raise FileNotFoundError('> Arquivo de cookies nao encontrado')
		else:
			return cookies

	def set_request(self, json_request_params) -> None:
		'''Converte json parameters para class variables'''
		self.headers = json_request_params['headers']
		self.cookies = json_request_params['headers']['cookie']
		self.url = json_request_params['url']
		self.payload = json_request_params['payload']
		self.api_name = json_request_params['api_name']
		self.last_access = json_request_params['last_access']

	def call_api(self) -> dict:
		'''Faz a chamada a API'''
		'''Chama a validacao da resposta'''
		'''Chama atualizacao do ultimo acesso'''
		'''Retorna a resposta'''
		print("> Acessando API")
		print(self)
		try:
			response = requests.post(self.url, json = self.payload, headers = self.headers)
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			raise ConnectionError("> Erro de conexao!")
		self.validate_response(response)
		print("> Resposta Valida")
		json_response = response.json()
		self.update_last_access()
		return json_response

	def update_last_access(self) -> None:
		'''Atualiza ultimo acesso'''
		request = self.load_json_params()
		today = date.today()
		request['last_access'] = today.strftime("%d%m%Y")
		json_obj = json.dumps(request, indent=4)
		with open(self.request_path, 'w') as f:
			f.write(json_obj)
	
	def validate_response(self, response) -> dict:
		'''Valida a resposta'''
		print("> Validando Json...")
		try:
			res = response.json()
			print('> Resposta: ' + response.text[:30] + '(...)')
		except ValueError:
			raise Exception("> Resposta Invalida!")
		else:
			return res
	
	def __str__(self) -> str:
		'''Imprime informacoes do Request'''
		to_str ='\nName: ' + str(self.api_name) + '\n'
		if (self.last_access != None):
			to_str +='Last_access: ' + str(self.last_access) + '\n'
		to_str +='\n*Request Parameters*\n'
		to_str += 'Header: ' + str(self.headers)[0:40] + '(...)\n'
		to_str +='Cookies: ' + str(self.cookies)[0:40]+ '(...)\n'
		to_str +='Url: ' + str(self.url)[0:40]+ '(...)\n'
		to_str +='Payload: ' + str(self.payload)[0:40]+ '(...)\n'
		return to_str