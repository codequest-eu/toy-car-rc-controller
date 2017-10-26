#include <Servo.h>
#include <Arduino.h>

#define SERVO_PIN_OUT 11 // steering servo
#define SERVO_PIN_IN 3

#define ESC_PIN_OUT 9 // electronic speed controller
#define ESC_PIN_IN 7

#define THROTTLE_ZERO 1470
#define MAX_THROTTLE 2500
#define MAX_STEERING 2500
#define DEFAULT_THROTTLE 1540

// learning
#define COMMAND_NO_INPUT 'I' // idle
#define COMMAND_PILOT_INPUT 'R' // remote
#define COMMAND_SERIAL_INPUT 'A' // autonomus
#define COMMAND_SERIAL_STEER 'T' // turn value

int t_last_log = 0;
int t_log_freq = 50;

int t_last_apply = 0;
int t_min_apply_delay = 50;

enum Command {
  commandEmpty,
  commandIncorrect,
  commandNoInput,
  commandPilotInput,
  commandSerialInput,
  commandSerialSteerValue
};

int steerCommandValue = 0;

enum InputMode {
  inputModeNone,
  inputModePilot,
  inputModeSerial
};

unsigned char serialInput[128];
int inputSize = 0;
int inputStart = 0;
enum InputMode inputMode = inputModePilot;

int lastAppliedSteer = 0;
int currentSteering = THROTTLE_ZERO;

Servo steeringOut;
Servo throttleOut;

int currentThrottle = THROTTLE_ZERO;

volatile unsigned long throttleInputStartTime = 0;
volatile unsigned long steeringInputStartTime = 0;

void setup() {
  steeringOut.attach(SERVO_PIN_OUT);
  throttleOut.attach(ESC_PIN_OUT);
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(ESC_PIN_IN, INPUT);
  Serial.begin(9600);

  setInputMode(commandNoInput);
}

void loop() {
  serialEvent2();
  handleCommands();
  
  int t = millis();
  if (inputMode != inputModeNone && t - t_last_apply > t_min_apply_delay) {
    applyCurrentValues();
    t_last_apply = t;
  }

  t = millis();
  if (inputMode == inputModePilot && t - t_last_log > t_log_freq) {
    t_last_log = t;
    Serial.println(currentSteering);
  }
}

void throttleRise() {
  throttleInputStartTime = micros();
  attachInterrupt(digitalPinToInterrupt(ESC_PIN_IN), throttleFall, FALLING);
}

void throttleFall() {
  unsigned long throttle = micros() - throttleInputStartTime;
  if (throttle >= 0 && throttle < MAX_THROTTLE) {
    currentThrottle = throttle;
  }
  attachInterrupt(digitalPinToInterrupt(ESC_PIN_IN), throttleRise, RISING);
}

void steeringRise() {
  steeringInputStartTime = micros();
  attachInterrupt(digitalPinToInterrupt(SERVO_PIN_IN), steeringFall, FALLING);
}

void steeringFall() {
  unsigned long steering = micros() - steeringInputStartTime;
  if (steering >= 0 && steering < MAX_STEERING) {
    currentSteering = steering;
  }
  attachInterrupt(digitalPinToInterrupt(SERVO_PIN_IN), steeringRise, RISING);
}

void handleCommands() {
  Command command;
  while (command = readSerialCommand(), command != commandEmpty) {
    if (command == commandNoInput || command == commandPilotInput || command == commandSerialInput) {
      setInputMode(command);
    } else if (command == commandSerialSteerValue) {
      steerCommand(steerCommandValue);
    }
  }

  int remainingBytes = inputSize - inputStart;
  for (int i = 0; i < remainingBytes; i++) {
    serialInput[i] = serialInput[inputStart + i];
  }

  inputStart = 0;
  inputSize = remainingBytes;
}

Command readSerialCommand() {
  int bytesInBuffer = inputSize - inputStart;

  if (bytesInBuffer < 1) {
    return commandEmpty;
  }

  unsigned char c = serialInput[inputStart];
  
  if (c == COMMAND_NO_INPUT) {
    inputStart += 1;
    return commandNoInput;
  } else if (c == COMMAND_PILOT_INPUT) {
    inputStart += 1;
    return commandPilotInput;
  } else if (c == COMMAND_SERIAL_INPUT) {
    inputStart += 1;
    return commandSerialInput;
  } else if (c == COMMAND_SERIAL_STEER) {
    if (bytesInBuffer < 3) {
      return commandEmpty;
    } else {
      uint16_t value = (uint16_t(serialInput[inputStart + 1]) << 8) |
                       serialInput[inputStart + 2];
      steerCommandValue = value; // TODO: add incorrect value flow
      inputStart += 3;
      return commandSerialSteerValue;
    }
  } else {
    inputStart += 1; // TODO: add log incorrect case?
    return commandIncorrect;
  }

  return commandEmpty;
}

void enablePwmInterrupts() { // TODO: is it safe to call it twice? same for disable
//  attachInterrupt(digitalPinToInterrupt(ESC_PIN_IN), throttleRise, RISING);
  attachInterrupt(digitalPinToInterrupt(SERVO_PIN_IN), steeringRise, RISING);
}

void disablePwmInterrupts() {
//  detachInterrupt(digitalPinToInterrupt(ESC_PIN_IN));
  detachInterrupt(digitalPinToInterrupt(SERVO_PIN_IN));
  currentThrottle = THROTTLE_ZERO;
  currentSteering = THROTTLE_ZERO;
  applyCurrentValues();
}

void steerCommand(int value) {
  if (inputMode != inputModeSerial) return;
  
  currentSteering = value;
}

void applyCurrentValues() {
  // Read the pulse width of 973 - 1954 for steering
  steeringOut.writeMicroseconds(currentSteering);
  if (abs(lastAppliedSteer - currentSteering) > 10) {
    logDebug("new steer applied:");
    logDebug(String(currentSteering));
    lastAppliedSteer = currentSteering;
  }

  // Read the pulse width of 973 - 1954 for thr
  throttleOut.writeMicroseconds(compensated_throttle());
}

void setInputMode(Command modeCommand) {
  if (modeCommand == commandNoInput) {
    logDebug("enter idle mode");
    disablePwmInterrupts();
    inputMode = inputModeNone;
  } else if (modeCommand == commandPilotInput) {
    logDebug("enter pilot mode");
    enablePwmInterrupts();
    inputMode = inputModePilot;
    currentThrottle = DEFAULT_THROTTLE;
  } else if (modeCommand == commandSerialInput) {
    logDebug("enter serial mode");
    disablePwmInterrupts();
    currentThrottle = DEFAULT_THROTTLE; // Const throttle so far, to discuss.
    inputMode = inputModeSerial;
  }
}

int compensated_throttle() {
  int compensation = abs(currentSteering - THROTTLE_ZERO) / 55;
  
  return currentThrottle + compensation;
}

void serialEvent2() {
  int inputLen = Serial.available();
  if (inputLen > 0) {
    unsigned char input[inputLen];
    Serial.readBytes(input, inputLen);

    for (int i = 0; i < inputLen; i++) {
      serialInput[inputSize + i] = input[i]; // we assume here that inputStart == 0
    }

    inputSize += inputLen;
  }
}

void logDebug(String message) {
  if (inputMode != inputModePilot) { // tmp, in input mode we need to print only steer values
    Serial.println(message);
  }
}

