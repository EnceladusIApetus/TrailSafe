from lib import hotspot, device
import os, thread, time

device.set_config('hotspot-status', 'not ready')
thread.start_new_thread(hotspot.prepare_hotspot, ())

while(True):
    if device.get_config('hotspot-status') == 'ready to run':
        print 'test'
        thread.start_new_thread(os.popen, ('python /home/pi/TrailSafe/Device/main_system/external_node_server.py', ))
        os.popen('hostapd /etc/hostapd/hostapd.conf')
    print 'not ready'
    time.sleep(25)
    
