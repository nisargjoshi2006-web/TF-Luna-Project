/*
 * Arduino UNO R3 + TF-Luna LiDAR Telemetry Firmware
 * Non-blocking, robust 9-byte binary packet parser with checksum validation
 * 
 * Wiring:
 *   - TF-Luna VCC (Red)   -> Arduino 5V
 *   - TF-Luna GND (Black) -> Arduino GND
 *   - TF-Luna TX (Green)  -> Arduino Pin 2 (SoftwareSerial RX)
 *   - TF-Luna RX (White)  -> Arduino Pin 3 (SoftwareSerial TX)
 */

#include <SoftwareSerial.h>

SoftwareSerial tfSerial(2, 3); // Pin 2 = RX, Pin 3 = TX

int distance = 0;
int strength = 0;

// Non-blocking frame parser for TF-Luna 9-byte standard protocol
bool getTFLunaData(int &dist, int &str) {
  static uint8_t state = 0;
  static uint8_t buf[9];
  static uint8_t idx = 0;

  while (tfSerial.available() > 0) {
    uint8_t b = tfSerial.read();

    if (state == 0) {
      if (b == 0x59) {
        buf[0] = b;
        state = 1;
      }
    } else if (state == 1) {
      if (b == 0x59) {
        buf[1] = b;
        idx = 2;
        state = 2;
      } else if (b == 0x59) {
        // Still 0x59, keep looking for next byte
        buf[0] = b;
        state = 1;
      } else {
        state = 0; // Reset
      }
    } else if (state == 2) {
      buf[idx++] = b;
      if (idx == 9) {
        state = 0; // Reset for next frame
        
        // Checksum calculation: sum of bytes 0..7
        uint8_t checksum = 0;
        for (int i = 0; i < 8; i++) {
          checksum += buf[i];
        }

        if (checksum == buf[8]) {
          dist = buf[2] | (buf[3] << 8); // Distance in cm
          str  = buf[4] | (buf[5] << 8); // Signal strength
          return true; // Valid frame!
        }
      }
    }
  }
  return false;
}

void setup() {
  // Serial to Computer (USB)
  Serial.begin(115200);
  while (!Serial) { delay(10); }

  // Serial to TF-Luna LiDAR
  tfSerial.begin(115200);

  // Clear incoming buffer
  while (tfSerial.available() > 0) {
    tfSerial.read();
  }

  // Header for serial reader / CSV parsing
  Serial.println(F("yaw_deg,pitch_deg,distance_cm,strength"));
}

void loop() {
  if (getTFLunaData(distance, strength)) {
    // Stream live CSV telemetry
    Serial.print(F("0,0,"));
    Serial.print(distance);
    Serial.print(F(","));
    Serial.println(strength);
  }
}
