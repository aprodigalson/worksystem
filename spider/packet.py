import struct
import socket
import scapy
from scapy.layers.inet import IP, Ether, TCP
from scapy.layers.http import HTTP
from scapy.layers.l2 import ARP
from scapy.sendrecv import send, sendp


class MACPacket(object):
    def __init__(self):
        pass


class IPPacket(object):
    def __init__(self):
        self.packet = IP()


class Packet(object):
    def __init__(self, src_ip='1.1.1.1', src_port=2000, dst_ip='2.2.2.2', dst_port=1024, proto='tcp'):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = proto
        self.ip_packet = IP(src=self.src_ip, dst=self.dst_ip)
        self.tcp_packet = TCP(sport=self.src_port, dport=self.dst_port)
        self.http_packet = HTTP()

    def get_protocol(self):
        return self.protocol

    def get_src_port(self):
        return self.tcp_packet.fields.get('sport')

    def get_src_ip(self):
        return self.ip_packet.fields.get('src')

    def get_dst_port(self):
        return self.tcp_packet.fields.get('dport')

    def get_dst_ip(self):
        return self.ip_packet.fields.get('dst')

    def set_src_port(self, src_port):
        self.src_port = src_port
        self.tcp_packet.setfieldval('sport', src_port)

    def set_src_ip(self, src_ip):
        self.src_ip = src_ip
        self.ip_packet.setfieldval('src', src_ip)

    def set_dst_port(self, dst_port):
        self.dst_port = dst_port
        self.tcp_packet.setfieldval('dport', dst_port)

    def set_dst_ip(self, dst_ip):
        self.dst_ip = dst_ip
        self.ip_packet.setfieldval('dst', dst_ip)


class HttpPacket(object):
    def __init__(self):
        pass


class Utils(object):
    @staticmethod
    def make_ip_header(src_ip='1.0.0.1', dst_ip='2.0.0.2', proto=socket.IPPROTO_TCP):
        ip_ver = 4
        ip_ihl = 5
        ip_tos = 0
        ip_tol_len = 0
        ip_id = 54321
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = proto
        ip_check = 0
        ip_src_addr = socket.inet_aton(src_ip)
        ip_dst_addr = socket.inet_aton(dst_ip)

        ip_ver_ihl = ip_ver << 4 + ip_ihl
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                ip_ver_ihl, ip_tos, ip_tol_len,
                                ip_id, ip_frag_off,
                                ip_ttl, ip_proto, ip_check,
                                ip_src_addr,
                                ip_dst_addr)
        return ip_header

    @staticmethod
    def make_tcp_header(ip_header, src_port=1024, dst_port=10086, src_ip='1.0.0.1', dst_ip='2.0.0.2', user_data='test'):
        src_port = src_port
        dst_port = dst_port
        tcp_seq = 111
        tcp_ack_seq = 0
        tcp_doff = 5
        tcp_fin = 0
        tcp_syn = 1
        tcp_rst = 0
        tcp_psh = 0
        tcp_ack = 0
        tcp_urg = 0
        tcp_window = socket.htons(2000)
        tcp_check = 0
        tcp_urg_ptr = 0

        tcp_offset = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
        tcp_header = struct.pack('!HHLLBBHHH',
                                 src_port, dst_port,
                                 tcp_seq,
                                 tcp_ack_seq,
                                 tcp_offset, tcp_flags, tcp_window,
                                 tcp_check, tcp_urg_ptr)


if __name__ == '__main__':
    pkt = Ether(src='11:22:33:44:55:77', dst='11:22:33:44:55:66') / ARP(op="who-has", pdst='1.1.1.200')
    # sendp(pkt, inter=1, count=5, iface="en0")
    tcp = Packet()
    print(tcp.get_src_port())
    print(tcp.get_src_ip())
    print(tcp.get_dst_ip())
    print(tcp.get_dst_port())
    tcp.set_dst_ip('1.1.1.1')
    print(tcp.get_dst_ip())
