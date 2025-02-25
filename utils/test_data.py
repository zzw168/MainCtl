import socket

import psutil

def check_network_with_ip():
    interfaces = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()

    for iface, stats in interfaces.items():
        if stats.isup:
            ip_info = addresses.get(iface, [])
            mac = [addr.address for addr in ip_info if addr.family == psutil.AF_LINK]
            ip = [addr.address for addr in ip_info if addr.family == socket.AF_INET]
            if mac:
                return [iface, mac[0], ip[0]]
            ip_display = ip[0] if ip else "无IP"
            mac_display = mac[0] if mac else "无MAC"
            print(f"网卡: {iface} 联通, IP: {ip_display}, MAC: {mac_display}, 速度: {stats.speed} Mbps")
            # return False
        # else:
        #     print(f"网卡: {iface} 未联通")

def check_network_interface_status():
    interfaces = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()
    for interface, stats in interfaces.items():
        if stats.isup:
            ip_info = addresses.get(interface, [])
            mac = [addr.address for addr in ip_info if addr.family == psutil.AF_LINK]
            ip = [addr.address for addr in ip_info if addr.family == socket.AF_INET]
            if mac:
                return [interface, mac[0], ip[0]]
            print(f"Interface {interface} {mac} is UP!")
        else:
            print(f"Interface {interface} is DOWN!")

a = check_network_interface_status()
print(a)