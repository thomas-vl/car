
import time, os, sys, threading, picamera
import wiringpi

try:
    wiringpi.wiringPiSetupGpio()
except:
    print ("GPIO issue", sys.exc_info()[0])

wiringpi.pinMode(4,OUTPUT)
wiringpi.pinMode(17,OUTPUT)
wiringpi.pinMode(18,PWM_OUTPUT)

print("spinning!\n")
wiringpi.pwmWrite(18,50)
wiringpi.digitalWrite(4,HIGH)
wiringpi.digitalWrite(17,LOW)

time.sleep(3)
print("stopping\n")
wiringpi.digitalWrite(4,LOW)
wiringpi.digitalWrite(17,LOW)
