import socket
import struct
import os
import sys
import header
import json

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


def receiveFile(c, path, buff_size, header):
    header = json.loads(header)
    file_name = header['file-name']
    file_size = header['file-size']
    buff_size = header['buffer-size']
    print 'log: file name is ' + file_name
    print 'log: file size is ' + str(file_size)
    print 'log: buffer size is ' + str(buff_size)

    receiveData(c, path, buff_size, file_size, file_name)
    checkFile(c, path, buff_size, file_size, file_name, 10)

    f = open(path + file_name, 'r')
    print 'log: total size is ' + str(os.fstat(f.fileno()).st_size)
    print '\n'
    f.close()
    c.close()

def checkFile(c, path, buff_size, file_size, file_name, tryout):
    f = open(path + file_name, 'r')
    while (os.fstat(f.fileno()).st_size < file_size and tryout > 0):
    	c.send(header.sendCode('51'))
    	print 'log: file is corrupt'
    	print 'log: received ' + str(os.fstat(f.fileno()).st_size)
    	receiveData(c, path, buff_size, file_size, file_name)
    	tryout -= 1
        if tryout <= 0:
    	   c.send(header.sendCode('24'))
    	   print 'log: stop receiving progress due to an error.'
        else:
    	   c.send(header.sendCode('11'))
    	print 'log: receiving progress complete.'
 
def receiveData(c, path, buff_size, file_size, file_name):
    f = open(path + file_name, 'w+')
    c.send(header.sendCode('310'))
    print 'log: receiving data'
    data_buffer = None
    while(file_size > 0):
        data_buffer = c.recv(buff_size)
        f.write(data_buffer)
        file_size -= buff_size
    f.close()

def sendData(s, buff_size, size, path):
    target_file = open(path, 'r')
    print 'log: sending data'
    while(size >= 0):
        data_buffer = target_file.read(buff_size)
        s.send(data_buffer)
        size -= buff_size
    s.settimeout(5)
    response = s.recv(1024)
    target_file.close()
    return response

def validateSending(s, buff_size, size, path, response):
    response = json.loads(response)
    print 'log: host->' + response['process-description']
    if response['process-code'] == 51:
        response = sendData(s, buff_size, size, path)
        while(response['process-code'] == 51 or response['process-code'] == 24):
            print 'log: host->' + response['process-description']
            response = sendData(s, buff_size, size, path)
    return response

def sendFile(path, buff_size, file_name):
    sendFile(getDefaultGateway('wlan0'), path, buff_size, file_name, 'SV')

def sendFile(dest_ip, path, buff_size, file_name, recv_id):
    target_file = open(path, 'r')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    port = 12345
    s.connect((dest_ip, port))
    print 'log: host connected'

    size = 0
    for line in target_file:
        size += len(line)
    target_file.close()

    s.send(header.sendFile(recv_id, file_name, buff_size, size))

    response = json.loads(s.recv(1024))
    print 'log: host->' + response['process-description']

    if response['process-code'] == 310:
        response = sendData(s, buff_size, size, path)
        return validateSending(s, buff_size, size, path, statusCode)
    else:
        return None

def send_text(dest_ip, port, timeout, text):
    return send_text(dest_ip, port, timeout, text, 'SV'):

def send_text(dest_ip, port, timeout, text, recv_id):
    s = create_socket(dest_ip, port, timeout)
    try:
        if s is not None:
            s.send(header.sendText(recv_id))
            response = json.loads(s.recv(1024))
            print 'log: host->' + response['process-description']
            if response['process-code'] == 310:
                s.send(text)
                response = s.recv(1024)
                s.close()
                return response
    except:
        print 'log: sending text fail'
        s.close()
    return None

def forward_text(c, port, timeout, header):
    c.send(header.sendCode('310'))
    print 'log: request text'
    text = c.recv(1024)
    print 'log: text received'
    s = create_socket(getDefaultGateway('wlan0'), port, timeout)
    try:
        if s is not None:
            print 'log: connected to node'
            s.send(header.sendCode(header))
            print 'log: request to forward text'
            response = json.loads(s.recv(1024))
            print 'log: host->' + response['process-description']
            if response['process-code'] == 310:
                print 'log: forwarding'
                s.send(text)
                response = json.loads(s.recv(1024))
                print 'log: forwarding completed. send back response'
                c.send(response)
            s.close()
            c.close()
            return response
    except:
        print 'log: forwarding failed'
        s.close()
        c.close()
    return None

def create_socket(dest_ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    if s.connect_ex((dest_ip, port)) == 0:
        return s
    else:
        return None
