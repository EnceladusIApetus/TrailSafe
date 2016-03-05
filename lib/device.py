import jsonfile

def get_config():
	reader = jsonfile.JSONFile()
	reader = reader.open_file('home/pi/TrailSafe/congif/config.ini')
	return reader.read()

def get_config(config):
	return get_config()[config]

def get_id():
	return get_config()['id']

def get_full_id():
	return get_config()['full-id']

def get_type():
	return get_config()['device-type']

def set_config(config, value):
	config = get_config()
	config[config] = value
	writer = jsonfile.JSONFile()
	writer.open_file('home/pi/TrailSafe/congif/config.ini')
	writer.write(config)