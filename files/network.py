import socket
import struct
import os
import sys

def getDefaultGateway_hex(interface):
    route = "/proc/net/route"
    with open(route) as f:
        for line in f.readlines():
            try:
                iface, dest, gateway, flags, _, _, _, _, _, _, _, =  line.strip().split()
                if iface == interface:
                    return gateway
            except:
                continue

def getDefaultGateway(interface):
    ip_hex = int(getDefaultGateway_hex(interface), 16)
    return socket.inet_ntoa(struct.pack('<L', ip_hex))


def receiveFile(c, path, buff_size):
    print 'log: request file name'
    c.send('request file name')
    fileName = c.recv(1024)
    print 'log: file name is ' + fileName
    print 'log: request file size'
    c.send('request file size')
    fileSize = int(c.recv(1024))
    print 'log: file size is ' + str(fileSize)
    print 'log: request buffer size'
    c.send('request buffer size')
    buff_size = int(c.recv(1024))
    print 'log: buffer size is ' + str(buff_size)

    receiveData(c, path, buff_size, fileSize, fileName)
    checkFile(c, path, buff_size, fileSize, fileName, 10)

    f = open(path + fileName, 'r')
    print 'log: total size is ' + str(os.fstat(f.fileno()).st_size)
    print '\n'
    f.close()
    c.close()

def checkFile(c, path, buff_size, fileSize, fileName, tryout):
    f = open(path + fileName, 'r')
    while (os.fstat(f.fileno()).st_size < fileSize and tryout > 0):
	c.send('file is corrupt')
	print 'log: file is corrupt'
	print 'log: received ' + str(os.fstat(f.fileno()).st_size)
	receiveData(c, path, buff_size, fileSize, fileName)
	tryout -= 1
    if tryout <= 0:
	c.send('stop sending')
	print 'log: stop receiving progress due to an error.'
    else:
	c.send('success')
	print 'log: receiving progress complete.'
 
def receiveData(c, path, buff_size, fileSize, fileName):
    f = open(path + fileName, 'w+')
    print 'log: receiving data'
    data_buffer = None
    while(fileSize > 0):
        data_buffer = c.recv(buff_size)
        f.write(data_buffer)
        fileSize -= buff_size
    f.close()

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
