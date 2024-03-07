# IoT part of the project 🌐🚀
``` username - fyp ```
``` password - fyp ```
``` IP address - 192.168.8.158 ```
### Circuit Diagram
https://bit.ly/high-level_circuit-diagram

<img src="https://github.com/FYP-19/IoT/assets/75986133/3cce3e50-2393-4969-a2b9-c611c6560571" alt="image (2)" width="500"/>

## Used IoT Devices

| Requirement                | IoT Device                                |
|-------------------------|----------------------------------------------|
| Microcontroller    | Raspberry Pi 3B+            |
| Triggering Switch   |  Micro Switch V-1521C25  |
| Camera Module        |  Raspberry Pi NoIR v2 camera board |
| Communication Model        |  LoRa Ra-02 SX1278 |
| Antenna        |  RF 433MHz Antenna 2-3 dBi   |

## Essential Linux Commands 

| Function                | Linux Command                                |
|-------------------------|----------------------------------------------|
| Check camera status    | vcgencmd get_camera            |
| Real time camera feed   | raspivid -t 0            |
| Capture an image        |  raspistill -o <image_name>.jpg |
| Watch the image        |  eog <image_name>.jpg |
