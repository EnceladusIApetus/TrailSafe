from lib import hotspot, device, connectNode
import os, thread, time

while(True):
    connectNode.connect_node()
    os.popen('python /home/pi/TrailSafe/Device/wb_main.py')
    
