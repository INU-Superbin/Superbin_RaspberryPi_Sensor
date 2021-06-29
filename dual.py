import RPi.GPIO as gpio
import time

print("start")

#str_pin = 20
#spd_pin = 21

rig_trig = 13
rig_echo = 16

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#gpio.setup(str_pin, gpio.OUT)
#gpio.setup(spd_pin, gpio.OUT)

gpio.setup(rig_trig, gpio.OUT)

gpio.setup(rig_echo, gpio.IN)



def dist(trig, echo):
    global srt, end
    
    gpio.output(trig, False)
    time.sleep(0.5)
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)
    
    while gpio.input(echo) == 0 :
        srt = time.time()
    while gpio.input(echo) == 1:
        end = time.time()
        
        
    puls_drtn = end - srt
    distance = puls_drtn * 17000
    distance = round(distance, 2)
    if distance > 50 :
        distance = 50
        
        
while True :
    rig_dist = dist(rig_trig, rig_echo)
    print(rig_dist)
    #print("rig_Distance : {} cm".format(rig_dist))