from utils.storage import StorageType
from controller.api_controller import ApiController
import sys

def scrape():
	apis = sys.argv[1:]
	for api_name in apis:
		api = ApiController(api_name)
		json_response = api.call_api()
		strg = StorageType().choose('file')
		strg.save(json_response, api.get_name())

if __name__ == '__main__':
	scrape()
