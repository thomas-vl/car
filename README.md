# Libraries
Open CV: http://opencv.org/

picamera: http://picamera.readthedocs.io/en/release-1.11/

wiringpi: https://github.com/WiringPi/WiringPi-Python
```
git clone --recursive https://github.com/WiringPi/WiringPi-Python.git
cd WiringPi-Python
git submodule update --init
sudo apt-get install python-dev python-setuptools swig
cd WiringPi
sudo ./build
Return to the root directory of the repository and:

swig2.0 -python wiringpi.i

or

swig3.0 -thread -python wiringpi.i

##Build & install with

sudo python setup.py install

Or Python 3:

sudo python3 setup.py install
```
