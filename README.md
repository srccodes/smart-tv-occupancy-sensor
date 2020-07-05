# smart-tv-occupancy-sensor
Article on "IOT - Kid's Eye and Energy Safe Smart and Green TV - PoC" (https://www.srccodes.com/iot-kids-eye-safe-smart-green-tv-roku-esp32-hcsr04-hcsr501-pir-motion-ultrasonic-sensors-oled/)

This is enhancement of my last project (IOT - Kid's Eye Safe Smart TV - PoC - https://www.srccodes.com/iot-kids-eye-safe-smart-tv-roku-esp32-hcsr04-sensor-oled/).  I have added one more sensor called PIR motion sensor (HC-SR501). Dual Technology Occupancy Sensor (Ultrasonic sensor & Motion sensor) yields a very responsive and reliable solution to detect occupancy. PIR sensor detects the change of infrared radiations emitted by the subject in motion in its field of view. Perfect for my project to detect audience in front of TV. Circuit built using ESP32 will read Ultrasonic Distance Sensor (HC-SR04) and PIR Motion Sensor (HC-SR501). Based on that reading , Micropython logic will decide when to pause or start the TV by calling smart TV API (e.g. in my case Roku TV API to toggle Play/Pause  http://$ROKU_DEV_TARGET:8060/keypress/play).
In this PoC, if viewer goes very close (within preconfigured threshold 1 meter) to the TV or no viewer (no motion) detected for certain period of time (say 10 mins), TV will be paused automatically.
