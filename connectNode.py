from wifi import Cell, Scheme
import socket
from lib import jsonfile, network

global port
port = None

def testInternetConnection():
    s = createConnection()
        
    if s is not None:
        s.send('testInternetConnection')
        if s.recv(1024) == '1':
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
    jsonfile.open_file('/home/pi/TrailSafe/config/config.ini')
    info = jsonfile.read()
    deviceSSID = info['device-SSID']
    passkey = info['passkey']
    interface = info['client-interface']
    targetSSIDPrefix = info['target-SSIDPrefix']
    port = info['port']
    cellList = Cell.all(interface)
    targetSSID = []
    internetSSID = []

    for cell in cellList:
        if targetSSIDPrefix in cell.ssid:
            targetSSID.append(cell)

    print 'target amount %d' % len(targetSSID)
    for x in range (0, len(targetSSID)):
        print targetSSID[x].ssid
        scheme = Scheme.find(interface, targetSSID[x].ssid)
        if scheme is None:
            print 'create scheme'
            scheme = createScheme(interface, targetSSID[x], targetSSID[x].ssid, passkey)
        scheme.activate()                     
        if testInternetConnection() == True:
            internetSSID.append(targetSSID[x])

    print internetSSID

    highSignal = internetSSID[0]
    print 'find maximum high signal'
    for ssid in internetSSID:
        if ssid.signal > highSignal.signal:
            highSignal = ssid
    print 'connect'
    scheme = Scheme.find(interface, highSignal.ssid)
    scheme.activate()

    jsonfile.update({'node-defaultGateway': network.getDefaultGateway(interface)})

