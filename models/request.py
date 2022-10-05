import os

class Request:

	dirname = os.path.dirname(os.path.dirname(__file__))

	def __init__(self, params_filename):
		self.params_filename = params_filename
		self.request_path = os.path.join(self.dirname, 'request_parameters/' + self.params_filename + '_request.json')
		print(self.request_path)
		self.cookies_path = os.path.join(self.dirname, 'request_parameters', self.params_filename + '_cookies')

	def __str__(self):
		print('')
		print('*Request Params* ')
		print('Header: ' + str(self.headers)[0:30] + '(...)')
		print('Cookie: ' + str(self.headers['cookie'])[0:30]+ '(...)')
		print('Url: ' + str(self.url))
		print('Payload: ' + str(self.payload)[0:30]+ '(...)')
		print('Name: ' + str(self.api_name))
		print('Last_access: ' + str(self.last_access))
		print('')

	def get_cookies(self):
		try:
			cookies = open(self.cookies_path).readline()
		except FileNotFoundError:
			raise FileNotFoundError('> Arquivo de cookies nao encontrado')
		else:
			return cookies
	
	def set_request_params(self, request):
		self.headers = request['headers']
		self.headers['cookie'] = self.get_cookies()
		self.url = request['url']
		self.payload = request['payload']
		self.api_name = request['api_name']
		self.last_access = request['last_access']