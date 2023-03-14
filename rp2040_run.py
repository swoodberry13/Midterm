import time 
from machine import Pin, I2C
from secrets import Tufts_eecs as wifi
import mqtt_CBR
import sys


led11 = Pin(6, Pin.OUT)
led12 = Pin(19, Pin.OUT)
led21 = Pin(25, Pin.OUT)
led22 = Pin(15, Pin.OUT)
led31 = Pin(4, Pin.OUT)
led32 = Pin(7, Pin.OUT)
led41 = Pin(21, Pin.OUT)
led42 = Pin(20, Pin.OUT)

def myled(lednum, on_off):
    if lednum==4:
        led41.value(on_off)
        led42.value(on_off)
    if lednum==41:
        led41.value(on_off)
    if lednum==42:
        led42.value(on_off)
        
    if lednum==3:
        led31.value(on_off)
        led32.value(on_off)
    if lednum==31:
        led31.value(on_off)
    if lednum==32:
        led32.value(on_off) 
     
    if lednum==2:
        led21.value(on_off)
        led22.value(on_off)
    if lednum==21:
        led21.value(on_off)
    if lednum==22:
        led22.value(on_off)
        
    if lednum==1:
        led11.value(on_off)
        led12.value(on_off)
    if lednum==11:
        led11.value(on_off)
    if lednum==12:
        led12.value(on_off)

def stop():
    for i in range(5):
        myled(i,0)
def AllOn():
    for i in range(5):
        myled(i,1)               
def blink():
    stop()
    time.sleep(.5)
    AllOn()
    time.sleep(.5)
    stop()
    time.sleep(.3)
def changeMultiple(arr,sleeptime,on_or_off):#changes multiple leds to on or off
    #either with a timer in bettween them or all at the same time
    if sleeptime==0:
        for i in arr:
            myled(i, on_or_off)
            time.sleep(sleeptime)
    else:
        for i in arr:
            myled(i, on_or_off)
            time.sleep(sleeptime)
def endWalking():#this runs when the 
    changeMultiple([12,22,31,41], 0, 1)
    time.sleep(.5)
    stop()
    changeMultiple([32,42,11,21], 0, 1)
    time.sleep(.5)
    stop()
def startUp():
    blink()
    stop()
    changeMultiple([12,21,32,41], .25, 1)
    changeMultiple([42,31,22,11], .25, 1)
    blink()
def startedwifi():#This is what runs when the rp2040 has successfully connected to the wifi
    stop()
    changeMultiple([12,21,32,41],.25,1)
    time.sleep(.25)
    stop()
    changeMultiple([12,21,32,41],.25,1)
    time.sleep(.25)
    stop()
def subbed():
    for i in range(2):
        stop()
        changeMultiple([4,1],0,1)
        time.sleep(.4)
        stop()
        changeMultiple([3,2],0,1)
        time.sleep(.4)
        stop()
def phase1():
    stop()
    time.sleep(.3)
    myled(1,1)
def phase2():
    stop()
    time.sleep(.3) 
    changeMultiple([1,2],0,1)
def phase3():
    stop()
    time.sleep(.3) 
    changeMultiple([1,2,3],0,1)
def phase4():
    stop()
    AllOn()
mqtt_broker = '10.247.80.176' 
topic_sub = 'myLaptop'
topic_pub = 'lego'
client_id = 'Sloans Laptop'


readIn=''
isNew=False #this is just so I can check if there is new data
mqtt_CBR.connect_wifi(wifi)
startedwifi()

link1_angles=[77,7,9,8]
link2_angles=[77,7,9,8]
def move():#this sends all my angles to the robot and to my computer which then sends
    #them to adafruit
    for i in len(link1_angles):
        angel=mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
        adaPub='angleCur '+str(link1_angles[i])+' '+str(link2_angles[i])
        legoPub=[float(link1_angles[i]),float(link2_angles[i])]
        angel.publish('myLaptop', adaPub)
        angel.publish(topic_pub, legoPub)
        time.sleep(1)
def demo():#this demos all of my led functions
    print('DEMO OF BLINK')
    blink()
    time.sleep(2)
    print('DEMO OF STARTUP')  
    startUp()
    time.sleep(2)
    print('DEMO OF WIFI CONNECT')
    startedwifi()
    time.sleep(2)
    print('DEMO OF SUBBED')
    subbed()
    time.sleep(2)
    print('DEMO OF PHASE LIGHT UP')
    phase1()
    time.sleep(.2)
    phase2()
    time.sleep(.2)
    phase3()
    time.sleep(.2)
    phase4()
    time.sleep(.4)
    phase3()
    time.sleep(.2)
    phase2()
    time.sleep(.2)
    phase1()
    time.sleep(.2)
    stop()
    time.sleep(2)
    print('DEMO OF END WALKING')
    endWalking()
    time.sleep(2)
def decodeAngles(myString):#this parses the message from mqtt and returns an array of two floats 
    #that represent the shoulder angle and elbow angle
    #mostly used for testing
    if myString[0] != '(':
        return []
    else:
        val1 = float(myString[1:myString.find(',')])
        val2 = float(myString[myString.find(',')+1:myString.find(')')])
        return [val1,val2]  
def whenCalled(topic, msg):#decodes messages sent via mqtt and saves them to the variable readIn
    global readIn 
    global isNew
    message=msg.decode()
    if message != '':#change readIn if something is received
        readIn=message
        isNew=True
    print((topic.decode(), msg.decode()))
    time.sleep(0.5)
def main():
    global readIn
    global isNew 
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    fred.subscribe(topic_sub)
    subbed()
    started=False
    while True:
        try:
            fred.check()
            if isNew ==True:
                isNew=False
                if readIn=='stop_leg':
                    print('stopping leg')
                    endWalking()
                    sys.exit()
                if readIn=='start_leg':
                    print('starting leg')
                    startUp()
                    move()
        except OSError as e:
            print(e)
            fred.connect()
        except KeyboardInterrupt as e:
            fred.disconnect()
            print('done')
            break


main()