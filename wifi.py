import time
import network
import usocket as socket
import ure as re

sever=True
choose=0
addr = ("192.168.4.1",80)

html0='''<!DOCTYPE html><html><body><form method="get"><input type="text" name="ssid" value="ssid"/><input type="text" name="password" value="password"/><input type="submit" value="send"/></from></body></html>'''

html1='''<!DOCTYPE html><html><body>success</body></html>'''

html2='''<!DOCTYPE html><html><body>ssid or password was wrong<form method="get"><input type="submit" value="send"/></from></body></html>'''

#当WiFi连接失败，运行此函数，通过手机连接热点ESP-AP浏览器访问192.168.4.1获取WiFi信息
#获取成功时返回True
def html_sever():
    ap = network.WLAN(network.AP_IF)     #创建ap接入点
    ap.active(True)
    ap.config(essid='ESP-AP',password='123456789')
    ap.config(essid='ESP-AP',channel=1) #设置接入点的ESSID，和WiFi 通道
    sk = socket.socket()#创建socket套接字
    sk.bind(addr)
    sk.listen(3)
    while sever:
        con, add = sk.accept()
        data = con.recv(1024) #等待数据
        data_utf8=str(data.decode('utf8'))#将接受的数据转换为utf8格式
        find_write(data_utf8)
        send_html(con) #将HTML页面发送到80端口
        con.close()
    time.sleep(1)
    sk.close() #关闭socket
    ap.active(False)
    return True


def find_write(get):#将获取到的WiFi信息写入data.txt
    match=re.search(r"GET /\?ssid=(.*?)&password=(.*?) HTTP",get)#从HTML返回的数据中获取WiFi信息
    if match: #如果获取到信息
        print(match.group(0))
        with open("data.txt","w") as f: #将WiFi信息写入data.txt
            f.write(match.group(0))
            global choose
            choose=1
            
        
def send_html(conn): #选择要发送的HTML页面
    global choose
    if choose==0:#发送WiFi上传界面
        conn.sendall(html0)
    if choose==1:
        a=connect_wifi()
        if a==True:
            global sever 
            sever=False
            conn.sendall(html1)
        else:
            choose=0
            conn.sendall(html2)


#使用方法：若连接成功，打印接口的IP/netmask/gw/DNS地址,返回True；
#         若连接失败，返回False。
def connect_wifi():#获取data.txt的WiFi信息
    with open("data.txt","rb") as f:
        data=f.read()
    match=re.search(r"GET /\?ssid=(.*?)&password=(.*?) HTTP",data)#获取DATA.TXT中的WiFi信息
    if match:
        SSID = match.group(1)               #WiFi名称
        PASSWORD = match.group(2)           #WiFi密码
        wlan = network.WLAN(network.STA_IF)  #创建WLAN对象
        wlan.active(True)               #激活界面
        if not wlan.isconnected(): #检查站点是否连接
            print('connecting to network...')
            wlan.connect(SSID, PASSWORD)
        for i in range(6):#循环6次检查是否连接成功(6秒内是否连接成功)
            time.sleep(1) #延时1秒
            if wlan.isconnected():#检查站点是否连接
                print('network config:', wlan.ifconfig())#获取接口的IP/netmask/gw/DNS地址
                return True
            while i==5:#i=5之前未跳出循环则连接失败
                print('连接失败，请重新上传WiFi信息')
                return False
    else:
        return False












