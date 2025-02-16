import socket
import struct
import time

def create_packet(id, seq, payload_size):
    header = struct.pack('!BBHHH', 8, 0, 0, id, seq)
    payload = bytes([i & 0xff for i in range(payload_size)])
    checksum_val = calculate_checksum(header + payload)
    header = struct.pack('!BBHHH', 8, 0, checksum_val, id, seq)
    return header + payload

def calculate_checksum(data):
    sum = 0
    for i in range(0, len(data), 2):
        sum += (data[i] << 8) + (data[i+1] if i+1 < len(data) else 0)
    sum = (sum >> 16) + (sum & 0xffff)
    sum += sum >> 16
    return ~sum & 0xffff

def setup_socket():
    icmp = socket.getprotobyname("icmp")
    return socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def get_hostname(ip_address):
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return ip_address
