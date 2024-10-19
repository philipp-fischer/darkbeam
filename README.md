# Darkbeam

Darkbeam is a little projector box with WiFi. Put it next to your bed to project the date and time to your ceiling or wall at night. 
To see how you can build one yourself, go to https://www.printables.com/model/1043928-darkbeam-the-smart-nighttime-projector-v3

This repository contains the example firmware and software to operate Darkbeam.
There are currently two tested options: **ESPHome** and **micropython**.

## Use with ESPHome

Using an ESPHome-based firmware is the simpler but slightly more limited option. 

#### Precompiled firmware
If you don't have any server at home and no home assistant installation, and all you want to do is display the date and time, then the pre-compiled image `example-date-time.factory.bin` might be sufficient for you.

1. Connect Darkbeam to your computer using a USB cable
2. Go to https://web.esphome.io/
3. If you're flahsing it for the first time, select "Prepare for first use"
4. When done, select "Close" then "Install" and upload the firmware image from this repository (`esphome/example-date-time.factory.bin`)
5. Once it is done with flashing you should already see some text displayed on the OLED
6. Wait for 1 minute until the WiFi Hotspot "Darkbeam Fallback Hotspot" appears and connect to it using the password "d4rkb34m!"
7. You should be redirected to a captive portal where you can select the WiFi network and the password to use
8. Once set, Darkbeam should use the WiFi connection to obtain the correct date and time from an NTP server

#### Build your own firmware
The `esphome/example-date-time.yaml` is the configuration that was used to build the firmware file mentioned above.
If you plan to build your own firmware, you'll need either Home Assistant with the ESPHome Add-on or a standalone ESPHome installation (like the [pre-built docker image](https://esphome.io/guides/getting_started_command_line.html))

When you customize the yaml file, you should adapt the wifi ssid and password so that the captive portal is not needed.
In the display lambda you can change the drawing code and plot arbitrary text and shapes. Take a look at [this page](https://esphome.io/components/display/index.html) to see what you can do.

If you are using Darkbeam with Home Assistant, you can also display the value of a sensor in your home or the weather forecast etc. Be creative and feel free to contribute your code to this repository!


## Use with micropython
The advantage of using the micropython firmware is that you are not limited to the drawing routines that the ESPHome display component provides.
You'll be able to change the display brightness and other settings on the fly without re-flashing the firmware.
When implemented as a streaming device, you can stream arbitrary image and video content to Darkbeam at a rather high framerate. I managed to show a little video in real-time.

The drawback may be that it's harder to interface with Home Assistant. You'll need your own little script running on some computer in your network, transmitting frame data to Darkbeam.

Right now, I don't have step-by-step instructions for this path. Let me know if you can't figure it out.
In the `micropython/` folder I provide the `payload.py` script which you should upload to the controller after installing micropython. Make sure it's executed after boot.

On the other end, run the `client.py` script which transmits the frame data to Darkbeam via UDP. The UDP packet bytes start with one byte for the brightness (0-255) and the remaining bytes following the SSD1306-internal pixel buffer format.
