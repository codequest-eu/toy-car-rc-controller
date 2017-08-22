#include <Servo.h>

#define SERVO_PIN_OUT 11 // steering servo
#define SERVO_PIN_IN 13

#define ESC_PIN_OUT 9 // electronic speed controller
#define ESC_PIN_IN 10

#define THROTTLE_ZERO 1470
#define DEFAULT_THROTTLE 1520

#define COMMAND_NO_INPUT "stop"
#define COMMAND_PILOT_INPUT "pilot"
#define COMMAND_SERIAL_INPUT "serial"

int ch1;
int steering_value = 0;
const int alpha_ch1 = 25;
Servo ch1_out;

int ch2;
int throttle_value = 0;
const int alpha_ch2 = 40;
Servo ch2_out;

int t_last_log = 0;
int t_log_freq = 50;

// New vars section below. Ones above should be removed during refactor or moved down if still needed.

enum InputModes {
  inputModeNone,
  inputModePilot,
  inputModeSerial
};

String serialInput = "";
enum InputModes inputMode = inputModeNone;

int lastAppliedSteer = 0;
int currentSteer = 0;

int currentThrottle = THROTTLE_ZERO;

void setup() {
  ch1_out.attach(SERVO_PIN_OUT);
  ch2_out.attach(ESC_PIN_OUT);
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(ESC_PIN_IN, INPUT);
  Serial.begin(9600);
}

void loop() { 
  handleCommands();
  
  ch1 = pulseIn(SERVO_PIN_IN, HIGH); // Read the pulse width of 973 - 1954 for steering
  if (abs(ch1 - steering_value) > alpha_ch1) {
    steering_value = ch1;  
    ch1_out.writeMicroseconds(steering_value);
  }
  
  ch2 = pulseIn(ESC_PIN_IN, HIGH); // Read the pulse width of 973 - 1954 for thr
  if (ch2 > THROTTLE_ZERO + alpha_ch2 || ch2 < THROTTLE_ZERO - alpha_ch2) {
    throttle_value = ch2;
  } else {
    throttle_value = THROTTLE_ZERO;
  }
  ch2_out.writeMicroseconds(throttle_value);
  
  int t = millis();
  if (t - t_last_log > t_log_freq) {
    t_last_log = t;
    Serial.println(steering_value);
  }
  
  delay(10);
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
      inputMode = inputModeNone;
    } else if (command == COMMAND_PILOT_INPUT) {
      inputMode = inputModePilot;
    } else if (command == COMMAND_SERIAL_INPUT) {
      inputMode = inputModeSerial;
      currentThrottle = DEFAULT_THROTTLE; // Const throttle so far, to discuss.
    } else if (int steer = command.toInt() != 0) { // Only numeric value in command is new steering. Probably will need to extend later.
      steerCommand(steer);
    }
}

void steerCommand(int value) {
  if (inputMode != inputModeSerial) return;

  currentSteer = value;
}

void serialEvent() {
  int inputLen = Serial.available();
  if (inputLen > 0) {
    char input[inputLen];
    Serial.readBytes(input, inputLen);
    serialInput += String(input);
  }
}
