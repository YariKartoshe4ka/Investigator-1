#include <Servo.h>

unsigned short int SERVO_PIN = 9;
Servo servo;


void setup() {
  servo.attach(SERVO_PIN);
  servo.write(0);
}

void loop() {
  // Nothing here :)
}
