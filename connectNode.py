from wifi import Cell, Scheme
from lib import jsonfile, network, header, device
import socket, json

global port
port = None

def testInternetConnection():
    s = createConnection()
        
    if s is not None:
        s.send(header.sendCode('60'))
        response = json.loads(s.recv(1024))
        print 'log: host->' + response['process-description']
        if int(response['process-code']) == 61:
            print 'Server connection successful.'
            return True
        else:
            return False
    else:
        print 'Cannot connect to server.'
    
def createConnection():
    global port
    defaultGateway = network.getDefaultGateway('wlan0')
    print defaultGateway
    socket.setdefaulttimeout(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'start connection'
    if s.connect_ex((defaultGateway, port)) == 0:
        return s
    else:
        return None

def createScheme(interface, cell, ssidName, passkey):
    scheme = Scheme.for_cell(interface, ssidName, cell, passkey)
    scheme.save()
    return scheme

def connectNode():
    global port
    deviceSSID = device.get_config('device-SSID')
    passkey = device.get_config('passkey')
    interface = device.get_config('client-interface')
    targetSSIDPrefix = device.get_config('target-SSIDPrefix')
    port = device.get_config('port')
    cellList = Cell.all(interface)
    targetSSID = []
    internetSSID = []

    for cell in cellList:
        if targetSSIDPrefix in cell.ssid:
            targetSSID.append(cell)

    print 'log: number of target SSID -> %d' % len(targetSSID)
    for x in range (0, len(targetSSID)):
        print targetSSID[x].ssid
        scheme = Scheme.find(interface, targetSSID[x].ssid)
        if scheme is None:
            print 'log: create scheme'
            scheme = createScheme(interface, targetSSID[x], targetSSID[x].ssid, passkey)
        scheme.activate()
        if testInternetConnection() == True:
            internetSSID.append(targetSSID[x])

    print internetSSID

    highSignal = internetSSID[0]
    print 'log: finding maximal signal SSID'
    for ssid in internetSSID:
        if ssid.signal > highSignal.signal:
            highSignal = ssid
    print 'log: connected'
    scheme = Scheme.find(interface, highSignal.ssid)
    scheme.activate()

    device.set_config('node-defaultGateway', network.getDefaultGateway(interface))

