import time, os, sys, threading, picamera
import wiringpi


class car(object):
    def __init__(self):
        #initialise GPIO
        try:
            wiringpi.wiringPiSetupGpio()
        except:
            print ("GPIO issue", sys.exc_info()[0])

    class camera(object):
        def __init__(self):
            #initialise camera
            self.camera = picamera.PiCamera()
            self.camera.resolution = (1024, 768)
            self.camera.start_preview()

        def picture(self):
            self.camera.capture('image.jpg')

    class crashSensor(object):
        def __init__(self):
            self.pin = 24
            self.alive = True
            wiringpi.pinMode(self.pin,0)
            wiringpi.pullUpDnControl(self.pin,2)

        def crashWorker(self):
            while self.alive:
                state = wiringpi.digitalRead(self.pin)
                if state == 0:
                    self.crash()
                    self.alive = False

        def check(self):
            t = threading.Thread(name='crash',target=self.crashWorker)
            t.start()

        def crash(self):
            c.lightFL.blink(2)
            c.lightFR.blink(2)


    class light(object):
        def __init__(self, pin):
            #make pins into output
            wiringpi.pinMode(pin,1)
            #set output low
            wiringpi.digitalWrite(pin,0)
            #set variables
            self.status = 0
            self.pin = pin

        def on(self):
            #turn light on
            wiringpi.digitalWrite(self.pin,1)
            self.status = 1

        def off(self):
            #turn light off
            wiringpi.digitalWrite(self.pin,0)
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
            t = threading.Thread(name='light',target=self.blinkThread)
            t.start()


def cameraTest():
    c.cam.picture()

def lightTest():
    c.lightFL.on()
    c.lightFR.on()
    time.sleep(2)
    c.lightFL.off()
    c.lightFR.off()

def crashTest():
    c.crashS.check()

c = car()
c.lightFL = c.light(26)
c.lightFR = c.light(20)
c.crashS = c.crashSensor()
c.cam = c.camera()

test = input('What do you want to test:(light,camera,crash)')
if (test == "light"):
    lightTest()
if (test == "camera"):
    cameraTest()
if (test == "crash"):
    crashTest()
