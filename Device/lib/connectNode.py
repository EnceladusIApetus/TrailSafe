from wifi import Cell, Scheme
from lib import jsonfile, network, header, device, wifi_lib
import socket, json

def connect_node():
	try:        
                interface = device.get_config('client-interface')
            
                target_ssid = wifi_lib.get_ssid_by_name(device.get_config('target-SSIDPrefix'), Cell.all(interface))
                if target_ssid is None:
                    print 'error: no target ssid'
                    return False

                print 'list of target ssid'
                for x in range (0, len(target_ssid)):
                    print '   => ' + target_ssid[x].ssid
                
                internet_ssid = wifi_lib.get_server_connected_ssid(target_ssid)
                if internet_ssid is None:
                    print 'error: no server connected ssid'
                    return False
                
                print 'list of candidate ssid'
                for x in range (0, len(internet_ssid)):
                    print '   => ' + internet_ssid[x].ssid
                    
                chosen_ssid = wifi_lib.get_highest_signal_ssid(internet_ssid)
                print 'chosen ssid: ' + chosen_ssid.ssid
                wifi_lib.connect_wifi(chosen_ssid)    

                device.set_config('node-defaultgateway', network.get_defaultgateway(interface))
                node_info = network.request_device_info()
                device.set_config('registration-node-id', node_info['device-id'])
                network.register_device()
                device.set_config('server-connection', 'connected')
                return True
	except:
                return False                

