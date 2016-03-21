from lib import device
import os

device_type = device.get_type()
if device_type == 'WB':
    os.popen('python /home/pi/TrailSafe/Device/main_system/wristband_startup.py')
elif device_type == 'EN':
    os.popen('python /home/pi/TrailSafe/Device/main_system/external_node_startup.py')
else:
    os.popen('python /home/pi/TrailSafe/Device/main_system/internal_node_startup.py')
