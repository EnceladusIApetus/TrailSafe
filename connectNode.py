from wifi import Cell, Scheme
from lib import jsonfile, network, header, device
import socket, json

global port
port = None

def test_internet_connection():
    s = create_connection()
        
    if s is not None:
        s.send(header.send_code('60'))
        response = json.loads(s.recv(1024))
        print 'log: host->' + response['process-description']
        if int(response['process-code']) == 61:
            print 'Server connection successful.'
            return True
        else:
            return False
    else:
        print 'Cannot connect to server.'
    
def create_connection():
    global port
    defaultgateway = network.getdefaultgateway('wlan0')
    print defaultgateway
    socket.setdefaulttimeout(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'start connection'
    if s.connect_ex((defaultgateway, port)) == 0:
        return s
    else:
        return None

def create_scheme(interface, cell, ssidName, passkey):
    scheme = Scheme.for_cell(interface, ssidName, cell, passkey)
    scheme.save()
    return scheme

def connect_node():
    global port
    device_ssid = device.get_config('device-SSID')
    passkey = device.get_config('passkey')
    interface = device.get_config('client-interface')
    target_ssid_prefix = device.get_config('target-SSIDPrefix')
    port = device.get_config('port')
    cell_list = Cell.all(interface)
    target_ssid = []
    internet_ssid = []

    for cell in cell_list:
        if target_ssid_prefix in cell.ssid:
            target_ssid.append(cell)

    print 'log: number of target SSID -> %d' % len(target_ssid)
    for x in range (0, len(target_ssid)):
        print target_ssid[x].ssid
        scheme = Scheme.find(interface, target_ssid[x].ssid)
        if scheme is None:
            print 'log: create scheme'
            scheme = create_scheme(interface, target_ssid[x], target_ssid[x].ssid, passkey)
        scheme.activate()
        if test_internet_connection() == True:
            internet_ssid.append(target_ssid[x])

    print internet_ssid

    high_signal_ssid = internet_ssid[0]
    print 'log: finding maximal signal SSID'
    for ssid in internet_ssid:
        if ssid.signal > high_signal_ssid.signal:
            high_signal_ssid = ssid
    print 'log: connected'
    scheme = Scheme.find(interface, high_signal_ssid.ssid)
    scheme.activate()

    device.set_config('node-defaultgateway', network.getdefaultgateway(interface))

