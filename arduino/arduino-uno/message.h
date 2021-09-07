#ifndef MESSAGE_H
#define MESSAGE_H


#define MESSAGE_HEADER             0x01
#define MESSAGE_FOOTER             0xFF

#define MESSAGE_DELAY              3
#define MESSAGE_MAX_LOST           5
#define MESSAGE_MAX_LENGTH         255

#define COMMAND_LIGHT_ON           0x02
#define COMMAND_LIGHT_OFF          0x03
#define COMMAND_DIRECTION_STOP     0x04
#define COMMAND_DIRECTION_LEFT     0x05
#define COMMAND_DIRECTION_RIGHT    0x06
#define COMMAND_RUN_STOP           0x07
#define COMMAND_RUN_FORWARD        0x08
#define COMMAND_RUN_BACKWARD       0x09
#define COMMAND_SPEED_LOW          0x0A
#define COMMAND_SPEED_MEDIUM       0x0B
#define COMMAND_SPEED_HIGH         0x0C
#define COMMAND_SPEED_DEC          0x0D
#define COMMAND_SPEED_INC          0x0E
#define COMMAND_CAMERA_DOWN        0x0F
#define COMMAND_CAMERA_MIDDLE      0x10
#define COMMAND_CAMERA_UP          0x11
#define COMMAND_CAMERA_DEC         0x12
#define COMMAND_CAMERA_INC         0x13


/**
 * bool getMessage - gets message from Serial
 *
 * This function can be used to get message from Serial port
 * Copies commands to the passed array @message. Writes the
 * number of processed commands to the @cnt. Max length of
 * message defined in MESSAGE_MAX_LENGTH
 * 
 * Returns `false` on success and `true` on failure
 *
 * @message: byte array where to copy commands
 * @cnt: number of processed commands
 */
bool getMessage(byte message[MESSAGE_MAX_LENGTH], short *cnt);


/**
 * bool execCommand - executes passed command
 *
 * This function can be used to execute passed command
 * It checks the @command with a switch-case, and if such
 * a command is detected, it executes it
 * 
 * Returns `false` on success and `true` on failure
 *
 * @command: hex command to execute
 */
bool execCommand(byte command);


/**
 * void flushCommands - flushes cached values
 *
 * This function can be used to to flush or apply
 * cached values of already executed commands from
 * `execCommand`. Takes more than 1 second to execute
 */
void flushCommands();


#endif /* MESSAGE_H */