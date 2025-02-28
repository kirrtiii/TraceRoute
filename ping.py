"""
Python implementation of the ping utility.

This module provides functionality to ping a specified host.
"""

import argparse
import time
from utils import create_packet, setup_socket, resolve_hostname
import socket
import struct

def ping(host, count, interval, packet_size, timeout):
    """
    Ping a specified host.

    This function sends ICMP Echo Request packets to a specified host and
    reports on the round-trip time and packet loss statistics.

    :param host: Hostname or IP address to ping
    :type host: str
    :param count: Number of ping requests to send (0 for infinite)
    :type count: int
    :param interval: Time interval between ping requests in seconds
    :type interval: float
    :param packet_size: Size of the ping packet in bytes
    :type packet_size: int
    :param timeout: Timeout for each ping request in seconds
    :type timeout: float
    """
    dest_addr = resolve_hostname(host)
    if not dest_addr:
        print(f"Ping: unknown host {host}")
        return

    print(f"PING {host} ({dest_addr}) {packet_size} bytes of data.")

    sock = setup_socket()
    my_id = 1234 
    seq_no = 0
    packets_sent = 0
    packets_received = 0

    try:
        while count == 0 or packets_sent < count:
            seq_no += 1
            packet = create_packet(my_id, seq_no, packet_size - 8) 
            sock.sendto(packet, (dest_addr, 1))
            packets_sent += 1

            send_time = time.time()
            sock.settimeout(timeout)
            try:
                recv_packet, addr = sock.recvfrom(1024)
                recv_time = time.time()
                icmp_header = recv_packet[20:28]
                type, code, checksum, packet_id, sequence = struct.unpack('!BBHHH', icmp_header)

                if type == 0 and packet_id == my_id:  
                    rtt = (recv_time - send_time) * 1000
                    print(f"{len(recv_packet)} bytes from {addr[0]}: icmp_seq={sequence} ttl=64 time={rtt:.2f} ms")
                    packets_received += 1
            except socket.timeout:
                print(f"Request timeout for icmp_seq {seq_no}")

            if count == 0 or packets_sent < count:
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\n--- Ping statistics ---")
    finally:
        print(f"{packets_sent} packets transmitted, {packets_received} received, {(1 - packets_received/packets_sent)*100:.1f}% packet loss")
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Ping Implementation")
    parser.add_argument("host", help="The host to ping")
    parser.add_argument("-c", "--count", type=int, default=0, help="Stop after sending count ECHO_REQUEST packets")
    parser.add_argument("-i", "--interval", type=float, default=1, help="Wait interval seconds between sending each packet")
    parser.add_argument("-s", "--packetsize", type=int, default=56, help="Specify the number of data bytes to be sent")
    parser.add_argument("-t", "--timeout", type=float, default=2, help="Specify a timeout in seconds")
    args = parser.parse_args()

    ping(args.host, args.count, args.interval, args.packetsize, args.timeout)
