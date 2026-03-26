import socket
import subprocess
import re

def get_arp_targets():
    print("[*] Чтение ARP-таблицы...")
    arp_output = subprocess.check_output(['arp', '-a']).decode('cp866')
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ips = re.findall(ip_pattern, arp_output)
    
    unique_ips = list(set([ip for ip in ips if not ip.endswith('.255')]))
    return unique_ips

def check_ping(ip):
    response = subprocess.run(['ping', '-n', '1', '-w', '200', ip], stdout=subprocess.PIPE)
    return response.returncode == 0

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

common_ports = [21, 22, 80, 443, 3389, 8080]

if __name__ == "__main__":
    targets = get_arp_targets()
    print(f"[+] Найдено потенциальных целей: {len(targets)}")
    
    for ip in targets:
        if check_ping(ip):
            print(f"\n[!] Узел {ip} активен")
            for port in common_ports:
                if check_port(ip, port):
                    print(f"    [+] Порт {port} ОТКРЫТ")
        else:
            print(f"[-] Узел {ip} не отвечает")
input("Press enter to pay respect!")
