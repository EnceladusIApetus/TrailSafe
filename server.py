from lib import network, header, device
import socket, os, sys, json

def run_server():
    while(1):
        try:
            s = network.init_socket()

            print 'log: server is running'
            while True:
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
        except:
            print 'unexpected error: ', sys.exc_info()[0]
