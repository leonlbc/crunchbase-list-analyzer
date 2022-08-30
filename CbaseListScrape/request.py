import json
import os
import requests
from datetime import date


class Request:

	dirname = os.path.dirname(__file__)

	def __init__(self, params_filename):
		self.params_filename = params_filename
		self._headers, self.url, self.payload, self.api_name, self.last_access = self.__load()
		self.print_infos()

	def print_infos(self):
		print('')
		print('*Request Params* ')
		print('Header: ' + str(self._headers)[0:30] + '(...)')
		print('Cookies: ' + str(self._headers['cookies'])[0:30]+ '(...)')
		print('Url: ' + str(self.url))
		print('Payload: ' + str(self.payload)[0:30]+ '(...)')
		print('Name: ' + str(self.api_name))
		print('Last_access: ' + str(self.last_access))
		print('')

	def __load(self):
		request = self.__load_request_params()
		return self.set_params(request)

	#Carrega os parametros pelo arquivo json
	def __load_request_params(self):
		request_path = os.path.join(self.dirname, self.params_filename + '_request.json')

		#TODO: Erro se o arquivo n for encontrado
		with open(request_path, 'r') as f:
			request = json.load(f)
		
		req = ['api_name', 'url', 'payload', 'headers', 'last_access']
		for i in req:
			if i not in req:
				raise Exception("> O arquivo "+ self.params_filename +" precisa do parametro: \"" + i + "\"")
		return request

	#Seta os parametros
	def set_params(self, request):
		_headers = request['headers']
		cookies_path = os.path.join(self.dirname, self.params_filename + '_cookies')
		try:
			cookies = open(cookies_path).readline()
		except FileNotFoundError:
			raise FileNotFoundError('> Arquivo de cookies nao encontrado')
		else:
			_headers['cookies'] = cookies
		url = request['url']
		payload = request['payload']
		api_name = request['api_name']
		last_access = request['last_access']
		return _headers, url, payload, api_name, last_access

	def call_api(self):
		response = requests.post(self.url, json = self.payload, headers = self._headers)
		if self.validate_json(response):
			json_response = response.json()
			self.update_last_access()
			return json_response
		print("> Erro ao acessar API")
		return None

	def validate_json(self, response):
		try:
			response.json()
			print('> Resposta: ' + response.text[:30] + '(...)')
		except ValueError:
			print("> Resposta Invalida!")
			return False

		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print("> Erro de conexao!")
			return False
		return True

	def update_last_access(self):
		request_path = os.path.join(self.dirname, self.params_filename + '_request.json')

		#TODO: Erro se o arquivo n for encontrado
		with open(request_path, 'r') as f:
			request = json.load(f)

		today = date.today()
		request['last_access'] = today.strftime("%d%m%Y")

		with open(request_path, 'w') as f:
			json.dump(request, f)
