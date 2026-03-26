import socket
import subprocess
import re


def check_ping(ip):

    process = subprocess.run(['ping', '-n', '1', '-w', '500', ip], capture_output=True, text=True)
    return "TTL=" in process.stdout


def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0


while True:
    print("\n" + "="*30)
    print("=== Network Scanner ===")
    print("Введите 'exit' для выхода")
    user_input = input("Введите IP-адреса через запятую: ").strip().lower()

 
    if user_input == 'exit':
        print("Завершение работы...")
        break


    targets = [ip.strip() for ip in user_input.split(",") if ip.strip()]

    if not targets:
        print("[!] Ошибка: Вы ничего не ввели.")
        continue

    print("\n--- Начало сканирования ---")
    for ip in targets:
       
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            print(f"[!] {ip} - Некорректный формат IP-адреса")
            continue

        if check_ping(ip):
            print(f"\n[+] {ip} is ONLINE")
            common_ports = [21, 22, 80, 443, 3389]
            for port in common_ports:
                if check_port(ip, port):
                    print(f"    Port {port}: OPEN")
        else:
            print(f"[-] {ip} is OFFLINE")


input("\nPress enter to pay respect!")