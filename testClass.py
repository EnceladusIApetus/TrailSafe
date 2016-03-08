from lib import jsonfile, header
import socket, json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect_ex(('192.168.1.1', 12345))
s.send(header.send_code('60'))
response = json.loads(s.recv(1024))
print 'host: ' + response['process-description']

if int(response['process-code']) == 61:
	print 'host: ' + response['process-description']