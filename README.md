# Christmas Lights Client

This repository contains the client code to display patterns on a strip of WS2812b LEDs from a raspberry pi zero 2w. This repo is a sister repo of the [ChristmasLightsServer](https://github.com/Stephen-Hallett/ChristmasLights) repository which hosts the server.

## Required hardware
- Rasbpberry pi zero (or better)
- USB microphone w/ adapter to connect (If you want sound responsive lights)
- Micro-USB cable for power
- WS2812b LED strip

## Hardware setup
First plug in all USB cables to the raspberry pi, then connect the WS2812b LED strip as follows:

- Power (red) -> 5v pin
- Signal (green) -> pin 18 (This pin has PWM)
- Ground (white) -> Ground pin

![Raspberry pi pinout](./media/raspberrypi_pinout.png)

#### Optional
3D print the case provided in the PiZeroCase directory.

## Software setup
The following setup instructions assume you are using a debian based operating system. This has only been tested on a raspberry pi zero2w running Rasbian lite 64 bit.


**Clone repository**
```sh
cd #Setup assumes you are in base directory
git clone https://github.com/Stephen-Hallett/ChristmasLightsClient.git
```

**Install python**
```sh
sudo apt update
sudo apt install python3 python3-pip
```

**Install port audio (skip if not using a microphone)**
```sh
sudo apt install portaudio19-dev
```

**Make virtual environment and install packages**
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Run client script**
```sh
python ChristmasClient.py
```

#### Optional  
**Enable run on startup with crontab**
```sh
crontab -e
```
Paste the following:
```sh
@reboot ~/ChristmasLightsClient/.venv/python ~/ChristmasLightsClient/ChristmasClient.py
```