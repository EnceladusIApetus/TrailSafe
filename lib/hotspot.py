import device

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
