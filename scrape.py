from utils.storage import StorageType
from request import Request

def scrape():
	api_name = 'hotTechCompanies'
	request = Request(api_name)
	json_response = request.call_api()
	strg = StorageType().choose('file')
	strg.save(json_response, api_name)

if __name__ == '__main__':
	scrape()
