from lib import device
import os, connectNode

print os.popen('ifdown wlan1').read()
connectNode.connectNode()

node_gateway = device.get_config('node-defaultGateway')
self_gateway = None

for gateway in device.get_config('self-defaultGateway-list'):
    if gateway not in node_gateway:
        self_gateway = gateway
        break
old_gateway = device.get_config('self-defaultGateway')
print 'chose gateway: ' + self_gateway
device.set_config('self-defaultGateway', self_gateway)

interface_file = open('/etc/network/interfaces', 'r')
dhcpd_file = open('/etc/dhcp/dhcpd.conf', 'r')
filedata_interface = interface_file.read()
filedata_dhcpd = dhcpd_file.read()
filedata_interface = filedata_interface.replace(old_gateway, self_gateway)
filedata_dhcpd = filedata_dhcpd.replace(old_gateway[:-2], self_gateway[:-2])
print old_gateway
print self_gateway

interface_file = open('/etc/network/interfaces', 'w')
dhcpd_file = open('/etc/dhcp/dhcpd.conf', 'w')
interface_file.write(filedata_interface)
interface_file.close()
dhcpd_file.write(filedata_dhcpd)
dhcpd_file.close()
print os.popen('ifup wlan1').read()
print os.popen('ifconfig wlan1 ' + self_gateway).read()
print os.popen('service isc-dhcp-server start').read()
print os.popen('/usr/sbin/hostapd /etc/hostapd/hostapd.conf').read()

