import os.path
import json
from datetime import date

dirname = os.path.dirname(os.path.dirname(__file__))
today = date.today()

def already_saved_today(last_access):
	if (last_access != today.strftime("%d%m%Y")):
		return False
	return True

def save(json_response, filename):
	print('Salvando...')
	filename = format_filename(filename)
	file = os.path.join(dirname, 'saved', filename)
	with open(file, 'w') as outfile:
		json.dump(json_response, outfile)
	print('Salvo com sucesso.')

def format_filename(filename):
	time_format = today.strftime("%d%m%Y")
	return filename + time_format + ".json"
