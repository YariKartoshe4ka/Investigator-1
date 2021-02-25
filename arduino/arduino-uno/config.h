#ifndef CONFIG_H
#define CONFIG_H


// Serial section
#define SERIAL_RX 10
#define SERIAL_TX 11
#define SERIAL_SPEED 115200
#define SERIAL_TERMINATOR '\n'
#define SERIAL_DELAY 10

// Servo section
#define SERVO_PIN 9
#define SERVO_MAX_ANGLE 135
#define SERVO_MIN_ANGLE 0
#define SERVO_DELAY 40
unsigned short int SERVO_POS = 0;
String SERVO_DIRECTION = "stop"; // stop/up/down

// Light section
#define LIGHT_PIN 2

// Motor section
#define EN_A 8
#define IN1_A 7
#define IN2_A 6
#define EN_B 5
#define IN1_B 4
#define IN2_B 3
String MOTOR_RUN = "stop";       // stop/forward/backward
String MOTOR_DIRECTION = "stop"; // stop/left/right


#endif
