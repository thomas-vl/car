# Written in python3

# Libraries
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
google cloud SDK
```
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

google cloud vision
```
...
```

