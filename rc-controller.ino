#include <Servo.h>

#define SERVO_PIN_OUT 11 // steering servo
#define SERVO_PIN_IN 13

#define ESC_PIN_OUT 9 // electronic speed controller
#define ESC_PIN_IN 10

#define THROTTLE_ZERO 1470

int ch1;
int p_ch1 = 200;
const int alpha_ch1 = 25;
Servo ch1_out;

int ch2;
int p_ch2 = 0;
const int alpha_ch2 = 40;
Servo ch2_out;

int t_last_log = 0;
int t_log_freq = 250;

void setup() {
  ch1_out.attach(SERVO_PIN_OUT);
  ch2_out.attach(ESC_PIN_OUT);
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(ESC_PIN_IN, INPUT);
  Serial.begin(9600);
}

void loop() { 
  ch1 = pulseIn(SERVO_PIN_IN, HIGH); // Read the pulse width of 973 - 1954 for steering
  if (abs(ch1 - p_ch1) > alpha_ch1) {
    p_ch1 = ch1;  
    ch1_out.writeMicroseconds(p_ch1);
  }
  
  ch2 = pulseIn(ESC_PIN_IN, HIGH); // Read the pulse width of 973 - 1954 for thr
  if (ch2 > THROTTLE_ZERO + alpha_ch2 || ch2 < THROTTLE_ZERO - alpha_ch2) {
    p_ch2 = ch2;
  } else {
    p_ch2 = THROTTLE_ZERO;
  }
  ch2_out.writeMicroseconds(p_ch2);
  
  int t = millis();
  if (t - t_last_log > t_log_freq) {
    t_last_log = t;
    String log_out = "{\"steering\": ";
    log_out += p_ch1;
    log_out += ", \"acceleration\": ";
    log_out += p_ch2;
    log_out += "}";
    Serial.println(log_out);
  }
  
  delay(10);
}
