from lib import hotspot, device
import os, connectNode, thread, server

print os.popen('ifdown wlan1').read()
while connectNode.connect_node() == False:
    print 'error: connect connect to server connected ssid'
self_gateway = hotspot.choose_gateway()
print 'chosen gateway: ' + self_gateway
old_gateway = device.get_config('self-defaultgateway')
device.set_config('self-defaultgateway', self_gateway)
hotspot.replace_setting(old_gateway, self_gateway)

print os.popen('ifup wlan1').read()
print os.popen('ifconfig wlan1 ' + self_gateway).read()
print os.popen('service isc-dhcp-server start').read()
thread.start_new_thread(server.run_server, ())
print os.popen('/usr/sbin/hostapd /etc/hostapd/hostapd.conf').read()

