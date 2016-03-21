from wifi import Cell, Scheme
from lib import device, network

def create_scheme(interface, cell, ssidName, passkey):
    scheme = Scheme.for_cell(interface, ssidName, cell, passkey)
    scheme.save()
    return scheme

def get_highest_signal_ssid(ssid_list):
    chosen_ssid = ssid_list[0]
    for ssid in ssid_list:
        if ssid.signal > chosen_ssid.signal:
            chosen_ssid = ssid
    return chosen_ssid

def get_ssid_by_name(ssid_name, cell_list):
    device_info = device.get_all_config()
    target_ssid = []
    for cell in cell_list:
        if ssid_name in cell.ssid:
            if device_info['device-type'] == 'EN' and cell.ssid == device_info['device-SSID']:
                break
            target_ssid.append(cell)
    return target_ssid

def get_server_connected_ssid(ssid_list):
    device_info = device.get_all_config()
    
    if ssid_list is None:
        return None
    
    interface = device_info['client-interface']
    passkey = device_info['passkey']
    server_connected_ssid = []
    for x in range (0, len(ssid_list)):
        connect_wifi(ssid_list[x])
        if network.test_server_connection() == True:
            server_connected_ssid.append(ssid_list[x])
    return server_connected_ssid

def connect_wifi(ssid):
    device_info = device.get_all_config()
                            
    interface = device_info['client-interface']
    passkey = device_info['passkey']
    scheme = Scheme.find(interface, ssid.ssid)
    if scheme is None:
            scheme = create_scheme(interface, ssid, ssid.ssid, passkey)
    scheme.activate()
