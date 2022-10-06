from utils.storage import StorageType
from request import Request
import sys

def scrape():
	apis = sys.argv[1:]
	for api_name in apis:
		request = Request(api_name)
		json_response = request.call_api()
		strg = StorageType().choose('file')
		strg.save(json_response, api_name)

if __name__ == '__main__':
	scrape()
