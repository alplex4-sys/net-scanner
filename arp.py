import socket
import subprocess
import re

def get_arp_targets():
    print("[*] Чтение ARP-таблицы...")
    arp_output = subprocess.check_output(['arp', '-a']).decode('cp866')
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ips = re.findall(ip_pattern, arp_output)
    
    unique_ips = []
    for ip in set(ips):
        octets = [int(o) for o in ip.split('.')]
        
        if octets[3] == 255:
            continue
        if 224 <= octets[0] <= 239:
            continue
        if ip in ["255.255.255.255", "0.0.0.0"]:
            continue
            
        unique_ips.append(ip)
        
    return unique_ips

def check_ping(ip):
    process = subprocess.run(['ping', '-n', '1', '-w', '200', ip], capture_output=True, text=True)
    return "TTL=" in process.stdout

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

input("\nPress enter to pay respect!")