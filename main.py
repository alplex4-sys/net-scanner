import subprocess

def check_ping(ip):
    
    response = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.PIPE)
    
    if response.returncode == 0:
        return "ONLINE"
    else:
        return "OFFLINE"

#Пул адресов
targets = ["8.8.8.8", "127.0.0.1", "192.168.2.100"]

print("--- Сетевой сканер запущен ---")
for ip in targets:
    status = check_ping(ip)
    print(f"{ip} is {status}")
