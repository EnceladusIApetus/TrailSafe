import socket
import os
import sys
from lib import jsonfile

def sendData(s, buff_size, size, path):
	target_file = open(path, 'r')
	print 'log: sending data'
	while(size >= 0):
		data_buffer = target_file.read(buff_size)
		s.send(data_buffer)
		size -= buff_size
	s.settimeout(5)
	statusCode = s.recv(1024)
	target_file.close()
	return statusCode

def validateSending(s, buff_size, size, path, statusCode):
	if statusCode in 'file is corrupt':
		statusCode = sendData(s, buff_size, size, path)
		while(statusCode in 'file is corrupt' or statusCode in 'stop sending'):
			statusCode = sendData(s, buff_size, size, path)

def sendFile(dest_ip, path, buff_size, fileName):
	target_file = open(path, 'r')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	port = 12345
	s.connect((dest_ip, port))

	print 'log: host connected'
	s.send('send file')
	print 'log: host->' + s.recv(1024)
	print 'log: send file name'
	s.send(fileName)
	print 'log: host->' + s.recv(1024)

	size = 0
	for line in target_file:
		size += len(line)
	target_file.close()

	print 'log: send file size'
	s.send(str(size))
	print 'log: host->' + s.recv(1024)
	print 'log: send buffer size'
	s.send(str(buff_size))

	statusCode = sendData(s, buff_size, size, path)
	validateSending(s, buff_size, size, path, statusCode)

jsonfile.open_file('/home/pi/TrailSafe/config/config.ini')
x = jsonfile.read()


dest_ip = sys.argv[1]
path = sys.argv[2]
fileName = sys.argv[3]
sendFile(dest_ip, path, 16, fileName)
