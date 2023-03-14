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
mqtt_broker = 'MY IP HERE' 
topic_sub = 'myLaptop'
topic_pub = 'lego'
client_id = 'Sloans Laptop'


readIn=''
isNew=False #this is just so I can check if there is new data
mqtt_CBR.connect_wifi(wifi)
startedwifi()

#values obtained from inverse kinematics code
theta1_angles=[39.574951470122166, 35.80011456649873, 32.17103986542873, 28.68321148649983, 25.329929635849545, 22.10259185597818, 18.991013502339044, 15.983761067396575, 13.068476181644359, 10.232173653126704, 7.461502744995615, 4.742966260794741, 2.0630964426106475, -0.5914099927229334, -3.233593112848229, -5.876161424079883, -8.531447361041925, -11.211379827175287, -13.927466992659225, -16.6907825819041, -19.511948798969307, -22.401108735179818, -25.367880495050194, -28.421284304157005, -31.569632491856375, -34.820370478153585, -38.179854812139425, -41.653052108462894, -45.24314082703898, -48.95099702924729, -52.77454690693083, -56.70797530071777, -60.74079410270937, -64.85680224536591, -69.03301563839109, -73.2387153497451, -77.43485337354443, -81.57414924145417, -85.60226168260502, -89.46035136809387]
theta2_angles=[138.92465112559796, 139.70062737253573, 140.37820347400248, 140.96766418800135, 141.4795035403989, 141.9242805446431, 142.31247545913212, 142.65435472519712, 142.95985062855328, 143.23845942867757, 143.49915952492927, 143.7503493982415, 143.9998036939228, 144.25464490789338, 144.5213276501919, 144.80563229333006, 145.11266486567223, 145.4468602249055, 145.81198576330897, 146.2111430930872, 146.64676529198982, 147.1206073263481, 147.63372719071154, 148.1864550990833, 148.77834772942288, 149.40812407009537, 150.07357887602723, 150.77146918692821, 151.4973689397262, 152.24548670541952, 153.00844250167688, 153.77700232609962, 154.539774854948, 155.28288555785514, 155.98966157630585, 156.64038791560165, 157.21223096057756, 157.6794615101929, 158.01412724290287, 158.18729166280227]
#keeping track of x values as well as theta values so that I know when to turn on the light for each phase
x_vals=[-7.6, -7.473, -7.346, -7.219, -7.092, -6.965, -6.838, -6.711, -6.584, -6.457, -6.33, -6.203, -6.076, -5.949, -5.822, -5.695, -5.568, -5.441, -5.314, -5.187, -5.06, -4.933, -4.806, -4.679, -4.552, -4.425, -4.298, -4.171, -4.044, -3.917, -3.79, -3.663, -3.536, -3.409, -3.282, -3.155, -3.028, -2.901, -2.774, -2.647, -2.52, -2.393, -2.266, -2.139, -2.012, -1.885, -1.758, -1.631, -1.504, -1.377, -1.25, -1.123, -0.996, -0.869, -0.742, -0.615, -0.488, -0.361, -0.234, -0.107, 0.02, 0.147, 0.274, 0.401, 0.528, 0.655, 0.782, 0.909, 1.036, 1.163, 1.29, 1.417, 1.544, 1.671, 1.798, 1.925, 2.052, 2.179, 2.306, 2.433, 2.56, 2.687, 2.814, 2.941, 3.068, 3.195, 3.322, 3.449, 3.576, 3.703, 3.83, 3.957, 4.084, 4.211, 4.338, 4.465, 4.592, 4.719, 4.846, 4.973]

def move():#this sends all my angles to the robot and to my computer which then sends
    #them to adafruit
    phase1()
    for i in len(theta1_angles):
        if i==10:
            phase2()
        if i==20:
            phase3()
        angel=mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
        adaPub='angleCur '+str(theta1_angles[i])+' '+str(theta2_angles[i])
        legoPub=[float(theta1_angles[i]),float(theta2_angles[i])]
        angel.publish('myLaptop', adaPub)
        angel.publish(topic_pub, legoPub)
        time.sleep(1)
    phase4()

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