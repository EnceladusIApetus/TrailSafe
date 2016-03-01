from lib import network
import socket
import os
import sys


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
    	head = c.recv(1024)

    	print 'log: progress ' + head
    
    	if head == 'send file':
            network.receiveFile(c, '/home/pi/TrailSafe/files/', 1100)

        if head == 'testInternetConnection':
            print 'test connection'
            c.send('1')

        if head == 'forward text':
            network.forward_text(c, 12345, 5)
            
    except KeyboardInterrupt:
	print 'exit program.'
	break
    except:
        print 'unexpected error: ', sys.exc_info()[0]
