import network, header, device, socket, json, time

def register_device(c, head):
    head['path'].append(device.get_full_id())
    head['path'] = json.dumps(head['path'])
    response_raw = network.HTTPConnection('POST', '/device/register', head)
    send_back(c, response_raw)

def update_status(c, head):
    head['path'].append(device.get_full_id())
    response_raw = network.HTTPConnection('POST', '/device/updatestatus', head)
    send_back(c, response_raw)

def update_self_status():
    head = json.loads(header.send_code('80'))
    head['message'] = header.update_status()
    response_raw = network.HTTPConnection('POST', '/device/updatestatus', head)
    print response_raw.read()

def send_self_event(event_type, detail):
    head = json.loads(header.send_code('90'))
    head['message'] = header.send_event(event_type, detail)
    response_raw = network.HTTPConnection('POST', '/device/event', head)
    print response_raw.read()

def send_event(c, head):
    response_raw = network.HTTPConnection('POST', '/device/event', head)
    send_back(c, response_raw)

def check_emergency_response(c, head):
    response_raw = network.HTTPConnection('POST', '/wristband/check_response', head)
    send_back(c, response_raw)

def send_back(c, response_raw):
    response = response_raw.read()
    print response
    if response_raw is  None or int(response_raw.status) != 200:
            response = header.send_code('12')
    c.send(response)
    c.close()
    return response

def test_server_connection(c, head):
    response_raw = network.HTTPConnection('POST', '/test/serverconnection', head)
    send_back(c, response_raw)

def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((device.get_config('self-defaultgateway'), device.get_config('port')))
    s.listen(device.get_config('forwarder-timeout'))
    return s

def auto_update_self_status(interval):
    while(1):
        update_self_status()
        time.sleep(interval)
