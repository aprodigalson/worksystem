from worksystem.spider.packet import IPPacket, Packet
import ipaddress
from abc import ABCMeta, abstractmethod, ABC
from queue import Queue
import time


class NetDevice(object, metaclass=ABCMeta):
    def __init__(self):
        self.__packet_queue = Queue(maxsize=10)
        pass

    def add_socket(self):
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
    def __init__(self, msb, service_ip_pool=None):
        super(SLB, self).__init__()
        self.apiroute = msb
        if service_ip_pool is None:
            self.service_ip_pool = ['2.2.2.2']
        else:
            self.service_ip_pool = service_ip_pool
        # nat 映射表，用于外访内匹配内部服务的IP端口
        self.nat_mapping = []
        self.packet_num = 0

    def start(self):
        self.get_mapping_table()
        for ip in self.service_ip_pool:
            # 如果要使用网络，则需要执行NetWork.add_socket方法，类似与网口的占用
            NetWork.add_socket(ip, '', 'slb', self)

    def receive_packet(self, packet):
        if isinstance(packet, Packet):
            if not self.need_slb_process(packet):
                print('packet is not need slb to process')
                return
            level, mapping = self.get_packet_level(packet)
            if level == 'l4':
                inner_ip = mapping.get('inner_ip')
                inner_port = mapping.get('inner_port')
                packet.set_dst_ip(inner_ip)
                packet.set_dst_port(inner_port)
                self.packet_queue.put(packet)
            elif level == 'l7':
                print('apiroute', end=' ')
                self.send_packet_to_apiroute(packet)
            else:
                print('no this mapping')

    def send_packet_to_apiroute(self,packet):
        if isinstance(self.apiroute, MSB):
            self.apiroute.receive_packet(packet)
            packet = self.apiroute.send_packet()
            self.packet_queue.put(packet)

    def send_packet(self):
        self.packet_num += 1
        return self.packet_queue.get(timeout=1)

    def need_slb_process(self, packet):
        if isinstance(packet, Packet):
            if packet.get_dst_ip() in self.get_all_service_ip():
                return True
        return False


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

    def get_all_service_ip(self):
        return self.service_ip_pool


class NetWork(object):
    socket_list = []
    null_socket = {
        'ip': '',
        'port': '',
        'name': '',
        'object': None,
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
            if ip == socket.get('ip') and port == socket.get('port'):
                return socket
            if ip == socket.get('ip') and socket.get('port') == '':
                return socket
        return NetWork.null_socket

    @staticmethod
    def translate_packets(packet_list):
        for packet in packet_list:
            NetWork.translate(packet)

    @staticmethod
    def translate(packet):
        is_first = True
        while True:
            if isinstance(packet, Packet):
                dst_ip = packet.get_dst_ip()
                dst_port = packet.get_dst_port()
                dst = NetWork.get_socket(dst_ip, dst_port)
                src_ip = packet.get_src_ip()
                src_port = packet.get_src_port()
                src = NetWork.get_socket(src_ip, src_port)
                if is_first:
                    print('[src:(' + str(src_ip) + ':' + str(src_port) + ')' +
                          'dst:' + '(' + str(dst_ip) + ':' + str(dst_port) + ')]' +
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
        print('\n')


class MSB(NetDevice):
    def __init__(self):
        super(MSB, self).__init__()
        self.service_table = []
        self.port_list = list(range(10000, 65535))
        self.allocated_port_list = []

    def receive_packet(self, packet):
        if isinstance(packet, Packet):
            port = packet.get_dst_port()
            service = self.get_service_by_port(port)
            if service is None:
                print('packet not need msb to process')
                return
            inner_ip = service.get('service_ip')
            inner_port = service.get('service_port')
            packet.set_dst_ip(inner_ip)
            packet.set_dst_port(inner_port)
            self.packet_queue.put(packet)
        pass

    def send_packet(self):
        return self.packet_queue.get(timeout=1)

    def get_service_by_port(self, port):
        for service in self.service_table:
            if port == service.get('service_external_port'):
                return service
        return None

    def get_service_publish_port(self, name):
        for service in self.service_table:
            if service.get('name') == name:
                return service.get('service_external_port')
        return 'unknown'

    def get_all_service_publish_port(self):
        res = []
        for service in self.service_table:
            res.append(service.get('service_external_port'))
        return res

    def get_service_table(self):
        return self.service_table

    def service_cancel(self, service_name):
        for service in self.service_table:
            if service.get('name') == service_name:
                self.service_table.remove(service)
                return True

        return False

    def service_register(self, service_name, service_ip, service_port, protocol):
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
        self.port_pool = list(range(0, 65535))

        self.allocated_ip_list = []
        self.allocated_port_list = []

        self.pod_list = []

    def allocate_ip_port(self, service):
        service_ip = ''
        service_port = ''
        for ip in self.ip_pool:
            if ip not in self.allocated_ip_list:
                ip = str(ip)
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
            msb.service_register(self.name, ip, port, self.type)

    def stop(self, k8s, msb):
        pass

    def receive_packet(self, packet):
        if isinstance(packet, Packet):
            self.packet_queue.put(packet)
            pass

    def send_packet(self):
        return None
        pass

    pass


class TCPClient(object):
    def generate_packet(self, nums=1,
                        src_ip_list=None,
                        dst_ip_list=None,
                        src_port_list=None,
                        dst_port_list=None):
        if src_ip_list is None:
            src_ip_list = ['1.1.1.1'] * nums
        if dst_ip_list is None:
            dst_ip_list = ['2.2.2.2'] * nums
        if src_port_list is None:
            src_port_list = [1000] * nums
        if dst_port_list is None:
            dst_port_list = [2000] * nums
        min_length = min([len(src_port_list),
                          len(src_ip_list),
                          len(dst_port_list),
                          len(dst_ip_list)])
        res = []
        for index in range(min_length):
            packet = Packet(src_ip=src_ip_list[index],
                            src_port=src_port_list[index],
                            dst_ip=dst_ip_list[index],
                            dst_port=dst_port_list[index],
                            proto='http')
            res.append(packet)
        if len(res) < nums:
            res.extend([res[0] for _ in range(nums - len(res))])
        return res


class Main(object):
    @staticmethod
    def main_thread():
        k8s = K8S()
        msb = MSB()
        service_name = 'test-service-1'
        service = Service(service_name,
                          service_type='tcp')
        service.start(k8s, msb)
        service_ip_pool = ['10.68.4.25', '120.53.30.236']
        slb = SLB(service_ip_pool=service_ip_pool,
                  msb=msb)
        slb.start()

        client = TCPClient()
        packets = client.generate_packet(nums=10,
                                         dst_ip_list=slb.get_all_service_ip(),
                                         dst_port_list=msb.get_all_service_publish_port())
        NetWork.translate_packets(packets)
        print(slb.packet_num)


if __name__ == '__main__':
    Main().main_thread()
