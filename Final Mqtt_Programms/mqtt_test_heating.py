import network
import time
import ubinascii
from umqtt.simple import MQTTClient
from machine import Pin
import micropython
import socket
import machine

p2 = machine.Pin(4)
pwm2 = machine.PWM(p2)

p5 = machine.Pin(14)
pwm5 = machine.PWM(p5)

p6 = machine.Pin(12)
pwm6 = machine.PWM(p6)

p8 = machine.Pin(15)
pwm8 = machine.PWM(p8)

heatarray = [pwm8,pwm6,pwm5,pwm2]
beginningvalue = 400
beginningvalue_small = 200

SERVER = "192.168.200.117"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"topic/test"
newmessage = False

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.ifconfig(('192.168.200.77','255.255.255.0','192.168.200.1','8.8.8.8'))
        sta_if.connect('Labs-Guest', 'L-G@UDK4GJ2015')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    ap_if.active(False)

do_connect()

def sub_cb(topic, msg):
    print((topic, msg))
    global newmessage
    
    if msg == b"on":
        heatarray[0].duty(beginningvalue+150)
        heatarray[1].duty(beginningvalue+250)
        heatarray[2].duty(beginningvalue+350)
        heatarray[3].duty(beginningvalue+400)
        #a = 1
        print('TURN LED0 ON')
    if msg == b"off":
    	for i in heatarray:
    		i.duty(0)
        beginningvalue = 400
    if msg == b"heat_small":
        heatarray[0].duty(beginningvalue_small+150)
        heatarray[1].duty(beginningvalue_small+250)
        heatarray[2].duty(beginningvalue_small+350)
        heatarray[3].duty(beginningvalue_small+400)
        #a = 3
    if msg == b"heat_first":
        #a = 4
        heatarray[0].duty(100)
        heatarray[1].duty(beginningvalue+250)
        heatarray[2].duty(beginningvalue+350)
        heatarray[3].duty(100)
    if msg == b"heat_second":
        #a = 4
        heatarray[0].duty(beginningvalue+150)
        heatarray[1].duty(100)
        heatarray[2].duty(100)
        heatarray[3].duty(beginningvalue+400)


def main(server=SERVER):
    global newmessage
    do_connect()
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    try:
        while 1:
            #micropython.mem_info()
            c.check_msg()
            time.sleep(1)

    finally:
		c.disconnect()

main()
