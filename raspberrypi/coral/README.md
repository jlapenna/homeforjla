## Resources

## Coral Board

*   https://coral.withgoogle.com/docs/enviro-board/datasheet/
*   https://coral.withgoogle.com/docs/enviro-board/get-started/

### Python

#### Install

./raspberrypi/coral/install.sh

It adds an apt source and installs:

```
coral-enviro-drivers-dkms dkms python3-coral-cloudiot python3-jwt
python3-luma-core python3-luma-oled python3-paho-mqtt python3-smbus2
python3.5-cryptoauthlib raspberrypi-kernel-headers
```

#### Demo

```shell
cd /usr/lib/python3/dist-packages/coral/enviro
python3 enviro_demo.py
```
                                                                                                                                       
### GCP

#### Setup

https://cloud.google.com/iot/docs/

## Grove Moisture Sensor

*   http://wiki.seeedstudio.com/Grove-Moisture_Sensor/
