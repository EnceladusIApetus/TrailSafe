import server, buffers, json, device

def transfer_buffer():
    head = buffers.dequeue()
    while head is not None:
      message = None
      if 'message' in head:
         message = json.loads(head['message'])
         print 'process: ' + message['process-description']

      device.set_config('test', message['process-description'])
        
      if int(head['process-code']) == 20:
         network.receive_file(None, '/home/pi/TrailSafe/files/', 1024, head)

      if int(head['process-code']) == 130:
         server.send_self_gps_coordinate(None, head)

      if message is not None:
         if int(message['process-code']) == 60:  #test server connection
            server.test_server_connection(None, head)
                      
         if int(message['process-code']) == 40:  #device registration
            server.register_device(None, head)

         if int(message['process-code']) == 80:  #update device status
            server.update_status(None, head)

         if int(message['process-code']) == 90:  #send event
            server.send_event(None, head)

         if int(message['process-code']) == 94:  #check responsing for emergency event
            server.check_emergency_response(None, head)

         if int(message['process-code']) == 110: #check risk status of each own device
            server.check_risk_status(None, head)

         if int(message['process-code']) == 130: #update gps
            server.update_gps_coordinate(None, head)

      head = buffers.dequeue()

