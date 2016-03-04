import jsonfile

def open_file():
	jsonfile.open_file('/home/pi/TraiSafe/config/code_description.ini')
	return jsonfile.read()

def get_description(code):
	description = open_file()
	if description[code] is None:
		return None
	else
		return description[code]