from machine import Pin
import dht
d = dht.DHT11(Pin(14))
d.measure()
print(d.humidity())
print(d.temperature())
