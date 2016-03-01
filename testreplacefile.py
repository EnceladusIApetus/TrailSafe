filedata = None
with open('interfaces', 'r') as file:
    filedata = file.read()

filedata = filedata.replace('192.168.1.1', 'address 192.168.1.1')

with open('interfaces', 'w') as file:
    file.write(filedata)
