from lib import network, header, device, server
import socket, os, sys, json, thread

thread.start_new_thread(network.auto_update_status, ())
while(True):
    try:
        s = server.init_socket()
        print 'log: server is running'
        while True:
            c, addr = s.accept()
            c.settimeout(5)
            head = json.loads(c.recv(1024))

            print 'process: ' + head['process-description']

            if int(head['process-code']) == 21:
                network.forward_message(c, 12345, 5, head)

            if int(head['process-code']) == 100:
                network.reply_device_info(c)
                        
    except KeyboardInterrupt:
        print 'exit program.'
        sys.exit()
    except:
        report = {}
        report['detail'] = 'an eror has occured in part of server'
        report['sys-info'] = str(sys.exc_info())
        network.send_event(0, json.dumps(report))
        print 'unexpected error: ', sys.exc_info()
        s = server.init_socket()
