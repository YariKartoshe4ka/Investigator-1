# Guide

1. [Preparing](#preparing)
    - [Getting components](#getting-components)
    - [Setup Arduino IDE](#arduino-ide)
        - [ESP32-CAM](#esp32-cam)
        - [Arduino Uno](#arduino-uno)
2. [Building](#building)
    - [Flashing ESP32-CAM](#flashing-esp32-cam)
    - [Configuring servo](#configuring-servo)
    - [Building](#building-1)
    - [Flashing Arduino Uno](#flashing-arduino-uno)
3. [Managing](#managing)
    - [API](#api)
    - [iClient](#iclient)



# Preparing

### Getting components

I ordered all the components on AliExpress. This is full price-list of it:

- [Arduino Uno R3](components/arduino_uno_r3.jpg) \~4.5$
- [ESP32-CAM](components/esp32-cam.jpg) \~5$
- [Chassis](components/chassis.jpg) \~7$
- [Wires F-M 20sm](components/wires_f-m_20sm.jpg) \~1$
- [Wires M-M 20sm](components/wires_m-m_20sm.jpg) \~1$
- [L298N motor driver](components/l298n_motor_driver.jpg) \~1.5$
- [SG90](components/sg90.jpg) (180-degree only!) \~1.2$
- [BreadBoard mini](components/breadboard_mini.jpg) \~0.5$
- [18650 battery](components/18650_battery.jpg) \~2.5$ (if you have got small power bank, you can use it instead of this)
- [Case for 18650 battery](components/case_for_18650_battery.jpg) \~1$ (if you have got small power bank, you can use it instead of this)
- [Leds](components/leds.jpg) \~1$
- [USB A to USB B wire](components/wire_usb_a_to_usb_b.jpg) =$0 (included in arduino uno)
- [Toggle switch button](components/toggle_switch_button.jpg) =0$ (included in chassis)

Full price is: \~41.5$

### Setup Arduino IDE

###### ESP32-CAM

I found [easy guide](https://www.youtube.com/watch?v=0LIhTLsOLbA) how configure Arduino IDE for ESP32-CAM. Now you only need install ESP32-CAM library<br>

###### Arduino Uno

You only need to install the L298N library from [here](https://github.com/AndreaLombardo/L298N)



# Building

### Flashing ESP32-CAM

1. Open [this sketch](../../arduino/esp32-cam/esp32-cam.ino)
2. Replace `********` with SSID and password of your WiFi
```cpp
...

  const char* ssid = "*********";
  const char* password = "********";

...
```
3. Load it with [previous guide](#esp32-cam) on youtube<br>
This is schema for flashing ESP32-CAM

<img src="../schema/esp32-cam_uno.png">



### Configuring servo

Connect servo motor to Arduino Uno with this schema

<img src="../schema/servo_uno.png">

and load [this sketch](../../arduino/servo/servo.ino). It will move servo to 0°. Then put servo on chassis with this schema

<img src="../schema/servo_chassis.png">



### Building

Now you can build robot with this schema

<img src="../schema/full.png">

On the chassis, I arranged everything like this

<img src="">


### Flashing Arduino Uno


Open [this sketch](../../arduino/arduino-uno/arduino-uno.ino) and load it to Arduino Uno<br>
Now you need to make sure that WiFi network is working and restart the robot by turning on and off toggle switch button



# Managing

### API

Robot is managed by sending HTTP GET requests to [http://Investigator-1/api](http://Investigator-1/api) url. The command is passed in the cmd parameter, i.e. the final url will look like this: [http://Investigator-1/api?cmd=light off](http://Investigator-1/api?cmd=light%20off). The request is processed by ESP32-CAM and sent to the Arduino Uno via Serial. Arduino, in turn, processes the command by simple if-else comparisons and executes it. A table of all commands by default:

<table>
  <tr>
    <th>Command</th>
    <th>Argument</th>
    <th>Description</th>
    <th>Default value</th>
  </tr>

  <!-- motor command section -->
  <tr>
    <td rowspan="3">motor</td>
    <td>forward</td>
    <td>Set a forward movement</td>
    <td rowspan="3">stop</td>
  </tr>

  <tr>
    <td>backward</td>
    <td>Set a backward movement</td>
  </tr>

  <tr>
    <td>stop</td>
    <td>Stop a movement</td>
  </tr>
  
  <!-- direction command section -->
  <tr>
    <td rowspan="3">direction</td>
    <td>left</td>
    <td>Turn to the left</td>
    <td rowspan="3">stop</td>
  </tr>

  <tr>
    <td>right</td>
    <td>Turn to the right</td>
  </tr>

  <tr>
    <td>stop</td>
    <td>Drive straight</td>
  </tr>

  <!-- camera command section -->
  <tr>
    <td rowspan="3">camera</td>
    <td>up</td>
    <td>Turn the camera up</td>
    <td rowspan="3">stop</td>
  </tr>

  <tr>
    <td>down</td>
    <td>Turn the camera down</td>
  </tr>

  <tr>
    <td>stop</td>
    <td>Stop camera movement</td>
  </tr>

  <!-- light command section -->
  <tr>
    <td rowspan="2">light</td>
    <td>on</td>
    <td>Turn on the headlights</td>
    <td rowspan="2">off</td>
  </tr>

  <tr>
    <td>off</td>
    <td>Turn off the headlights</td>
  </tr>

  <!-- speed command section -->
  <tr>
    <td>speed</td>
    <td>0&hellip;255</td>
    <td>Set 0&hellip;255 motor speed</td>
    <td>0</td>
  </tr>
</table>


### iClient

To easy control the robot you can install [iClient](../../client) (wrapper for Investigator-1 commands API, was written by me too).

