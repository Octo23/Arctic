import External_Key
import requests
import json
import sys
import socket
from time import sleep
import threading, time
from datetime import datetime

def tx_func():
    sleep (2)
    portNum = 12122

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.1)

    message = "Query,BlueFalls,\n"
    sock.sendto(message.encode("ascii"), ("255.255.255.255", portNum))

def find():
    transmit = threading.Thread(target=tx_func)
    transmit.start()
    sockRx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockRx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sockRx.bind(("0.0.0.0", 21212))
    spaAddr = "0.0.0.0"
    while "0.0.0.0" == spaAddr:
    # sock.sendto(bytes("hello", "utf-8"), ip_co)
        data, addr = sockRx.recvfrom(1024)
        #print(data)
        if len(addr) > 1:
            spaAddr = addr[0]
            return spaAddr

def pushOverSend(msg, msgPriority="low"):
    import http.client, urllib
    priority = 0
    retry = 0
    expire = 0
    if (msgPriority == "high"):
        priority = 2
        retry = 120
        expire = 10800
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": External_Key.push_token,
        "user": External_Key.push_user,
        "message": msg,
        "priority": priority,
        "retry": retry,
        "expire": expire,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    pushResp = conn.getresponse()

def api_Connection_Status():
    secret = External_Key.API_Key_secret
    

    

    headers = {'X-API-KEY': secret}

    url_status = 'https://api.myarcticspa.com/v2/spa/status'
    try:
        response = requests.get(url_status, headers=headers)
        response_json = response.json()
    except:
        print("Something went wrong, double check your API key " + str(datetime.now()))
        exit(-1)


    for key, value in response_json.items():
        if key == 'connected':
            connected = value
    #return False, just for testing purposes
    #return False
    return connected

#check the API for connection status, if it fails, wait 90 seconds and try again, then wait an additional 90 seconds
#If the API call reports a connection at least once in three minutes, don't reboot and exit, otherwise reboot.
spa_IP = External_Key.SPA_IP
if len(sys.argv) > 1:
    try:
        socket.inet_aton(sys.argv[1])
        spa_IP = sys.argv[1]
    except:
        print("The only argument that can be set is the IP address of the spa, it can also be set in the External_Key file, otherwise this script will attempt to find the spa")
        exit(-1)

if api_Connection_Status():
    print("Spa appears to be responding as expected, exiting " + str(datetime.now()))
    exit(1)
else:
    print("API failed first attempt " + str(datetime.now()))
    sleep(90)
    if api_Connection_Status():
        print("Spa is delayed, but appears to be responding as expected, exiting " + str(datetime.now()))
        exit(1)
    else:
        print("API failed second attempt " + str(datetime.now()))
        sleep(90)
        if api_Connection_Status():
            print("Spa is really delayed, but appears to be responding as expected, exiting " + str(datetime.now()))
            exit(1)
        else:
            if spa_IP == "0.0.0.0":
                spa_IP = find()

data= {
    'submit': 'Reboot'
    }
r = requests.post('http://' + spa_IP + ':8080/rebootTarget', data=data)

print (r.text + str(datetime.now()))

if External_Key.pushOver:
    pushOverSend("Spa has been rebooted for website connectivity " + str(datetime.now()), "high")
