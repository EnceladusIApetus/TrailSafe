from lib import jsonfile, header
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect_ex(('192.168.1.1', 12345))
s.send(header.sendCode('60'))
print s.recv(1024)