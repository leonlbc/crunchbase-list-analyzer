import utils.file_utils as f_utils
from storage import StorageType
from request import Request
from dotenv import load_dotenv

def api_main():
	#Carrega variaveis de ambiente
	load_dotenv()

	#Constroi request, a partir do nome (mudar?)
	req = Request('crunchBaseList')

	#Verifica se ja acessou hoje
	if f_utils.already_saved_today(req.last_access) == False:
		print('> Acessando a API: ' + req.api_name + '...')
		json_response = req.call_api()
		#Verifica se recebeu a resposta, se sim, salva (file ou db)
		if json_response != None:
			strg = StorageType().choose('file')
			strg.save(json_response, req.api_name)
	else: print("> A API " + req.api_name + " ja foi acessada hoje")

if __name__ == '__main__':
	api_main()
