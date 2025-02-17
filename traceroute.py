"""
Python implementation of the traceroute utility.

This module provides functionality to trace the route to a specified host,
showing the path that packets take to reach the destination.
"""

import argparse
import time
from utils import create_packet, setup_socket, resolve_hostname, get_hostname
import socket

def traceroute(dest_addr, max_hops=30, timeout=1, queries=3, numeric=False, summary=False):
    """
    Perform a traceroute to a specified destination.

    This function sends packets with increasing TTL values to discover the path
    to the destination and measure round-trip times for each hop.

    :param dest_addr: Destination hostname or IP address
    :type dest_addr: str
    :param max_hops: Maximum number of hops to probe (default: 30)
    :type max_hops: int
    :param timeout: Timeout for each probe in seconds (default: 1)
    :type timeout: float
    :param queries: Number of queries per hop (default: 3)
    :type queries: int
    :param numeric: If True, print numeric addresses only (default: False)
    :type numeric: bool
    :param summary: If True, print summary of unanswered probes (default: False)
    :type summary: bool
    """
    dest_ip = resolve_hostname(dest_addr)
    if not dest_ip:
        print(f"traceroute: unknown host {dest_addr}")
        return

    print(f"traceroute to {dest_addr} ({dest_ip}), {max_hops} hops max")

    sock = setup_socket()
    my_id = 1234

    for ttl in range(1, max_hops + 1):
        unanswered = 0
        print(f"{ttl}", end="  ")
        
        for seq in range(queries):
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            packet = create_packet(my_id, seq, 36)  # 36 bytes payload
            
            send_time = time.time()
            sock.sendto(packet, (dest_ip, 33434))  # 33434 is a common starting port for traceroute
            
            try:
                sock.settimeout(timeout)
                recv_packet, addr = sock.recvfrom(1024)
                recv_time = time.time()
                
                if addr[0] == dest_ip:
                    rtt = (recv_time - send_time) * 1000
                    if not numeric:
                        addr = (get_hostname(addr[0]), addr[1])
                    print(f"{addr[0]} {rtt:.3f} ms", end="  ")
                    if seq == queries - 1:
                        print()
                    return
                else:
                    rtt = (recv_time - send_time) * 1000
                    if not numeric:
                        addr = (get_hostname(addr[0]), addr[1])
                    print(f"{addr[0]} {rtt:.3f} ms", end="  ")
            except socket.timeout:
                print("* ", end="")
                unanswered += 1
        
        print()
        if summary and unanswered > 0:
            print(f"  {unanswered}/{queries} probes unanswered for this hop")

    print("Traceroute completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Traceroute Implementation")
    parser.add_argument("host", help="Destination host")
    parser.add_argument("-n", action="store_true", help="Print numeric addresses")
    parser.add_argument("-q", type=int, default=3, help="Number of queries per hop")
    parser.add_argument("-S", action="store_true", help="Print probe summary")
    args = parser.parse_args()

    traceroute(args.host, queries=args.q, numeric=args.n, summary=args.S)
