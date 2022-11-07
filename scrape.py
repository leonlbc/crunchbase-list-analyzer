from utils.storage import StorageType
from request import Request

def scrape():
	api_name = 'hotTechCompanies'
	request = Request(api_name)
	acessar = input("Fazer chamada? (s/n): ")
	if acessar.lower().strip() != "s":
		print("Chamada de API cancelada")
		return

	try_again = "s"
	while(try_again.lower().strip() == "s"):
		try:
			json_response = request.call_api()
			try_again = "n"
		except ValueError:
			try_again = input("Tentar novamente? (s/n): ")
			if try_again.lower().strip() == "s":
				request.insert_cookies()

	strg = StorageType().choose('file')
	strg.save(json_response, api_name)

if __name__ == '__main__':
	scrape()
