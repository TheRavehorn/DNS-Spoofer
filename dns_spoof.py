#!/usr/bin/env python3
from custom_queue import Queue
import subprocess


def get_ip():
    subprocess.call("ifconfig", shell=True)
    ip = input("Redirect to (IP) -> ")
    return ip


def get_site():
    site = input("Redirect from (domain) -> ")
    return site


print("DNS Spoofer 0.01 by Ravehorn")

ip = get_ip()
site = get_site()
# ip = "10.0.2.15"
# site = "jokes.com"

queue = Queue(ip, site)
