import time, os, sys, threading
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
        #turn light off
        io.digitalWrite(self.pin,0)
        self.status = 0

    def blinkWorker(self,pause):
        #frits: ik ben er vrij zeker van dat dit met minder code kan.
        if (self.status == 0):
            self.on()
            time.sleep(pause)
            self.off()
            time.sleep(pause)
        else:
            self.off()
            time.sleep(pause)
            self.on()
            time.sleep(pause)

    def blinkThread(self):
        for _ in range(self.times):
            self.blinkWorker(0.5)

    def blink(self,times):
        self.times = times
        #Dit is een example voor threading omdat ik deze functie async wil laten lopen misschien moet het wat schoon gemaakt worden
        #meer info over threading: https://pymotw.com/2/threading/
        t = threading.Thread(target=self.blinkThread)
        t.start()

#initialise GPIO
try:
    io.wiringPiSetupGpio()
except:
    print "GPIO issue", sys.exc_info()[0]

#FL = FrontLeft, FR = FrontRight
lightFL = light(21)
lightFR = light(16)
lightFL.blink(5)
lightFR.on()
lightFR.blink(4)
time.sleep(3)
lightFR.off()
