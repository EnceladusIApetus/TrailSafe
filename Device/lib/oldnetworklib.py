

def receive_file(c, path, buff_size, header):
    header = json.loads(header)
    file_name = header['file-name']
    file_size = header['file-size']
    buff_size = header['buffer-size']
    print 'log: file name is ' + file_name
    print 'log: file size is ' + str(file_size)
    print 'log: buffer size is ' + str(buff_size)
    
    receive_data(c, path, buff_size, file_size, file_name)
    check_file(c, path, buff_size, file_size, file_name, 10)

    f = open(path + file_name, 'r')
    print 'log: total size is ' + str(os.fstat(f.fileno()).st_size)
    print '\n'
    f.close()
    c.close()

def receive_data(c, path, buff_size, file_size, file_name):
    f = open(path + file_name, 'w+')
    c.send(header.send_code('310'))
    print 'log: receiving data'
    data_buffer = None
    while(file_size > 0):
        data_buffer = c.recv(buff_size)
        f.write(data_buffer)
        file_size -= buff_size
    f.close()

def send_data(s, buff_size, size, path):
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

def validate_sending(s, buff_size, size, path, response):
    response = json.loads(response)
    print 'log: host->' + response['process-description']
    if response['process-code'] == 51:
        response = send_data(s, buff_size, size, path)
        while(response['process-code'] == 51 or response['process-code'] == 24):
            print 'log: host->' + response['process-description']
            response = send_data(s, buff_size, size, path)
    return response

def send_file_to_server(path, buff_size, file_name):
    send_file(get_defaultgateway('wlan0'), path, buff_size, file_name, 'SV')

def send_file(dest_ip, path, buff_size, file_name, recv_id):
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

    s.send(header.send_file(recv_id, file_name, buff_size, size))

    response = json.loads(s.recv(1024))
    print 'log: host->' + response['process-description']

    if response['process-code'] == 310:
        response = send_data(s, buff_size, size, path)
        return validate_sending(s, buff_size, size, path, statusCode)
    else:
        return None

def check_file(c, path, buff_size, file_size, file_name, tryout):
    f = open(path + file_name, 'r')
    while (os.fstat(f.fileno()).st_size < file_size and tryout > 0):
    	c.send(header.send_code('51'))
    	print 'log: file is corrupt'
    	print 'log: received ' + str(os.fstat(f.fileno()).st_size)
    	receive_data(c, path, buff_size, file_size, file_name)
    	tryout -= 1
        if tryout <= 0:
    	   c.send(header.send_code('24'))
    	   print 'log: stop receiving progress due to an error.'
        else:
    	   c.send(header.send_code('11'))
    	print 'log: receiving progress complete.'
