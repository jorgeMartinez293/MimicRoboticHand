# Robotic Hand Control with Hand Tracking

This project controls a 3D-printed robotic hand using computer vision. It uses MediaPipe to track hand landmarks from a webcam feed and sends servo angles to an Arduino via serial communication.

## Project Structure

- `src/python/`: Python scripts for hand tracking and serial communication.
- `src/arduino/`: Arduino sketches for controlling the servos.
- `hardware/3d_models/`: STLs for printing the robotic hand parts.

## Hardware Requirements

- **Arduino Board** (Uno, Nano, etc.)
- **5x Servo Motors** (SG90 or similar)
- **Webcam**
- **3D Printed Hand Parts** (See `hardware/3d_models/`)
- **External Power Supply** (Recommended for servos)

## Software Requirements

- Python 3.8+
- [Arduino IDE](https://www.arduino.cc/en/software)

## Installation

### 1. Python Environment

It is recommended to use Conda to manage dependencies.

**Linux:**
```bash
conda env create -f src/python/environment_linux.yml
conda activate hand_control
```

**Windows:**
```bash
conda env create -f src/python/environment_win.yml
conda activate hand_control
```

Or install manually via pip:
```bash
pip install opencv-python mediapipe pyserial numpy
```

### 2. Arduino Setup

1. Open `src/arduino/receiver_sketch/receiver_sketch.ino` in the Arduino IDE.
2. Connect your Arduino board.
3. Select the correct Board and Port in **Tools**.
4. Upload the sketch.

**Wiring:**
- Thumb Servo: Pin 2
- Index Servo: Pin 3
- Middle Servo: Pin 4
- Ring Servo: Pin 5
- Pinky Servo: Pin 6

## Usage

1. Connect the Arduino via USB.
2. Run the Python script:
    ```bash
    python src/python/hand_processing.py
    ```
3. Show your hand to the webcam. The robotic hand should mimic your movements.
4. Press `q` to exit the application.

## Credits

Based on "Mano Robotica" by **cmarinv2005** on Thingiverse: [https://www.thingiverse.com/thing:6421211](https://www.thingiverse.com/thing:6421211)
