# Written in python3

# Libraries
Open CV: http://opencv.org/

picamera: http://picamera.readthedocs.io/en/release-1.11/

wiringpi: https://github.com/WiringPi/WiringPi-Python
```
git clone --recursive https://github.com/WiringPi/WiringPi-Python.git
cd WiringPi-Python
git submodule update --init
sudo apt-get install python3-dev python3-setuptools swig3.0
cd WiringPi
sudo ./build
Return to the root directory of the repository and:
swig3.0 -python wiringpi.i
sudo python3 setup.py install
```
