import time, os, sys
import wiringpi as io

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

initResource()
lightTest()

