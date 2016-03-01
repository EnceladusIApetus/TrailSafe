import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345

try:
    s.bind(('192.168.1.1', port))
except:
    s.bind(('192.168.1.254', port))
    print 'bind to 192.168.1.254'

s.listen(5)
while True:
    c, addr = s.accept()
    receive = c.recv(1024)
    print receive
    if receive in 'testInternetConnection':
        c.send('1')
    c.close()

