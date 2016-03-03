import json, device

def sendText(recv_id):
	x = {}
	x['process'] = 21
	x['process-description'] = 'send text to server'
	x['sender'] = device.get_full_id()
	x['receiver'] = recv_id
	x['path'] = []
	return json.dumps(x)

def forwardData(old_header):
	x = json.loads(old_header)
	x['path'].append(device.get_full_id())
	return json.dumps(x)

def sendFile(recv_id, file_name, buffer_size):
	x = {}
	x['process'] = 20
	x['process-description'] = 'send file to server'
	x['sender'] = device.get_full_id()
	x['receiver'] = recv_id
	x['path'] = []
	x['file_name'] = file_name
	x['buffer_size'] = buffer_size
	return json.dumps(x)

def registerDevice():
	x = {}
	x['process'] = 40
	x['process-description'] = 'register device'
	x['device_id'] = device.get_full_id()
	x['device_type'] = device.get_type()
	x['path'] = []
	return json.dumps(x)