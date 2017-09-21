#include <Servo.h>

#define SERVO_PIN_OUT 11 // steering servo
#define SERVO_PIN_IN 3

#define ESC_PIN_OUT 9 // electronic speed controller
#define ESC_PIN_IN 7

#define THROTTLE_ZERO 1470
#define MAX_THROTTLE 2500
#define MAX_STEERING 2500
#define DEFAULT_THROTTLE 1550

// learning
#define COMMAND_NO_INPUT 'i' // idle
#define COMMAND_PILOT_INPUT 'r' // remote
#define COMMAND_SERIAL_INPUT 'a' // autonomus
#define COMMAND_SERIAL_STEER 'd' // turn

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

char serialInput[128];
int inputSize = 0;
int inputStart = 0;
enum InputMode inputMode = inputModePilot;

int lastAppliedSteer = 0;
int currentSteer = 0;

Servo steeringOut;
Servo throttleOut;

int currentThrottle = THROTTLE_ZERO;
int currentSteering = THROTTLE_ZERO;

volatile unsigned long throttleInputStartTime = 0;
volatile unsigned long steeringInputStartTime = 0;

void setup() {
  steeringOut.attach(SERVO_PIN_OUT);
  throttleOut.attach(ESC_PIN_OUT);
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(ESC_PIN_IN, INPUT);
  Serial.begin(9600);

  setInputMode(commandPilotInput);
}

void loop() {
  handleCommands();
  
  int t = millis();
  if (inputMode != inputModeNone && t - t_last_apply > t_min_apply_delay) {
    applyCurrentValues();
    t_last_apply = t;
  }

  t = millis();
  if (t - t_last_log > t_log_freq) {
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

  char c = serialInput[inputStart];
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
      steerCommandValue = value; // TODO: incorrect value flow
      inputStart += 3;
      return commandSerialSteerValue;
    }
  } else {
    inputStart += 1; // TODO: log incorrect case?
    return commandIncorrect;
  }

  return commandEmpty;
}

void enablePwmInterrupts() { // TODO: is it safe to call it twice? same for disable
  attachInterrupt(digitalPinToInterrupt(ESC_PIN_IN), throttleRise, RISING);
  attachInterrupt(digitalPinToInterrupt(SERVO_PIN_IN), steeringRise, RISING);
}

void disablePwmInterrupts() {
  detachInterrupt(digitalPinToInterrupt(ESC_PIN_IN));
  detachInterrupt(digitalPinToInterrupt(SERVO_PIN_IN));
}

void steerCommand(int value) {
  if (inputMode != inputModeSerial) return;

  currentSteer = value;
}

void applyCurrentValues() {
  // Read the pulse width of 973 - 1954 for steering
  steeringOut.writeMicroseconds(currentSteering);

  // Read the pulse width of 973 - 1954 for thr
  throttleOut.writeMicroseconds(currentThrottle);
}

void setInputMode(Command modeCommand) {
  if (modeCommand == commandNoInput) {
    disablePwmInterrupts();
    inputMode = inputModeNone;
  } else if (modeCommand == commandPilotInput) {
    enablePwmInterrupts();
    inputMode = inputModePilot;
  } else if (modeCommand == commandSerialInput) {
    disablePwmInterrupts();
    currentThrottle = DEFAULT_THROTTLE; // Const throttle so far, to discuss.
    inputMode = inputModeSerial;
  }
}

void serialEvent() {
  int inputLen = Serial.available();
  if (inputLen > 0) {
    char input[inputLen];
    Serial.readBytes(input, inputLen);

    for (int i = 0; i < inputLen; i++) {
      serialInput[inputSize + i] = input[i]; // we assume here that inputStart == 0
    }

    inputSize += inputLen;
  }
}
