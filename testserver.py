from lib import network
import socket
import os
import sys
import json
import header


self_ip = '192.168.2.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((self_ip, 12345))
s.listen(10)
print 'start'
while True:
    try:
    	c, addr = s.accept()
	    c.settimeout(5)
    	header = json.loads(c.recv(1024))

    	print 'process: ' + head['process-description']
    
    	if header['process-code'] == 20:
            network.receiveFile(c, '/home/pi/TrailSafe/files/', 1024, header)

        if header['process-code'] == 60:
            if network.test_server_connection():
                c.send(header.sendCode('61'))
            else:
                c.send(header.sendCode('62'))

        if header['process-code'] == 21:
            network.forward_text(c, 12345, 5, header)
            
    except KeyboardInterrupt:
	print 'exit program.'
	break
    except:
        print 'unexpected error: ', sys.exc_info()[0]
