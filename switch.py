from machine import Pin
from time import sleep_ms

pin=[16,5,4,0]#对应IN1到 IN4的GPIO引脚
Pin_All=[Pin(p,Pin.OUT) for p in pin]# 不要用GPIO1 否则模块会卡死-_-

speed=3

def SteperWriteData(data):
    count=0
    for i in data:
        Pin_All[count].value(i)
        count+=1
        
 
def SteperFrontTurn():
    global speed
     
    SteperWriteData([1,0,0,0])
    sleep_ms(speed)
 
    SteperWriteData([1,1,0,0])
    sleep_ms(speed)
 
    SteperWriteData([0,1,0,0])
    sleep_ms(speed)
     
    SteperWriteData([0,1,1,0])   
    sleep_ms(speed)
    
    SteperWriteData([0,0,1,0])
    sleep_ms(speed)
 
    SteperWriteData([0,0,1,1])
    sleep_ms(speed)
 
    SteperWriteData([0,0,0,1])
    sleep_ms(speed)
     
    SteperWriteData([1,0,0,1])   
    sleep_ms(speed)
     
def SteperBackTurn():
    global speed
     
    SteperWriteData([1,0,0,1])
    sleep_ms(speed)
     
    SteperWriteData([0,0,0,1])   
    sleep_ms(speed)
     
    SteperWriteData([0,0,1,1])
    sleep_ms(speed)
 
    SteperWriteData([0,0,1,0])
    sleep_ms(speed)
    
    SteperWriteData([0,1,1,0])
    sleep_ms(speed)
 
    SteperWriteData([0,1,0,0])
    sleep_ms(speed)
 
    SteperWriteData([1,1,0,0])
    sleep_ms(speed)
     
    SteperWriteData([1,0,0,0])   
    sleep_ms(speed)
 
 
def SteperStop():
    SteperWriteData([0,0,0,0])


def motor(direction,times): #控制电机正反转
    if direction:
        for i in range(times):
            SteperFrontTurn()
        
    else:
        for i in range(times):
            SteperBackTurn()
    
    
    
    
    
    
    
    
    
    
    

