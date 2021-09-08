bool getMessage(byte message[MESSAGE_MAX_LENGTH], short *cnt) {
  bool collect = false;
  short lost = 0;

  while(collect || SSerial.available()) {
    delay(MESSAGE_DELAY);

    byte received = SSerial.read();

    if (received == MESSAGE_FOOTER)
      return false;

    if (received == -1) {
      if (++lost == MESSAGE_MAX_LOST)
        return true;
      continue;
    }

    if (*cnt == MESSAGE_MAX_LENGTH)
      return true;

    if (received == MESSAGE_HEADER) {
      collect = true;
      continue;
    }

    if (collect)
      message[(*cnt)++] = received;
  }
  return false;
}


bool execCommand(byte command) {
  switch (command) {

    case COMMAND_LIGHT_ON: {
      digitalWrite(LIGHT_PIN, HIGH);
      break;
    }

    case COMMAND_LIGHT_OFF: {
      digitalWrite(LIGHT_PIN, LOW);
      break;
    }

    case COMMAND_DIRECTION_STOP: {
      if(MOTOR_RUN == MOTOR_RUN_FORWARD) {
        if(MOTOR_DIRECTION == MOTOR_DIRECTION_LEFT)
          motors.forwardA();
        else if(MOTOR_DIRECTION == MOTOR_DIRECTION_RIGHT)
          motors.forwardB();
      }
      else if(MOTOR_RUN == MOTOR_RUN_BACKWARD) {
        if(MOTOR_DIRECTION == MOTOR_DIRECTION_LEFT)
          motors.backwardA();
        else if(MOTOR_DIRECTION == MOTOR_DIRECTION_RIGHT)
          motors.backwardB();
      }
      MOTOR_DIRECTION = MOTOR_DIRECTION_STOP;
      break;
    }

    case COMMAND_DIRECTION_LEFT: {
      motors.stopA();
      MOTOR_DIRECTION = MOTOR_DIRECTION_LEFT;
      break;
    }

    case COMMAND_DIRECTION_RIGHT: {
      motors.stopB();
      MOTOR_DIRECTION = MOTOR_DIRECTION_RIGHT;
      break;
    }

    case COMMAND_RUN_STOP: {
      motors.stop();
      MOTOR_RUN = MOTOR_RUN_STOP;
      break;
    }

    case COMMAND_RUN_FORWARD: {
      if(MOTOR_DIRECTION == MOTOR_DIRECTION_STOP)
        motors.forward();
      else if(MOTOR_DIRECTION == MOTOR_DIRECTION_LEFT)
        motors.forwardB();
      else if(MOTOR_DIRECTION == MOTOR_DIRECTION_RIGHT)
        motors.forwardA();
      MOTOR_RUN = MOTOR_RUN_FORWARD;
      break;
    }

    case COMMAND_RUN_BACKWARD: {
      if(MOTOR_DIRECTION == MOTOR_DIRECTION_STOP)
        motors.backward();
      else if(MOTOR_DIRECTION == MOTOR_DIRECTION_LEFT)
        motors.backwardB();
      else if(MOTOR_DIRECTION == MOTOR_DIRECTION_RIGHT)
        motors.backwardA();
      MOTOR_RUN = MOTOR_RUN_BACKWARD;
      break;
    }

    case COMMAND_SPEED_LOW: {
      MOTOR_SPEED = MOTOR_SPEED_LOW;
      break;
    }

    case COMMAND_SPEED_MEDIUM: {
      MOTOR_SPEED = MOTOR_SPEED_MEDIUM;
      break;
    }

    case COMMAND_SPEED_HIGH: {
      MOTOR_SPEED = MOTOR_SPEED_HIGH;
      break;
    }

    case COMMAND_SPEED_DEC: {
      MOTOR_SPEED--;
      break;
    }

    case COMMAND_SPEED_INC: {
      MOTOR_SPEED++;
      break;
    }

    default:
      return false;
  }

  return true;
}


void flushCommands() {
  motors.setSpeed(MOTOR_SPEED);
}
