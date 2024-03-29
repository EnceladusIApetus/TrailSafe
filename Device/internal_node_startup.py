from lib import network, header, device, server, gpio
import json, thread, sys

gpio.init()
gpio.clear()
gpio.set_output(gpio.get_pin('led-main-system'))
gpio.set_output(gpio.get_pin('led-emergency'))
gpio.set_output(gpio.get_pin('led-server-connection'))
s = server.init_socket()
server.auto_update_self_status()
print 'log: server is running'
while True:
   gpio.on(gpio.get_pin('led-main-system'))
   try:
      c, addr = s.accept()
      c.settimeout(5)
      raw_head = c.recv(1024)
      head = json.loads(raw_head)
      print raw_head
      message = None
      if 'message' in head:
         message = network.decap_message(raw_head)
         print 'process: ' + message['process-description']
          
      if int(head['process-code']) == 20:
         network.receive_file(c, '/home/pi/TrailSafe/files/', 1024, head)

      if int(head['process-code']) == 130:
         server.send_self_gps_coordinate(c, head)

      if int(head['process-code']) == 100:
         network.reply_device_info(c)

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

         if int(message['process-code']) == 110: #check risk status of each own device
            thread.start_new_thread(server.check_risk_status, (c, head))

         if int(message['process-code']) == 130: #update gps
            thread.start_new_thread(server.update_gps_coordinate, (c, head))

   except KeyboardInterrupt:
      print 'exit program.'
      sys.exit()
   except:
      """print sys.exc_info()
      report = {}
      report['detail'] = 'an eror has occured in part of server'
      report['sys-info'] = str(sys.exc_info())
      server.send_self_event(0, json.dumps(report))
      s = server.init_socket()"""
                  
