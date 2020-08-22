#!/usr/bin/env python3
import subprocess

try:
    import netfilterqueue
    import scapy
except ModuleNotFoundError:
    subprocess.call("apt-get update", shell=True)
    subprocess.call("apt-get install python3-pip git tcpdump libnfnetlink-dev libnetfilter-queue-dev -y", shell=True)
    subprocess.call("pip3 install python3-scapy --quiet", shell=True)
    subprocess.call("pip3 install -U git+https://github.com/kti/python-netfilterqueue --quiet", shell=True)
finally:
    subprocess.call("clear", shell=True)
