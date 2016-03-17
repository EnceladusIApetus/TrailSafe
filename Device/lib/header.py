import json
import device
import code_descriptor

def send_message(recv_id, message):
	x = {}
	x['process-code'] = 21
	x['process-description'] = code_descriptor.get_description('21')
	x['sender'] = device.get_full_id()
	x['receiver'] = recv_id
	x['path'] = []
	x['message'] = message
	return json.dumps(x)

def forward_data(old_header):
	x = json.loads(old_header)
	x['path'].append(device.get_full_id())
	return json.dumps(x)

def send_file(recv_id, file_name,  file_size, buffer_size):
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

def register_device():
	x = {}
	x['process-code'] = 40
	x['process-description'] = code_descriptor.get_description('40')
	x['device-id'] = device.get_id()
	x['device-full-id'] = device.get_full_id()
	x['device-type'] = device.get_type()
	x['registration-node-id'] = device.get_config('registration-node-id')
	return json.dumps(x)

def update_status():
        x = {}
        x['process-code'] = 80
        x['process-description'] = code_descriptor.get_description('80')
        x['device-id'] = device.get_id()
        x['device-type'] = device.get_type();
        x['device-full-id'] = device.get_full_id()
        return json.dumps(x)

def send_event(event_type, detail):
        x = {}
        x['process-code'] = 90
        x['process-description'] = code_descriptor.get_description('90')
        x['device-id'] = device.get_id()
        x['device-type'] = device.get_type();
        x['device-full-id'] = device.get_full_id()
        x['event-type'] = event_type
        x['event-detail'] = detail
        return json.dumps(x)

def check_emergency_response():
        x = {}
        x['process-code'] = 94
        x['process-description'] = code_descriptor.get_description('94')
        x['device-id'] = device.get_id()
        x['device-type'] = device.get_type();
        x['device-full-id'] = device.get_full_id()
        return json.dumps(x)

def send_code(code):
	x = {}
	x['process-code'] = code
	x['process-description'] = code_descriptor.get_description(code)
	return json.dumps(x)
