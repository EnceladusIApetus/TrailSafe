import socket
import struct

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


