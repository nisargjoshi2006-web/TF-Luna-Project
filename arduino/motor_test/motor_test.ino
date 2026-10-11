#include <ESP32Servo.h>

#define SERVO_PIN 18

Servo testServo;

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println(F("\n=========================================="));
  Serial.println(F("   MG996R SERVO MOTOR DIAGNOSTIC TEST"));
  Serial.println(F("=========================================="));

  // Allow all 4 hardware timers for ESP32Servo
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);

  testServo.setPeriodHertz(50); // Standard 50Hz servo
  
  // Attach with MG996R standard min/max pulse widths (500us - 2400us)
  int result = testServo.attach(SERVO_PIN, 500, 2400);
  Serial.print(F("Servo attached to GPIO 18, result = "));
  Serial.println(result);
  
  if (result == -1) {
    Serial.println(F("ERROR: Failed to attach servo! Retrying with default attach..."));
    testServo.attach(SERVO_PIN);
  }
}

int angle = 0;
int dir = 5;

void loop() {
  testServo.write(angle);
  
  Serial.print(F("[MOTOR RUNNING] Current Angle: "));
  Serial.print(angle);
  Serial.print(F(" deg | Pulse: "));
  Serial.print(testServo.readMicroseconds());
  Serial.println(F(" us"));

  angle += dir;
  if (angle >= 180) {
    angle = 180;
    dir = -5;
    delay(300);
  } else if (angle <= 0) {
    angle = 0;
    dir = 5;
    delay(300);
  }

  delay(40); // Smooth movement
}
