import json
import device
import code_descriptor

def sendText(recv_id):
	x = {}
	x['process-code'] = 21
	x['process-description'] = code_descriptor.get_description('21')
	x['sender'] = device.get_full_id()
	x['receiver'] = recv_id
	x['path'] = []
	return json.dumps(x)

def forwardData(old_header):
	x = json.loads(old_header)
	x['path'].append(device.get_full_id())
	return json.dumps(x)

def sendFile(recv_id, file_name,  file_size, buffer_size):
	x = {}
	x['process-code'] = 20
	x['process-description'] = code_descriptor.get_description('20')
	x['sender'] = device.get_full_id()
	x['receiver'] = recv_id
	x['path'] = []
	x['file-name'] = file_name
	x['file-size'] = file_size
	x['buffer-size'] = buffer_size
	return json.dumps(x)

def registerDevice():
	x = {}
	x['process-code'] = 40
	x['process-description'] = code_descriptor.get_description('40')
	x['device-id'] = device.get_full_id()
	x['device-type'] = device_info.get_type()
	x['path'] = []
	return json.dumps(x)

def sendCode(code):
	x = {}
	x['process-code'] = code
	x['process-description'] = code_descriptor.get_description(code)
	return json.dumps(x)