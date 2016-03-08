from lib import network, header, device
import socket, os, sys, json

self_ip = device.get_config('self-defaultgateway')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((self_ip, 12345))
s.listen(10)
print 'log: server is running'
while True:
    try:
    	c, addr = s.accept()
        c.settimeout(5)
    	head = json.loads(c.recv(1024))

    	print 'process: ' + head['process-description']
    
    	if int(head['process-code']) == 20:
            network.receive_file(c, '/home/pi/TrailSafe/files/', 1024, head)

        if int(head['process-code']) == 60:
            if network.test_server_connection():
                c.send(header.send_code('61'))
            else:
                c.send(header.send_code('62'))

        if int(head['process-code']) == 21:
            network.forward_message(c, 12345, 5, head)

        if int(head['process-code']) == 40:
            response = network.send_message_to_server(12345, 10, json.dumps(head))
            if response is not None:
                c.send(json.dumps(response['message']))
            else:
                c.send(header.send_code('42'))
            
    except KeyboardInterrupt:
        print 'exit program.'
        break
    except:
        print 'unexpected error: ', sys.exc_info()[0]
