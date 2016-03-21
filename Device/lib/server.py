import network, header, device, socket, json, time, sys

def register_device(c, head):
    try:
        head['path'].append(device.get_full_id())
        head['path'] = json.dumps(head['path'])
        response_raw = network.HTTPConnection('POST', '/device/register', head)
        send_back(c, response_raw)
    except:
        print sys.exc_info()
        report = {}
        report['detail'] = 'cannot register device'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))

def update_status(c, head):
    try:
        head['path'].append(device.get_full_id())
        response_raw = network.HTTPConnection('POST', '/device/updatestatus', head)
        send_back(c, response_raw)
    except:
        print sys.exc_info()
        report = {}
        report['detail'] = 'cannot update requestors\' status'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))

def update_self_status():
    try:
        head = json.loads(header.send_code('80'))
        head['message'] = header.update_status()
        response_raw = network.HTTPConnection('POST', '/device/updatestatus', head)
        print response_raw.read()
    except:
        print sys.exc_info()
        report = {}
        report['detail'] = 'cannot update self status'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))

def send_self_event(event_type, detail):
    head = json.loads(header.send_code('90'))
    head['message'] = header.send_event(event_type, detail)
    response_raw = network.HTTPConnection('POST', '/device/event', head)
    print response_raw.read()

def send_event(c, head):
    try:
        response_raw = network.HTTPConnection('POST', '/device/event', head)
        send_back(c, response_raw)
    except:
        print sys.exc_info()

def check_emergency_response(c, head):
    try:
        response_raw = network.HTTPConnection('POST', '/wristband/check_response', head)
        send_back(c, response_raw)
    except:
        print sys.exc_info()
        report = {}
        report['detail'] = 'an error has occured while checking an emergency response'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))

def send_back(c, response_raw):
    try:
        response = response_raw.read()
        print response
        if response_raw is  None or int(response_raw.status) != 200:
                response = header.send_code('12')
        c.send(response)
        c.close()
        return response
    except:
        print sys.exc_info()
        report = {}
        report['detail'] = 'cannot send back response to requestor'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))

def test_server_connection(c, head):
    try:
        response_raw = network.HTTPConnection('POST', '/test/serverconnection', head)
        send_back(c, response_raw)
    except:
        print sys.exc_info()
        report = {}
        report['detail'] = 'cannot test connection between server and node layer'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))

def init_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((device.get_config('self-defaultgateway'), device.get_config('port')))
        s.listen(device.get_config('forwarder-timeout'))
        return s
    except:
        print sys.exc_info()
        report = {}
        report['detail'] = 'cannot initial socket'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))

def auto_update_self_status():
    while(1):
        try:
            update_self_status()
            time.sleep(device.get_config('update-status-interval'))
        except:
            print sys.exc_info()
            report = {}
            report['detail'] = 'an error has occured while updating self status'
            report['sys-info'] = str(sys.exc_info())
            send_self_event(0, json.dumps(report))
