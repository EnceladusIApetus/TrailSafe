import jsonfile

def get_config():
	jsonfile.open_file('home/pi/TrailSafe/congif/config.ini');
	return jsonfile.read()

def get_id():
	return get_config()['id']

def get_full_id():
	return get_config()['full-id']

def get_type():
	return get_config()['device-type']