
#include <Servo.h> 

Servo myservo[5];  

const byte numFingers = 5;
int pos[numFingers];
int output_pin = 2; 

void setup() { 
  
  Serial.begin(9600);
  myservo[0].attach(2);
  myservo[1].attach(3);
  myservo[2].attach(4);
  myservo[3].attach(5);
  myservo[4].attach(6);
  
  myservo[0].write(0);
  myservo[1].write(180);
  myservo[2].write(180);
  myservo[3].write(180);
  myservo[4].write(0);
  
  delay(3000);
  
}
   
void loop() {
  if (Serial.available()) {

    char buffer[64];
    size_t len = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
    buffer[len] = '\0';

    char* token = strtok(buffer, ",");
    byte index = 0;

    while (token != NULL && index < numFingers) {
      pos[index] = atoi(token);
      token = strtok(NULL, ",");
      index++;
    }
  }
  
  for (int i = 0; i < numFingers; i++) {
    if (i == 0 || i == 4) {
      myservo[i].write(pos[i]);
    } else {
      myservo[i].write(180 - pos[i]);
    }
  }
} 

