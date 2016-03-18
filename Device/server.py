from lib import network, header, device
import socket, os, sys, json

def run_server():
        
    s = server.init_socket()
    print 'log: server is running'
    try:
        while True:
            c, addr = s.accept()
            c.settimeout(5)
            head = json.loads(c.recv(1024))

            print 'process: ' + head['process-description']

            if int(head['process-code']) == 21:
                network.forward_message(c, 12345, 5, head)
                    
    except KeyboardInterrupt:
        print 'exit program.'
        c.close()
        s.close()
        sys.exit()
    except:
        print 'unexpected error: ', sys.exc_info()
        network.send_event(1, str(sys.exc_info()))
        c.close()
        s.close()
        s = server.init_socket()
