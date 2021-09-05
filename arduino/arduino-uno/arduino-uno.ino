#include <SoftwareSerial.h>
#include <Servo.h>
#include <L298NX2.h>

#include "pins.h"
#include "config.h"
#include "message.h"


SoftwareSerial SSerial(SERIAL_RX_PIN, SERIAL_TX_PIN);
L298NX2 motors(EN_A_PIN, IN1_A_PIN, IN2_A_PIN, EN_B_PIN, IN1_B_PIN, IN2_B_PIN);
Servo servo;

void setup() {
  Serial.begin(9600);
  SSerial.begin(115200);
  while(!SSerial) { /* Wait for ESP32-CAM */ };

  pinMode(LIGHT_PIN, OUTPUT);

  servo.attach(SERVO_PIN);
  servo.write(CAMERA_ANGLE);

  motors.stop();
  motors.setSpeed(0);
}

void loop() {
  short cnt = -1;
  byte message[255];
  getMessage(message, &cnt);

  for (short int i = 0; i < cnt; i++)
    execCommand(message[i]);

  flushCommands();
}
