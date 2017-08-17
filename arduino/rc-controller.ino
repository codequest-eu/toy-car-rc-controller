#include <Servo.h>

#define SERVO_PIN_OUT 11 // steering servo
#define SERVO_PIN_IN 13

#define ESC_PIN_OUT 9 // electronic speed controller
#define ESC_PIN_IN 10

#define THROTTLE_ZERO 1470

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

void setup() {
  ch1_out.attach(SERVO_PIN_OUT);
  ch2_out.attach(ESC_PIN_OUT);
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(ESC_PIN_IN, INPUT);
  Serial.begin(9600);
}

void loop() { 
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
