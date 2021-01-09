#include <SoftwareSerial.h>
#include <Servo.h>
#include <L298NX2.h>
#include "config.h"


SoftwareSerial SSerial(SERIAL_RX, SERIAL_TX);
Servo servo;
L298NX2 motors(EN_A, IN1_A, IN2_A, EN_B, IN1_B, IN2_B);


String getCommand() {
  String command = "";
  char symbol;

  while(SSerial.available()) {
    symbol = SSerial.read();
    if(symbol == '\n')
      break;

    command += symbol;
    delay(SERIAL_DELAY);
  }

  return command;
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup() {
  SSerial.begin(SERIAL_SPEED);
  while(!SSerial) { /* Wait for ESP32-CAM */ };

  pinMode(LIGHT_PIN, OUTPUT);

  servo.attach(SERVO_PIN);
  servo.write(SERVO_POS);

  motors.stop();
  motors.setSpeed(0);
}

void loop() {
  String command = getCommand();
  String option  = getValue(command, ' ', 0);
  String value   = getValue(command, ' ', 1);

  // Light section
  if(option == "light") {
    if(value == "on")
      digitalWrite(LIGHT_PIN, HIGH);
    else if(value == "off")
      digitalWrite(LIGHT_PIN, LOW);
  }
  // Servo section
  else if(option == "camera") {
    if(value == "up")
      SERVO_DIRECTION = "up";
    else if(value == "down")
      SERVO_DIRECTION = "down";
    else if(value == "stop")
      SERVO_DIRECTION = "stop";
  }
  // Motor direction section
  else if(option == "direction") {
    if(value == "stop") {
      if(MOTOR_RUN == "forward") {
        if(MOTOR_DIRECTION == "left")
          motors.forwardA();
        else if(MOTOR_DIRECTION == "right")
          motors.forwardB();
      }
      else if(MOTOR_RUN == "backward") {
        if(MOTOR_DIRECTION == "left")
          motors.backwardA();
        else if(MOTOR_DIRECTION == "right")
          motors.backwardB();
      }
      MOTOR_DIRECTION = "stop";
    }
    else if(value == "left") {
      motors.stopA();
      MOTOR_DIRECTION = "left";
    }
    else if(value == "right") {
      motors.stopB();
      MOTOR_DIRECTION = "right";
    }
  }
  // Motor run section
  else if(option == "motor") {
    if(value == "stop") {
      motors.stop();
      MOTOR_RUN = "stop";
    }
    else if(value == "forward") {
      if(MOTOR_DIRECTION == "left")
        motors.forwardB();
      else if(MOTOR_DIRECTION == "right")
        motors.forwardA();
      else if(MOTOR_DIRECTION == "stop")
        motors.forward();
      MOTOR_RUN = "forward";
    }
    else if(value == "backward") {
      if(MOTOR_DIRECTION == "left")
        motors.backwardB();
      else if(MOTOR_DIRECTION == "right")
        motors.backwardA();
      else if(MOTOR_DIRECTION == "stop")
        motors.backward();
      MOTOR_RUN = "backward";
    }
  }
  // Motor speed section
  else if(option == "speed") {
    motors.setSpeed(value.toInt());
  }


  // Servo sweep loop
  if(SERVO_DIRECTION == "up") {
    if(SERVO_POS == SERVO_MAX_ANGLE)
      SERVO_DIRECTION = "stop";
    else {
      servo.write(SERVO_POS++);
      delay(SERVO_DELAY);
    }
  }
  if(SERVO_DIRECTION == "down") {
    if(SERVO_POS == SERVO_MIN_ANGLE)
      SERVO_DIRECTION = "stop";
    else {
      servo.write(SERVO_POS--);
      delay(SERVO_DELAY);
    }
  }
}
