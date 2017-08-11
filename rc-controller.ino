#include <Servo.h>

int ch1;
int p_ch1 = 200;
const int alpha_ch1 = 15;
Servo ch1_out;

int t_last_log = 0;
int t_log_freq = 250;

// CH1 - steering angle
// PIN 9 (pwm) - OUTPUT CH1. Connect it to pwm wire of the steeering servo in the model.
// PIN 10 (pwm) - INPUT CH1. Connect it to steering pwm output in model Rx (channel 1)

// TODO: CH2 - throttle
// PIN 11 (pwm) - OUTPUT CH2. Connect it to pwm wire of the steeering servo in the model.
// PIN 12 (pwm) - INPUT CH2. Connect it to steering pwm output in model Rx (channel 2)

void setup() {
  ch1_out.attach(9);
  pinMode(10, INPUT);
  Serial.begin(9600);
}

void loop() { 
  ch1 = pulseIn(10, HIGH); // Read the pulse width of 973 - 1954
  if (abs(ch1 - p_ch1) > alpha_ch1) {
    p_ch1 = ch1;  
    ch1_out.writeMicroseconds(p_ch1);
  }
  
  int t = millis();
  if (t - t_last_log > t_log_freq) {
    t_last_log = t;
    Serial.println(p_ch1);          
  }
  
  delay(10);
}
