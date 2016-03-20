import socket, struct, os, sys, header, json, device, httplib, urllib, time

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
    print json.dumps(send_message_to_server(device.get_config('port'), device.get_config('client-timeout'), header.update_status()))

def register_device():
    print json.dumps(send_message_to_server(device.get_config('port'), device.get_config('client-timeout'), header.register_device()))

def send_event(event_type, detail):
    print json.dumps(send_message_to_server(device.get_config('port'), device.get_config('client-timeout'), header.send_event(event_type, detail)))

def check_emergency_response():
    print json.dumps(send_message_to_server(device.get_config('port'), device.get_config('client-timeout'), header.check_emergency_response()))

def auto_update_status():
    while(1):
        try:
            update_status()
            time.sleep(device.get_config('update-status-interval'))
        except:
            print sys.exc_info()
            report = {}
            report['detail'] = 'an error has occured while updating self status'
            report['sys-info'] = str(sys.exc_info())
            send_event(1, json.dumps(report))
