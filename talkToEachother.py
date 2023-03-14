from Adafruit_IO import Client, Feed, Data 
import paho.mqtt.client as mqtt 
import time

broker='MY IP HERE' 
topic_pub = 'angles'
topic_turn_on='onoroff'
topic_sub ='myLaptop'


def on_message(client, userdata, msg):
    global message_from_rp2040
    global isNew
    message_from_rp2040=msg.payload.decode()
    print(message_from_rp2040)
    isNew=True
    message_from_rp2040=str(message_from_rp2040)

ADAFRUIT_IO_KEY = "aio_Sgki72f9eCL192pBprBxh6n3vbvk"
ADAFRUIT_IO_USERNAME = "swoodberry"

aio = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)


fred=mqtt.Client('sloan')
fred.connect(broker)
fred.subscribe(topic_sub)#connect to myLaptop
fred.on_message = on_message
isOn=False


fred.loop_start()#this is so my laptop can wait for the rp2040 to send angles that it is moving to

while True:
    global isNew
    global message_from_rp2040
    isNew=False
    message_from_rp2040=''
    try:
        ada_in= aio.receive(topic_turn_on).value
        print(ada_in)#checks to see if adafruit dashboard is turned on
        
        time.sleep(4)#needs to sleep so adafruit doesn't give me a throttling error
        
        if ada_in=='leg_on' and isOn==False:
            print('turning the leg on!')
            fred.publish('myLaptop','start_leg')#tells rp2040 to start the leg
            isOn=True
    
        if isNew:#checks to see if we have a new message from the rp2040
            isNew=False
            if message_from_rp2040[0:9]=='angleCur ':#checks to see if that message is an updated angle
                cutUpMessage=message_from_rp2040[9:].split(' ')
                curAngles=str(cutUpMessage[0])+" "+str(cutUpMessage[1])
                aio.send('angles',curAngles)
        if ada_in=='leg_of' and isOn==True:
            print('turning the leg off')
            fred.publish('myLaptop','stop_leg')#tells rp2040 to stop leg
            isOn=False
        if isOn==False

        
    except KeyboardInterrupt as e:
        fred.disconnect()
        print('done')
        break




