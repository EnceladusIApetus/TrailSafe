import jsonfile, threading

#global lock
#lock = threading.Lock()

def get_all_config():
	#global lock
	#lock.acquire()
	reader = jsonfile.JSONFile()
	reader.open_file('/home/pi/TrailSafe/Device/config/config.ini')
	#lock.release()
	return reader.read()

def get_config(config):
	return get_all_config()[config]

def get_id():
	return get_config('id')

def get_full_id():
	return get_config('full-id')

def get_type():
	return get_config('device-type')

def set_config(config_name, value):
	#global lock
	#lock.acquire()
	config_value = get_all_config()
	config_value[config_name] = value
	writer = jsonfile.JSONFile()
	writer.open_file('/home/pi/TrailSafe/Device/config/config.ini')
	writer.write(config_value)
	#lock.release()
