import network, header, device, socket, json, time, sys, threading, gpio, buffers
import transfer_buffer

def register_device(c, head):
    try:
        if isinstance(head['path'], unicode) is not True:
            head['path'].append(device.get_full_id())
            head['path'] = json.dumps(head['path'])
        response_raw = network.HTTPConnection('POST', '/device/register', head)
        if c is not None:
            if response_raw is None:
                c.send(header.send_code('41'))
                buffers.queue(head)
            else:
                send_back(c, response_raw)
    except:
        if c is not None:
            c.send(header.send_code('41'))
            buffers.queue(head)
        """print sys.exc_info()
        report = {}
        report['detail'] = 'cannot register device'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def update_status(c, head):
    try:
        head['path'].append(device.get_full_id())
        response_raw = network.HTTPConnection('POST', '/device/updatestatus', head)
        if c is not None:
            if response_raw is None:
                c.send(header.send_code('11'))
                buffers.queue(head)
            else:
                send_back(c, response_raw)
    except:
        if c is not None:
            c.send(header.send_code('11'))
            buffers.queue(head)
        """print sys.exc_info()
        report = {}
        report['detail'] = 'cannot update requestors\' status'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def update_self_status():
    try:
        head = json.loads(header.send_code('80'))
        head['message'] = header.update_status()
        response_raw = network.HTTPConnection('POST', '/device/updatestatus', head)
        response = json.loads(response_raw.read())
        print 'response: ' + response['process-description']
        if int(response['process-code']) == 11:
            gpio.on(gpio.get_pin('led-server-connection'))
            print 'node is still connect to server'
            transfer_buffer.transfer_buffer()
        else:
            gpio.off(gpio.get_pin('led-server-connection'))
    except:
        gpio.off(gpio.get_pin('led-server-connection'))
        """print sys.exc_info()
        print 'error in update_self_status'
        report = {}
        report['detail'] = 'cannot update self status'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def send_self_event(event_type, detail):
    head = json.loads(header.send_code('90'))
    head['message'] = header.send_event(event_type, detail)
    response_raw = network.HTTPConnection('POST', '/device/event', head)
    print response_raw.read()

def send_event(c, head):
    try:
        response_raw = network.HTTPConnection('POST', '/device/event', head)
        if c is not None:
            if response_raw is None:
                c.send(header.send_code('11'))
                buffers.queue(head)
            else:
                send_back(c, response_raw)
            if (json.loads(head['message'])['event-type']) == 1:
                gpio.on(gpio.get_pin('led-emergency'))
                emergency_request = int(device.get_config('emergency')) + 1
                device.set_config('emergency', emergency_request)
    except:
        if c is not None:
            c.send(header.send_code('11'))
            buffers.queue(head)
        print sys.exc_info()

def check_emergency_response(c, head):
    try:
        response_raw = network.HTTPConnection('POST', '/wristband/check_response', head)
        if c is not None:
            if response_raw is None:
                response = json.loas(header.send_code('11'))
                response['emergency-status'] = 95
                c.send(json.dumps(response))
            else:
                send_back(c, response_raw)
                if int(json.loads(resonse_raw.read())['process-code']) == 93:
                    emergency_request = int(device.get_config('emergency')) - 1
                    device.set_config('emergency', emergency_request)
                    if emergency_request == 0:
                        gpio.off('led-emergency')
    except:
        if c is not None:
            response = json.loas(header.send_code('11'))
            response['emergency-status'] = 95
            c.send(json.dumps(response))
        """print sys.exc_info()
        report = {}
        report['detail'] = 'an error has occured while checking an emergency response'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def send_back(c, response_raw):
    try:
        response = response_raw.read()
        print response
        if response_raw is  None or int(response_raw.status) != 200:
                response = header.send_code('12')
        c.send(response)
        c.close()
    except:
        if c is not None:
            response = header.send_code('12')
        """print sys.exc_info()
        report = {}
        report['detail'] = 'cannot send back response to requestor'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def test_server_connection(c, head):
    try:
        response_raw = network.HTTPConnection('POST', '/test/serverconnection', head)
        if c is not None:
            if response_raw is None:
                c.send(header.send_code('10'))
                buffers.queue(head)
            else:
                print response_raw
                send_back(c, response_raw)
    except:
        if c is not None:
            c.send(header.send_code('10'))
        """print sys.exc_info()
        report = {}
        report['detail'] = 'cannot test connection between server and node layer'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def init_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((device.get_config('self-defaultgateway'), device.get_config('port')))
        s.listen(device.get_config('forwarder-timeout'))
        return s
    except:
        """print sys.exc_info()
        report = {}
        report['detail'] = 'cannot initial socket'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def auto_update_self_status():
    try:
        update_self_status()
        threading.Timer(device.get_config('update-status-interval'), auto_update_self_status).start()
    except:
        print sys.exc_info()
        print 'error in auto_update_self_status'
        """report = {}
        report['detail'] = 'an error has occured while updating self status'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""
        threading.Timer(device.get_config('update-status-interval'), auto_update_self_status).start()

def check_risk_status(c, head):
    try:
        head['path'].append(device.get_full_id())
        response_raw = network.HTTPConnection('POST', '/wristband/check_risk_status', head)
        if c is not None:
            if response_raw is None:
                response = json.loads(header.send_code('11'))
                response['risk-status'] = 112
                c.send(json.dumps(response))
            else:
                send_back(c, response_raw)
    except:
        if c is not None:
            response = json.loads(header.send_code('11'))
            response['risk-status'] = 112
            c.send(json.dumps(response))
        """print sys.exc_info()
        report = {}
        report['detail'] = 'cannot check risk status for wristband which requested or send back response'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def send_self_gps_coordinate(c, head):
    try:
        message = {}
        head['device-id'] = device.get_id()
        message['message'] = json.dumps(head)
        response_raw = network.HTTPConnection('POST', '/node/updategps', message)
        if c is not None:
            if response_raw is None:
                print 'error'
                c.send(header.send_code('11'))
            else:
                print 'complete'
                send_back(c, response_raw)
    except:
        if c is not None:
            print 'exception'
            c.send(header.send_code('11'))
            print sys.exc_info()
        """report = {}
        report['detail'] = 'an error has occured while checking an emergency response'
        report['sys-info'] = str(sys.exc_info())
        send_self_event(0, json.dumps(report))"""

def update_gps_coordinate(c, head):
    try:
        head['path'].append(device.get_full_id())
        response_raw = network.HTTPConnection('POST', '/device/updatestatus', head)
        if c is not None:
            if response_raw is None:
                c.send(header.send_code('11'))
                buffers.queue(head)
            else:
                send_back(c, response_raw)
    except:
        if c is not None:
            c.send(header.send_code('11'))
            buffers.queue(head)
