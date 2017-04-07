
import time, os, sys, threading, picamera
import wiringpi

try:
    wiringpi.wiringPiSetupGpio()
except:
    print ("GPIO issue", sys.exc_info()[0])

wiringpi.pinMode(4,1)
wiringpi.pinMode(17,1)
wiringpi.pinMode(18,2)

print("spinning!\n")
wiringpi.pwmWrite(18,50)
wiringpi.digitalWrite(4,1)
wiringpi.digitalWrite(17,0)

time.sleep(3)
print("stopping\n")
wiringpi.digitalWrite(4,0)
wiringpi.digitalWrite(17,0)
