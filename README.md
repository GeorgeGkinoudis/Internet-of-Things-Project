<h1>- IoT Motion Detection Surveillance System - </h1><br>
Overview

This project is an Internet of Things (IoT) surveillance system built using a Raspberry Pi. The system integrates motion sensors and a camera module to detect movement and automatically capture images or video footage in real time.<br>

The objective of the project was to design and implement a low-cost, event-driven smart monitoring system capable of autonomous operation.<br>

- <h1>System Architecture - </h1><br>

The system consists of:<br>

Raspberry Pi (central controller)<br>

PIR Motion Sensor (motion detection input)<br>

Raspberry Pi Camera Module (image/video capture)<br>

Software logic for event-driven automation<br>

- <h1>Workflow -</h1> <br>

PIR sensor continuously monitors movement.<br>

Motion detection signal is sent to the Raspberry Pi.<br>

Event-driven script triggers the camera module.<br>

Image or video is captured and stored locally.<br>

(Optional) Notification or remote access functionality.<br>

- <h1>Technologies Used - </h1><br>

Raspberry Pi OS<br>

Python (GPIO control & event handling)<br>

RPi.GPIO library (sensor input control)<br>

Camera module libraries (e.g., Picamera)<br>

Basic Linux configuration & terminal operations<br>

Built with ❤️ and lots of ☕
