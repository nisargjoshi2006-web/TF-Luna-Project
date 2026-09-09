/*
 * Arduino UNO R3 + TF-Luna LiDAR (Sensor Only Mode)
 * Wiring:
 *   - TF-Luna VCC (Red)   -> Arduino 5V
 *   - TF-Luna GND (Black) -> Arduino GND
 *   - TF-Luna TX (Green)  -> Arduino Pin 2
 *   - TF-Luna RX (White)  -> Arduino Pin 3
 */

#include <SoftwareSerial.h>

SoftwareSerial tfSerial(2, 3); // RX = Pin 2, TX = Pin 3

int distance = 0;
int strength = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }

  tfSerial.begin(115200);
  Serial.println(F("yaw_deg,pitch_deg,distance_cm,strength"));
}

bool readTFLuna(int &dist, int &str) {
  unsigned long startTime = millis();
  while (millis() - startTime < 60) {
    if (tfSerial.available() >= 9) {
      if (tfSerial.read() == 0x59 && tfSerial.read() == 0x59) {
        uint8_t buf[7];
        tfSerial.readBytes(buf, 7);

        uint8_t checksum = 0x59 + 0x59;
        for (int i = 0; i < 6; i++) {
          checksum += buf[i];
        }

        if (checksum == buf[6]) {
          dist = buf[0] + (buf[1] << 8); // Distance in cm
          str  = buf[2] + (buf[3] << 8); // Signal strength
          return true;
        }
      }
    }
  }
  return false;
}

void loop() {
  if (readTFLuna(distance, strength)) {
    // Output standard CSV line
    Serial.print(F("0,0,"));
    Serial.print(distance);
    Serial.print(F(","));
    Serial.println(strength);
  }
  delay(30); // ~33 Hz update rate
}
