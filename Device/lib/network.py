import socket, struct, os, sys, header, json, device, httplib, urllib, time, gpio

def get_defaultgateway_hex(interface):
    route = "/proc/net/route"
    with open(route) as f:
        for line in f.readlines():
            try:
                iface, dest, gateway, flags, _, _, _, _, _, _, _, =  line.strip().split()
                if iface == interface:
                    return gateway
            except:
                continue

def get_defaultgateway(interface):
    ip_hex = int(get_defaultgateway_hex(interface), 16)
    return socket.inet_ntoa(struct.pack('<L', ip_hex))

def send_message_to_server(port, timeout, message):
    return send_message(get_defaultgateway('wlan0'), port, timeout, message, 'SV')

def send_message(dest_ip, port, timeout, message, recv_id):
    s = create_socket(dest_ip, port, timeout)
    try:
        if s is not None:
            s.send(header.send_message(recv_id, message))
            response = json.loads(s.recv(1024))
            print 'host: ' + response['process-description']
            s.close()
            return response
    except:
        print 'log: sending message fail'
        s.close()
    return None

def forward_message(c, port, timeout, head):
    try:
        if head['receiver'] == device.get_full_id():
            c.send(header.send_code('10'))
            print 'host: ' + head['message']
        else:
            s = create_socket(get_defaultgateway('wlan0'), port, timeout)
            try:
                if s is not None:
                    print 'log: forwarding message to node'
                    s.send(header.forward_data(json.dumps(head)))
                    response = json.loads(s.recv(1024))
                    print 'host: ' + response['process-description']
                    if response is not None:
                        print 'log: forwarding completed. send back response'
                        c.send(json.dumps(response))
                        s.close()
                    return response
                else:
                    c.send(header.send_code('27'))
            except:
                print 'log: forwarding failed'
                c.send(header.send_code('27'))
        c.close()
        return None
    except:
        print 'unexpected error: ', sys.exc_info()
        network.send_event(1, str(sys.exc_info()))
        c.close()

def create_socket(dest_ip, port, timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        if s.connect_ex((dest_ip, port)) == 0:
            return s
        else:
            return None

def decap_message(message):
        return json.loads((json.loads(message))['message'])    

def test_server_connection():
    response = send_message_to_server(12345, 10, header.send_code('60'))
    if response is not None and int(response['process-code']) == 10:
        return True
    return False

def HTTPConnection(method, url, params):
    params = urllib.urlencode(params)
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    con = httplib.HTTPConnection(device.get_config('server-ip'))
    con.request(method, url, params, headers)
    return con.getresponse()

def update_status():
    device_info = device.get_all_config()
    response = send_message_to_server(device_info['port'], device_info['client-timeout'], header.update_status())
    return response

def check_risk_status():
    device_info = device.get_all_config()
    response = send_message_to_server(device_info['port'], device_info['client-timeout'], header.check_risk_status())
    print 'response: ' + str(response['risk-status'])
    device.set_config('risk-status', response['risk-status'])

    return response

def register_device():
    device_info = device.get_all_config()
    response = send_message_to_server(device_info['port'], device_info['client-timeout'], header.register_device())
    return response

def send_event(event_type, detail):
    device_info = device.get_all_config()
    response = send_message_to_server(device_info['port'], device_info['client-timeout'], header.send_event(event_type, detail))
    return response

def send_emergency():
    send_event(1, 'user is in danger')

def check_emergency_response():
    device_info = device.get_all_config()
    response = send_message_to_server(device_info['port'], device_info['client-timeout'], header.check_emergency_response())
    return response

def auto_update_status():
    error_times = 0
    while True:
        try:
	    device_info = device.get_all_config()
            response = update_status()
            print 'update status: ' + response['process-description']
	    if device_info['device-type'] == 'WB':
		device.set_config('risk-status', 5)
		response = check_risk_status()

		if int(response['risk-status']) == 111:
		    print 'warning!!!'
		    gpio.gen_signal(gpio.get_pin('led-alert'), 5, 0.5)
	    else:
                time.sleep(device_info['update-status-interval'])
        except:
            error_times += 1
            if error_times > int(device.get_config('maximum-allowed-error')) and device.get_type() == 'WB':
                os.popen('pkill -f "wb_main.py"')
                device.set_config('server-connection', 'not connect')
                error_times = 0
            print sys.exc_info()
            report = {}
            report['detail'] = 'an error has occured while updating self status'
            report['sys-info'] = str(sys.exc_info())
            send_event(0, json.dumps(report))

def reply_device_info(c):
    response = {}
    response['process-code'] = 11
    response['device-id'] = device.get_id()
    response['device-type'] = device.get_type()
    response['device-full-id'] = device.get_full_id()
    c.send(json.dumps(response))
    c.close()

def request_device_info():
    device_info = device.get_all_config()
    s = create_socket(get_defaultgateway('wlan0'), device_info['port'], device_info['client-timeout'])
    s.send(header.request_device_info())
    return json.loads(s.recv(1024))
    
