import time, os, sys
import wiringpi as io


class light(object):
    def __init__(self, pin):
        #make pins into output
        io.pinMode(pin,1)
        #set output low
        io.digitalWrite(pin,0)
        #set variables
        self.status = 0
        self.pin = pin

    def on(self):
        #turn light on
        io.digitalWrite(self.pin,1)
        self.status = 1

    def off(self):
        io.digitalWrite(self.pin,0)
        self.status = 0

    def blink(self,times):
        for _ in times:
            self.on()
            time.sleep(2)
            self.off()
            time.sleep(2)

#initialise
try:
    io.wiringPiSetupGpio()
except:
    print "GPIO issue", sys.exc_info()[0]

lightFL = light(21)
lightFL.on()

lights = {
    "LeftFront":{"pin":21,"status":0},
    "RightFront":{"pin":16,"status":0}
    }

def lightCtrl(names,status):
    for i in names:
        io.digitalWrite(lights[i]["pin"],status)
        lights[i]["status"] = status

def initResource():
    try:
        io.wiringPiSetupGpio()
    except:
        print "GPIO issue", sys.exc_info()[0]
    for key, value in lights.items():
        #make pins into output
        io.pinMode(value["pin"],1)
        #set output low
        io.digitalWrite(value["pin"],0)

def lightTest():
    lightCtrl(["LeftFront"],1)
    time.sleep(3)
    lightCtrl(["LeftFront"],0)
    lightCtrl(["RightFront"],1)
    time.sleep(3)
    lightCtrl(["RightFront"],0)
    time.sleep(1)
    lightCtrl(["LeftFront","RightFront"],1)
    time.sleep(3)
    lightCtrl(["LeftFront","RightFront"],0)

#initResource()
#lightTest()
