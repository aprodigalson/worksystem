from worksystem.spider.packet import IPPacket, TCPPacket
import ipaddress
from abc import ABCMeta, abstractmethod, ABC
from queue import Queue
import time

class NetDevice(object, metaclass=ABCMeta):
    def __init__(self):
        self.__packet_queue = Queue(maxsize=10)
        pass
    @abstractmethod
    def receive_packet(self, packet):
        pass

    @abstractmethod
    def send_packet(self):
        pass

    @property
    def packet_queue(self):
        return self.__packet_queue
        pass

    @packet_queue.setter
    def packet_queue(self, value):
        self.__packet_queue = value


class SLB(NetDevice):
    def __init__(self, msb):
        super(SLB, self).__init__()
        self.apiroute = msb
        self.service_ip_pool = ['2.2.2.2']
        self.nat_mapping = []

    def start(self):
        self.get_mapping_table()
        for ip in self.service_ip_pool:
            NetWork.add_socket(ip, '', 'slb', self)

    def receive_packet(self, packet):
        if isinstance(packet, TCPPacket):
            level, mapping = self.get_packet_level(packet)
            if level == 'l4':
                inner_ip = mapping.get('inner_ip')
                inner_port = mapping.get('inner_port')
                packet.set_dst_ip(inner_ip)
                packet.set_dst_port(inner_port)
                self.packet_queue.put(packet)
            elif level == 'l7':
                self.send_packet_to_apiroute(packet)
            else:
                print('no this mapping')

    def send_packet(self):
        return self.packet_queue.get()

    def get_packet_level(self, packet):
        for mapping in self.get_mapping_table():
            if mapping.get('service_port') == packet.get_dst_port():
                if mapping.get('protocol') == 'http':
                    return 'l7', mapping
                elif mapping.get('protocol') == 'tcp':
                    return 'l4', mapping
        return 'unknown', {}

    def get_mapping_table(self):
        service_table = self.apiroute.get_service_table()
        for service_ip in self.service_ip_pool:
            for service in service_table:
                rule = {
                    'service_ip': service_ip,
                    'service_port': service.get('service_external_port'),
                    'inner_ip': service.get('service_ip'),
                    'inner_port': service.get('service_port'),
                    'protocol': service.get('protocol')
                }
                if rule not in self.nat_mapping:
                    self.nat_mapping.append(rule)
        return self.nat_mapping
    def get_service_ip(self):
        return self.service_ip_pool
class NetWork(object):
    socket_list = []
    null_socket={
        'ip':'',
        'port':'',
        'name':'',
        'object':None,
    }
    @staticmethod
    def add_socket(ip, port, name, obj):
        NetWork.socket_list.append({
            'ip': ip,
            'port': port,
            'name': name,
            'object': obj
        })
    @staticmethod
    def get_socket(ip, port):
        for socket in NetWork.socket_list:
            if ip== socket.get('ip') and port == socket.get('port'):
                return socket
            if ip==socket.get('ip') and socket.get('port')=='':
                return socket
        return NetWork.null_socket

    @staticmethod
    def translate(packet):
        is_first = True
        while True:
            if isinstance(packet, TCPPacket):
                dst_ip = packet.get_dst_ip()
                dst_port = packet.get_dst_port()
                dst = NetWork.get_socket(dst_ip, dst_port)
                src_ip = packet.get_src_ip()
                src_port = packet.get_src_port()
                src = NetWork.get_socket(src_ip, src_port)
                if is_first:
                    print('[src:('+str(src_ip)+':'+str(src_port)+')'+
                          'dst:' + '('+str(dst_ip)+':'+str(dst_port)+')]' +
                          ' ===>> ' + str(dst.get('name')),
                          end=' ')
                    is_first = False
                else:
                    print('===>>[src:(' + str(src_ip) + ':' + str(src_port) + ')' +
                          'dst:' + '(' + str(dst_ip) + ':' + str(dst_port) + ')]' +
                          ' ===>> ' + str(dst.get('name')),
                          end='')
                dst_obj = dst.get('object')
                time.sleep(0.01)
                if isinstance(dst_obj, NetDevice):
                    dst_obj.receive_packet(packet)
                    packet = dst_obj.send_packet()
                    if packet is None:
                        break
                elif dst_obj is None:
                    break
            else:
                break


class MSB(object):
    def __init__(self):
        self.service_table = []
        self.port_list = list(range(10000,65535))
        self.allocated_port_list = []

    def get_service_publish_port(self, name):
        for service in self.service_table:
            if service.get('name') == name:
                return service.get('service_external_port')
        return 'unknown'



    def get_service_table(self):
        return self.service_table

    def service_cancel(self, service_name):
        for service in self.service_table:
            if service.get('name') == service_name:
                self.service_table.remove(service)
                return True

        return False

    def service_register(self, service_name ,service_ip, service_port, protocol):
        # add mapping table
        tmp_port = self.allocate_port_to_service()
        if tmp_port is None:
            print('port is running out')
            return False
        self.service_table.append({
            'name': service_name,
            'service_external_port': tmp_port,
            'service_ip': service_ip,
            'service_port': service_port,
            'protocol': protocol
        })
        return True

    def allocate_port_to_service(self):
        for port in self.port_list:
            if port not in self.allocated_port_list:
                self.allocated_port_list.append(port)
                return port
        return None

class K8S(object):
    def __init__(self):
        self.ip_pool = ipaddress.ip_network('172.10.0.0/16')
        self.port_pool = list(range(0,65535))

        self.allocated_ip_list = []
        self.allocated_port_list = []

        self.pod_list = []

    def allocate_ip_port(self, service):
        service_ip = ''
        service_port = ''
        for ip in self.ip_pool:
            if ip not in self.allocated_ip_list:
                ip=str(ip)
                self.allocated_ip_list.append(ip)
                service_ip = ip
                break
        for port in self.port_pool:
            if port not in self.allocated_port_list:
                self.allocated_port_list.append(port)
                service_port = port
                break
        self.pod_list.append({
            'service': service,
            'ip': service_ip,
            'port': service_port
        })

    def get_pod_ip_port(self, service_name):
        for pod in self.pod_list:
            if pod.get('service') == service_name:
                return pod.get('ip'), pod.get('port')
        return '', ''


class Service(NetDevice):
    def __init__(self, name, service_type='tcp'):
        super(Service, self).__init__()
        self.name = name
        self.type = service_type

    def start(self, k8s, msb):
        if isinstance(k8s, K8S):
            k8s.allocate_ip_port(self.name)
        ip, port = k8s.get_pod_ip_port(self.name)
        NetWork.add_socket(ip, port, self.name, self)
        if isinstance(msb, MSB):
            msb.service_register(self.name,ip, port, self.type)

    def stop(self, k8s, msb):
        pass

    def receive_packet(self, packet):
        if isinstance(packet, TCPPacket):
            self.packet_queue.put(packet)
            pass
    
    def send_packet(self):
        return None
        pass
    pass

class TCPClient(object):
    def generate_packet(self):
        pass


class Main(object):
    def main_thread(self):
        k8s = K8S()
        msb = MSB()
        service = Service('test_service', service_type='tcp')
        service.start(k8s, msb)
        slb = SLB(msb)
        slb.start()
        packet = TCPPacket(dst_ip=slb.get_service_ip()[0] ,
                           dst_port=msb.get_service_publish_port('test_service'))
        NetWork.translate(packet)


if __name__ == '__main__':
    Main().main_thread()