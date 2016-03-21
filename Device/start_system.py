from lib import device
import os

device_type = device.get_type()
if device_type == 'WB':
    os.popen('python /home/pi/TrailSafe/Device/wristband_startup.py')
elif device_type == 'EN':
    os.popen('python /home/pi/TrailSafe/Device/external_node_startup.py')
else:
    os.popen('python /home/pi/TrailSafe/Device/internal_node_startup.py')
