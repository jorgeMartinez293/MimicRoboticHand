#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

const byte numFingers = 5;
int pos[numFingers];
float fingerValues[numFingers];
int output_pin = 0;

void setup() {
  Serial.begin(9600);
  servo1.attach(8);
  servo2.attach(9);
  servo3.attach(10);
  servo4.attach(11);
  servo5.attach(12);
}

void loop() {
  if (Serial.available()) {

    char buffer[64];
    size_t len = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
    buffer[len] = '\0';

    char* token = strtok(buffer, ",");
    byte index = 0;

    while (token != NULL && index < numFingers) {
      fingerValues[index] = atof(token);
      token = strtok(NULL, ",");
      index++;
    }

    for (int i = 0; i < numFingers; i++) {  
      output_pin = 8 + i;
      pos[i] = fingerValues[i];
      servo1.write(pos);
    }
  }
}