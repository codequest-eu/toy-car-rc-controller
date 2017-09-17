#include <Servo.h>

#define SERVO_PIN_OUT 11 // steering servo
#define SERVO_PIN_IN 3

#define ESC_PIN_OUT 9 // electronic speed controller
#define ESC_PIN_IN 7

#define THROTTLE_ZERO 1470
#define MAX_THROTTLE 2500
#define MAX_STEERING 2500
#define DEFAULT_THROTTLE 1520

#define COMMAND_NO_INPUT "stop"
#define COMMAND_PILOT_INPUT "pilot"
#define COMMAND_SERIAL_INPUT "serial"

int t_last_log = 0;
int t_log_freq = 50;

enum InputMode {
  inputModeNone,
  inputModePilot,
  inputModeSerial
};

String serialInput = "";
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

  enablePwmInterrupts();
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

void loop() { 
  handleCommands();

  if (inputMode != inputModeNone) {
    applyCurrentValues();
  }
  
  int t = millis();
  if (t - t_last_log > t_log_freq) {
    t_last_log = t;
    Serial.println(currentSteering);
  }
}

void handleCommands() {
  while (int separatorLocation = serialInput.indexOf('\n') >= 0) {
    String command = serialInput.substring(0, separatorLocation);
    serialInput = serialInput.substring(separatorLocation + 1);

    executeCommand(command);
  }
}

void executeCommand(String command) {
  if (command == COMMAND_NO_INPUT) {
      setInputMode(inputModeNone);
    } else if (command == COMMAND_PILOT_INPUT) {
      setInputMode(inputModePilot);
    } else if (command == COMMAND_SERIAL_INPUT) {
      setInputMode(inputModeSerial);
    } else if (int steer = command.toInt() != 0) { // Only numeric value in command is new steering. Probably will need to extend later.
      steerCommand(steer);
    }
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

void setInputMode(InputMode mode) {
  inputMode = mode;
  if (mode == inputModeNone) {
    disablePwmInterrupts();
  } else if (mode == inputModePilot) {
    enablePwmInterrupts();
  } else if (mode == inputModeSerial) {
    disablePwmInterrupts();
    currentThrottle = DEFAULT_THROTTLE; // Const throttle so far, to discuss.
  }
}

//void serialEvent() {
//  int inputLen = Serial.available();
//  if (inputLen > 0) {
//    char input[inputLen];
//    Serial.readBytes(input, inputLen);
//    serialInput += String(input);
//  }
//}
