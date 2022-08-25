import os.path
import json
from datetime import date

today = date.today()
dirname = os.path.dirname(os.path.dirname(__file__))

#Formata nome do arquivo para ficar no formato (...)ddmmyy.json
def format_filename(filename):
	time_format = today.strftime("%d%m%Y")
	return filename + time_format + ".json"

def already_saved_today(last_access):
	if (last_access != today.strftime("%d%m%Y")):
		return False
	return True

def save_response(json_response, filename):
	print('Salvando...')
	filename = format_filename(filename)
	file = os.path.join(dirname, 'saved', filename)
	with open(file, 'w') as outfile:
			json.dump(json_response, outfile)
