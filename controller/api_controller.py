from models.request import Request
from datetime import date
import json
import requests

today = date.today()

class ApiController:

	def __init__(self, api_name):
		self.request = Request(api_name)
		self.load()
		self.already_saved_today()
	
	def load(self):
		request = self.load_request_params()
		return self.request.set_request_params(request)

	def load_request_params(self):
		json_request = self.jsonify_request()
		req = ['api_name', 'url', 'payload', 'headers', 'last_access']
		for i in req:
			if i not in json_request.keys():
				raise Exception("> O arquivo "+ self.request.params_filename +" precisa do parametro: \"" + i + "\"")
		return json_request

	def jsonify_request(self):
		try:
			with open(self.request.request_path, 'r') as f:
				json_request = json.load(f)
		except FileNotFoundError:
			raise FileNotFoundError('> Arquivo de request nao encontrado')
		else:
			return json_request

	def already_saved_today(self):
		if (self.request.last_access == today.strftime("%d%m%Y")):
			raise Exception("API ja foi acessada hoje - Cancelando")
	
	def get_name(self):
		return self.request.api_name
	
	def call_api(self):
		response = requests.post(self.request.url, json = self.request.payload, headers = self.request.headers)
		self.validate_json(response)
		json_response = response.json()
		self.update_last_access()
		return json_response

	def update_last_access(self):
		request = self.jsonify_request()
		today = date.today()
		request['last_access'] = today.strftime("%d%m%Y")
		json_obj = json.dumps(request, indent=4)
		with open(self.request.request_path, 'w') as f:
			f.write(json_obj)
	
	def validate_json(self, response):
		try:
			response.json()
			print('> Resposta: ' + response.text[:30] + '(...)')
		except ValueError:
			raise Exception("> Resposta Invalida!")
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			raise Exception("> Erro de conexao!")
	
		
