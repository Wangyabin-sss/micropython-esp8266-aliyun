from simple import MQTTClient
from machine import Pin,Timer
import network
import dht
import switch
import time
import re

#根据实际情况填写
SERVER ='a1XXXXXXXXX.iot-as-mqtt.cn-shanghai.aliyuncs.com'  #MQTT Server
CLIENT_ID = "12345|securemode=3,signmethod=hmacsha1|"   #设备ID
#PORT=1883
username='devicel1&a1XXXXXXXXX'
password='2DXXXXXXXXXXXXXXXX3A62C1XXXXXF43A92C54'
 
publish_TOPIC = '/sys/a1XXXXXXXXX/devxxxx/thing/event/property/post'
subscribe_TOPIC ='/sys/a1XXXXXXXXX/devxxxx/thing/service/property/set'

client=None


led = Pin(2, Pin.OUT, value=0) #led
p12 = Pin(12, Pin.OUT) #水泵
p13 = Pin(13, Pin.OUT) #风扇
p15 = Pin(15, Pin.OUT) #遮阳布
data = dht.DHT11(Pin(14))


def Dataupload(timer):
    try:
        data.measure()
        print(data.humidity())
        message='{"id": "12345","version": "1.0","params": {"SwitchStatus": {"value": %d,},"Temperature": {"value": %d,},"Humidity": {"value": %d,},"IrrigationPump": {"value": %d,},"exhaustfan": {"value": %d,},"Shadecloth": {"value": %d,}},"method": "thing.event.property.post"}'%(led.value(),data.temperature(),data.humidity(),p12.value(),p13.value(),p15.value())
 #       print(message)
        client.publish(topic=publish_TOPIC,msg= message, retain=False, qos=0)
        
    except Exception as ex_results2:
        print('exception2',ex_results2)
        timer.deinit()
        
    
def sub_cb(topic, msg):
 #   print((topic, msg))
    dic=msg.decode()
    print(dic)
    refind(dic)

    
def refind(dicc):
    match0=re.search(r"{\"SwitchStatus\":(.*?)}",dicc)#获取DATA.TXT中的灯的开关信息
    if match0:
        value0=eval(match0.group(1))
        led.value(value0)
        
    match1=re.search(r"{\"IrrigationPump\":(.*?)}",dicc)#获取水泵的开关信息
    if match1:
        value1=eval(match1.group(1))
        p12.value(value1)
        
    match2=re.search(r"{\"exhaustfan\":(.*?)}",dicc)#获取排风扇的开关信息
    if match2:
        value2=eval(match2.group(1))
        p13.value(value2)
        
    match3=re.search(r"{\"Shadecloth\":(.*?)}",dicc)#获取遮阳布的开关信息
    if match3:
        value3=eval(match3.group(1))
        p15.value(value3)
        switch.motor(value3,512)
        

try:
#     data = dht.DHT11(Pin(14))
    client = MQTTClient(CLIENT_ID, SERVER,0,username,password,60)
    print(client)
    client.set_callback(sub_cb)
    client.connect()                                    #connect mqtt
    client.subscribe(subscribe_TOPIC)
    print("Connected to %s, subscribed to %s topic" % (SERVER, subscribe_TOPIC))
    timer=Timer(0)
    timer.init(mode=Timer.PERIODIC, period=5000,callback=Dataupload)
    while True:
        client.wait_msg()
        
except Exception as ex_results:
    print('exception1',ex_results)
    
finally:
    if(client is not None):
        client.disconnect()













