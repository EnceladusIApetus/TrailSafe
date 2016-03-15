from lib import network, header, device
import socket, os, sys, json, httplib, urllib, thread

self_ip = device.get_config('self-defaultgateway')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((self_ip, 12345))
s.listen(10)
print 'log: server is running'
while True:
  
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
                    thread.start_new_thread(network.test_server_connection_in, (c, head))

                if int(message['process-code']) == 40:  #device registration
                    thread.start_new_thread(network.register_device_in, (c, head))

                if int(message['process-code']) == 80:  #update device status
                    thread.start_new_thread(network.update_status_in, (c, head))

                if int(message['process-code']) == 90:  #send event
                    thread.start_new_thread(network.send_event_in, (c, head))

                if int(message['process-code']) == 94:  #check responsing for emergency event
                    thread.start_new_thread(network.check_emergency_response_in, (c, head))
            

