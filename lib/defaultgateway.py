import socket
import struct

def get_defaultgateway_hex(interface):
    route = "/proc/net/route"
    with open(route) as f:
        for line in f.readlines():
            try:
                iface, dest, gateway, flags, _, _, _, _, _, _, _, =  line.strip().split()
                if iface == interface:
                    return gateway
            except:
                continue

def get_defaultgateway(interface):
    ip_hex = int(getdefaultgateway_hex(interface), 16)
    return socket.inet_ntoa(struct.pack('<L', ip_hex))


