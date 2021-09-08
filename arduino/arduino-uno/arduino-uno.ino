#include "message.h"
#define _SS_MAX_RX_BUFF MESSAGE_MAX_LENGTH

#include <SoftwareSerial.h>
#include <L298NX2.h>

#include "pins.h"
#include "config.h"


SoftwareSerial SSerial(SERIAL_RX_PIN, SERIAL_TX_PIN);
L298NX2 motors(EN_A_PIN, IN1_A_PIN, IN2_A_PIN, EN_B_PIN, IN1_B_PIN, IN2_B_PIN);

void setup() {
  Serial.begin(9600);
  SSerial.begin(115200);

  while(!SSerial) { /* Wait for ESP32-CAM */ };

  pinMode(LIGHT_PIN, OUTPUT);

  motors.stop();

  flushCommands();
}

void loop() {
  byte message[MESSAGE_MAX_LENGTH];
  short cnt = 0;
  
  getMessage(message, &cnt);

  for (short int i = 0; i < cnt; i++)
    execCommand(message[i]);

  flushCommands();
}
