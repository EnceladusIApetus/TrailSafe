from lib import network, header, device, server
import json, thread, sys

s = server.init_socket()
thread.start_new_thread(server.auto_update_self_status, ())
print 'log: server is running'
while True:
   try:
    	c, addr = s.accept()
        c.settimeout(5)
        raw_head = c.recv(1024)
        head = json.loads(raw_head)
	message = None
        if 'message' in head:
            message = network.decap_message(raw_head)
            print 'process: ' + message['process-description']
    
    	if int(head['process-code']) == 20:
            network.receive_file(c, '/home/pi/TrailSafe/files/', 1024, head)

        if message is not None:
                if int(message['process-code']) == 60:  #test server connection
                    thread.start_new_thread(server.test_server_connection, (c, head))
                
                if int(message['process-code']) == 40:  #device registration
                    thread.start_new_thread(server.register_device, (c, head))

                if int(message['process-code']) == 80:  #update device status
                    thread.start_new_thread(server.update_status, (c, head))

                if int(message['process-code']) == 90:  #send event
                    thread.start_new_thread(server.send_event, (c, head))

                if int(message['process-code']) == 94:  #check responsing for emergency event
                    thread.start_new_thread(server.check_emergency_response, (c, head))

   except KeyboardInterrupt:
            print 'exit program.'
            sys.exit()
   except:
            print sys.exc_info()
            report = {}
            report['detail'] = 'an eror has occured in part of server'
            report['sys-info'] = str(sys.exc_info())
            server.send_self_event(1, json.dumps(report))
            s = server.init_socket()
            
