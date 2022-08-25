import requests

def request_api(url, payload, _headers):
	response = requests.post(url, json = payload, headers = _headers)
	try:
		response.raise_for_status()
	except requests.exceptions.HTTPError as e:
		raise ConnectionError()
	json_response = response.json()
	return json_response
