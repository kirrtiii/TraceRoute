"""
Utility functions for network operations.

This module provides common functions used in ping and traceroute implementations,
including packet creation, checksum calculation, and DNS resolution.
"""

import socket
import struct
import time

def create_packet(id, seq, payload_size):
    """
    Create an ICMP Echo Request packet.

    :param id: Identifier for the packet
    :type id: int
    :param seq: Sequence number for the packet
    :type seq: int
    :param payload_size: Size of the packet payload
    :type payload_size: int
    :return: Bytes object representing the ICMP packet
    :rtype: bytes
    """
    header = struct.pack('!BBHHH', 8, 0, 0, id, seq)
    payload = bytes([i & 0xff for i in range(payload_size)])
    checksum_val = calculate_checksum(header + payload)
    header = struct.pack('!BBHHH', 8, 0, checksum_val, id, seq)
    return header + payload

def calculate_checksum(data):
    """
    Calculate the checksum for an ICMP packet.

    :param data: Data to calculate checksum for
    :type data: bytes
    :return: Calculated checksum
    :rtype: int
    """
    sum = 0
    for i in range(0, len(data), 2):
        sum += (data[i] << 8) + (data[i+1] if i+1 < len(data) else 0)
    sum = (sum >> 16) + (sum & 0xffff)
    sum += sum >> 16
    return ~sum & 0xffff

def setup_socket():
    """
    Set up a raw socket for ICMP communication.

    :return: Configured socket object
    :rtype: socket.socket
    """
    icmp = socket.getprotobyname("icmp")
    return socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

def resolve_hostname(hostname):
    """
    Resolve a hostname to its IP address.

    :param hostname: Hostname to resolve
    :type hostname: str
    :return: IP address of the hostname, or None if unresolvable
    :rtype: str or None
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def get_hostname(ip_address):
    """
    Get the hostname for a given IP address.

    :param ip_address: IP address to lookup
    :type ip_address: str
    :return: Hostname if found, otherwise the original IP address
    :rtype: str
    """
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return ip_address
