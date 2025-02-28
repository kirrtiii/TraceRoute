# Ping & Traceroute

## **Introduction**
This project provides Python implementations of `ping` and `traceroute`, similar to their Linux counterparts. These tools help analyze network connectivity and diagnose routing paths.

- **Ping (`ping.py`)**: Sends ICMP Echo Request packets to a target host and measures response times.
- **Traceroute (`traceroute.py`)**: Traces the path packets take to reach a destination, showing each hop along the route.

Both scripts use **raw sockets** to generate ICMP packets, ensuring compatibility with real network infrastructure.

## **Installation**
### **Prerequisites**
- Python 3.x
- Install dependencies:
  ```sh
  pip install -r requirements.txt

## **How to Run**
- python ping.py <host>
- Ping with Count (-c)
  - python ping.py <host> -c <count>
- Ping with Interval (-i)
  - python ping.py <host> -i <interval>
- Ping with Packet size (-s)
  - python ping.py <host> -s <size>
- Ping with Timeout (-t)
  - python ping.py <host> -t <timeout>

- python traceroute.py <host>
- Traceroute with NO hostname resolution (-n)
  - python traceroute.py <host> -n
- Traceroute with custom queries per hop (-q)
  - python traceroute.py <host> -q <queries>
- Traceroute with NO hostname resolution (-n)
  - python traceroute.py <host> -n
- Traceroute with Summary (-S)
  - python traceroute.py <host> -S


