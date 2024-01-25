import re
import os
from collections import Counter

def get_ip_dict(log_file_path='/var/log/nginx/access.log'):
    ip_dict = Counter()
    log_pattern = re.compile(r'(?P<ip>.*?)- - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>.*?) (?P<bytes>.*?) "(?P<referer>.*?)" "(?P<ua>.*?)"')

    with open(log_file_path, mode='r') as file:
        for line in file:
            line = line.strip()
            result = log_pattern.match(line)
            if result:
                status = int(result.group("status"))
                if 400 <= status < 500:
                    ip = result.group("ip")
                    ip_dict[ip] += 1
        
    return ip_dict

def get_banned_ips():
    ufw_status = os.popen('ufw status').read()
    ips = re.findall(r"\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", ufw_status)
    return ips

def main():
    log_file_path = '/var/log/nginx/access.log'
    ip_dict = get_ip_dict(log_file_path)
    banned_ips_list = get_banned_ips()

    for ip, num in ip_dict.items():
        if int(num) >= 4:
            # print(ip)
            if ip.strip() not in map(str.strip, banned_ips_list):
                os.system(f"ufw deny from {ip}")

if __name__ == "__main__":
    main()

