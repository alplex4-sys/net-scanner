import socket
import subprocess

# Функция проверки "живой" ли узел
def check_ping(ip):
    
    response = subprocess.run(['ping', '-n', '1', '-w', '500', ip], stdout=subprocess.PIPE)
    return response.returncode == 0

# Функция проверки конкретного порта
def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

# Основная логика
targets = ["8.8.8.8", "127.0.0.1","192.168.0.1","62.141.122.126"] 
common_ports = [21, 22, 80, 443, 3389]

print("=== Scanning Network ===")
for ip in targets:
    if check_ping(ip):
        print(f"\n[+] {ip} is ONLINE")
        for port in common_ports:
            if check_port(ip, port):
                print(f"    Port {port}: OPEN")
    else:
        print(f"[-] {ip} is OFFLINE")
       
input()