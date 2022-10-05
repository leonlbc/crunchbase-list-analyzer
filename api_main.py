from utils.storage import StorageType
from controller.request_controller import RequestController

def api_main():
	request = RequestController()
	if request.already_saved_today() == False:
		json_response = request.call_api()
		strg = StorageType().choose('file')
		strg.save(json_response, request.api_name)
	else: print("> A API " + request.api_name + " ja foi acessada hoje")

if __name__ == '__main__':
	api_main()
