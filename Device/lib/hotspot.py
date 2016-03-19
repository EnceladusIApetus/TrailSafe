import device, os, connectNode, network, time, thread, server

def choose_gateway():
    chosen_gateway = None
    for gateway in device.get_config('self-defaultgateway-list'):
        if gateway not in device.get_config('node-defaultgateway'):
            chosen_gateway = gateway
            break
    return chosen_gateway

def replace_setting(old_gateway, self_gateway):
    interface_file = open('/etc/network/interfaces', 'r')
    dhcpd_file = open('/etc/dhcp/dhcpd.conf', 'r')
    filedata_interface = interface_file.read()
    filedata_dhcpd = dhcpd_file.read()
    filedata_interface = filedata_interface.replace(old_gateway, self_gateway)
    filedata_dhcpd = filedata_dhcpd.replace(old_gateway[:-2], self_gateway[:-2])

    interface_file = open('/etc/network/interfaces', 'w')
    dhcpd_file = open('/etc/dhcp/dhcpd.conf', 'w')
    interface_file.write(filedata_interface)
    interface_file.close()
    dhcpd_file.write(filedata_dhcpd)
    dhcpd_file.close()

def run_hotspot():
    device.set_config('hotspot-status', 'not ready')
    os.popen('pkill -f "hostapd"')
    os.popen('pkill -f "server.py"')
    print os.popen('ifdown wlan1').read()
    while connectNode.connect_node() == False:
        print 'error: connect connect to server connected ssid'
    self_gateway = choose_gateway()
    print 'chosen gateway: ' + self_gateway
    old_gateway = device.get_config('self-defaultgateway')
    device.set_config('self-defaultgateway', self_gateway)
    replace_setting(old_gateway, self_gateway)
    print os.popen('ifup wlan1').read()
    print os.popen('ifconfig wlan1 ' + self_gateway).read()
    print os.popen('service isc-dhcp-server start').read()
    device.set_config('hotspot-status', 'ready')

def start_hotspot():
    run_hotspot()
    
    while(True):
        try:
            if network.test_server_connection() is not True:
                print 'connection is aborted'
                run_hotspot()
                        
            time.sleep(5)
        except:
            print 'an error has occured while connecting to other node'

    
