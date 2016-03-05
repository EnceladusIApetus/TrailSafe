import jsonfile, device

def open_file():
	reader = jsonfile.JSONFile()
	reader.open_file(device.get_config('code-description-location'))
	return jsonfile.read()

def get_description(code):
	description = open_file()
	if description[code] is None:
		return None
	else:
		return description[code]