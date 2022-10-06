from utils.storage import StorageType
from api import Api
import sys

def scrape():
	apis = sys.argv[1:]
	for api_name in apis:
		api = Api(api_name)
		json_response = api.call_api()
		strg = StorageType().choose('file')
		strg.save(json_response, api.name)

if __name__ == '__main__':
	scrape()
