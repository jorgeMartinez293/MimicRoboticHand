# MimicRoboticHand
A simple and fun beginner project for arduino enthusiasts to create a working mimic hand that will track your hand´s position using your webcam and replicate your movements on a robotic hand


## Project overview
- **hand_processing.py**
  - Access your camera
  - Tracks your hand and fingers position using Mediapipe
  - Calculates individual distances between the tip of your fingers and designated landmarks
  - Estimates the distance and angle between the hand and the camera using reference distances
  - Applies corrections depending on the distance and angle of the hand
  - translate the distance into centimeters to be shown when debugging
  - translate centimeters into degrees each servo should turn
  - creates a multidimensional vector featuring each angle for each finger and packages it all into a single string
  - sends this string through the indicated port into the arduino
 
- **receiver_final.ino**
    - Checks for an input, in case of:
    - Decompose the received string into five single values which are stored in an array
    - writes each value into each servo
 
## Requirements
- **Virtual enviroment provided in the repository**
    - Python 3.9
    - Mediapipe
- Arduino UNO (and a way to connect it to your computer)
- x5 microservos s90
- conectors for the servos
- Power supply 5V >1.5Amp
- usb cable to cut
- **3D robotic hand by @cmarinv2005 (youtube)**
    - https://www.thingiverse.com/thing:4807141 **(.stl files to print)**
    - https://www.youtube.com/watch?v=zDDg-aSAReo&t=878s **(assembly instructions)**
    - https://www.youtube.com/watch?v=XJluSlFzW6Q
 
## Setup
- Print and assemble the robotic hand by @cmarinv2005 (youtube)
- connect all servo´s positives to the power supply, aswell as the ground, making sure you share it with the arduino GND
- connect servos to pins from 2 to 6 on the board
- upload the .ino script to the board and check for the port it is conneted to
- install and activate the virtual enviroment provided in the repository.
- run the python script changing the port constant into wherever you have connected your board to
