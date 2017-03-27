import time, os, sys, threading
import wiringpi as io


class light(object):
    threads = []

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



    def blinkWorker(self):
        if (self.status == 0):
            self.on()
            time.sleep(1)
            self.off()
            time.sleep(1)
        else:
            self.off()
            time.sleep(1)
            self.on()
            time.sleep(1)

    def blinkThread(self):
        for _ in range(self.times):
            self.blinkWorker()

    def blink(self,times):
        self.times = times
        t = threading.Thread(target=self.blinkThread)
        threads.append(t)
        t.start()

#initialise
try:
    io.wiringPiSetupGpio()
except:
    print "GPIO issue", sys.exc_info()[0]

#FL = FrontLeft, FR = FrontRight
lightFL = light(21)
lightFR = light(16)
lightFL.blink(5)
lightFR.on()
time.sleep(3)
LightFR.off()
