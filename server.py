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

                    if int(head['process-code']) == 21:
                        network.forward_message(c, 12345, 5, head)
                    
        except KeyboardInterrupt:
            print 'exit program.'
        except:
            print 'unexpected error: ', sys.exc_info()[0]
