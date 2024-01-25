import os

cmd = '''lastb | awk '/ssh/{print $3}' |sort | uniq -c |awk '{print $2"="$1}' > /root/scripts/ban_ip/BlackList '''

os.system(cmd)

suspect_ips = open('/root/scripts/ban_ip/BlackList')
banedip_list = [i.split(':')[1] for i in open('/etc/hosts.deny')]
for line in suspect_ips:
    IP = line.split('=')[0]
    NUM = int(line.split('=')[1])
    # print(type(IP))
    if IP not in banedip_list:
        if NUM >= 5:
            with open('/etc/hosts.deny', mode='a') as blacklist:
                blacklist.write('sshd:'+IP+':deny')
                
