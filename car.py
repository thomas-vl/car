from bluetooth import *
import time, os, sys, threading, picamera, git, subprocess, uuid
import wiringpi


class motorClass(object):
    def __init__(self):
        self.status = ""
        self.pwmPin = 18
        self.forwardPin = 17
        self.backwardPin = 4
        self.speed = 50
        wiringpi.pinMode(self.forwardPin,1)
        wiringpi.pinMode(self.backwardPin,1)
        wiringpi.pinMode(self.pwmPin,1)
        wiringpi.softPwmCreate(self.pwmPin,0,100)

    def forward(self):
        wiringpi.softPwmWrite(self.pwmPin,self.speed)
        wiringpi.digitalWrite(self.forwardPin,1)
        wiringpi.digitalWrite(self.backwardPin,0)
        self.status = "f"

    def backward(self):
        wiringpi.softPwmWrite(self.pwmPin,self.speed)
        wiringpi.digitalWrite(self.forwardPin,0)
        wiringpi.digitalWrite(self.backwardPin,1)
        self.status = "b"

    def setSpeed(self, speedInt):
        wiringpi.softPwmWrite(self.pwmPin,speedInt)
        self.speed = speedInt

    def stop(self):
        wiringpi.digitalWrite(self.forwardPin,0)
        wiringpi.digitalWrite(self.backwardPin,0)
        self.status = ""

    def getStatus(self):
        return self.status

class steerClass(object):
    def __init__(self):
        self.status = ""
        self.enablePin = 25
        self.leftPin = 24
        self.rightPin = 23
        wiringpi.pinMode(self.enablePin,1)
        wiringpi.pinMode(self.leftPin,1)
        wiringpi.pinMode(self.rightPin,1)

    def left(self):
        wiringpi.digitalWrite(self.enablePin,1)
        wiringpi.digitalWrite(self.leftPin,0)
        wiringpi.digitalWrite(self.rightPin,1)
        self.status = "l"
        camera.picture()

    def right(self):
        wiringpi.digitalWrite(self.enablePin,1)
        wiringpi.digitalWrite(self.leftPin,1)
        wiringpi.digitalWrite(self.rightPin,0)
        self.status = "r"
        picture.picture()

    def straight(self):
        wiringpi.digitalWrite(self.enablePin,0)
        self.status = ""

    def getStatus(self):
        return self.status

class cameraClass(object):
    def __init__(self):
        #initialise camera
        self.camera = picamera.PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (640, 480)
        self.camera.start_preview()
        t = threading.Thread(name='cameraThread',target=self.worker)
        t.start()

    def worker(self):
        while True:
            if steer.getStatus() == "" and motor.getStatus() != "":
                self.picture()
            time.sleep(1)

    def picture(self):
        folder = motor.getStatus()+steer.getStatus()
        print("folder:" + folder)
        uid_str = uuid.uuid1().urn[9:]
        filename = folder+'/'+uid_str+'.jpg'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.camera.capture(filename)

class crashSensor(object):
    def __init__(self):
        self.pin = 16
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
        lightFL.blink(2)
        lightFR.blink(2)

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

class btClass(object):
    def __init__(self):
        self.addr = "9C:65:B0:78:51:C4"
        self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
        t = threading.Thread(name='bt',target=self.connect)
        t.start()

    def connect(self):
        service_matches = ""
        while len(service_matches) == 0:
            service_matches = find_service( uuid = self.uuid, address = self.addr )
            time.sleep(10)

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        self.sock=BluetoothSocket( RFCOMM )
        self.sock.connect((host, port))
        self.drive()

    def drive(self):
        try:
            while True:
                data = self.sock.recv(1024)
                if data == b'forward':
                    motor.forward()
                    motor.setSpeed(70)
                if data == b'backward':
                    motor.setSpeed(70)
                    motor.backward()
                if data == b'idle':
                    motor.stop()
                if data == b'left':
                    steer.left()
                if data == b'right':
                    steer.right()
                if data == b'straight':
                    steer.straight()
                if data == b'reboot':
                    command = "/sbin/shutdown -r now"
                    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                    output = process.communicate()[0]

        except:
            self.connect()


def cameraTest():
    camera.picture()

def lightTest():
    lightFL.on()
    lightFR.on()
    time.sleep(2)
    lightFL.off()
    lightFR.off()

def crashTest():
    crashS.check()

def motorTest():
    motor.forward()
    time.sleep(2)
    motor.backward()
    time.sleep(2)
    motor.forward()
    steer.right()
    time.sleep(1)
    steer.straight()
    time.sleep(1)
    motor.stop()

#g = git.cmd.Git()
#print(g.pull())

try:
    wiringpi.wiringPiSetupGpio()
except:
    print ("GPIO issue", sys.exc_info()[0])

lightFL = light(26)
lightFR = light(20)
crashS = crashSensor()
motor = motorClass()
steer = steerClass()
camera = cameraClass()
bt = btClass()

test = input('What do you want to test:(light,camera,crash)')
if (test == "light"):
    lightTest()
if (test == "camera"):
    cameraTest()
if (test == "crash"):
    crashTest()
if (test == "motor"):
    motorTest()
