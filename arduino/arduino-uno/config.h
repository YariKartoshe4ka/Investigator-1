#ifndef CONFIG_H
#define CONFIG_H


/* Motor section */
#define MOTOR_RUN_STOP          0
#define MOTOR_RUN_FORWARD       1
#define MOTOR_RUN_BACKWARD      2
short MOTOR_RUN = MOTOR_RUN_STOP;

#define MOTOR_DIRECTION_STOP    0
#define MOTOR_DIRECTION_LEFT    1
#define MOTOR_DIRECTION_RIGHT   2
short MOTOR_DIRECTION = MOTOR_DIRECTION_STOP;

#define MOTOR_SPEED_LOW         0
#define MOTOR_SPEED_MEDIUM      127
#define MOTOR_SPEED_HIGH        255
short MOTOR_SPEED = MOTOR_SPEED_LOW;


#endif /* CONFIG_H */
