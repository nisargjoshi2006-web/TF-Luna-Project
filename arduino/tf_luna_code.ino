/*
 * ======================================================================================
 *       TF-LUNA LIDAR TELEMETRY FIRMWARE (UNIVERSAL: ESP-32 & ARDUINO UNO)
 * ======================================================================================
 * Features:
 * 1. Automatically detects whether you are using an ESP-32 or an Arduino UNO.
 * 2. ESP-32: Uses high-speed HardwareSerial Serial2 (Zero external libraries required!).
 * 3. Arduino UNO: Uses SoftwareSerial (Pin 2 RX, Pin 3 TX).
 * 4. Paced 60 Hz rate limiter prevents USB serial buffer congestion and eliminates lag.
 * 5. Full 9-byte binary packet checksum validation.
 * 
 * WIRING DIAGRAM:
 * --------------------------------------------------------------------------------------
 *  FOR ESP-32 (NodeMCU / DevKit):
 *    - TF-Luna VCC (Red)   -> ESP-32 VIN or 5V
 *    - TF-Luna GND (Black) -> ESP-32 GND
 *    - TF-Luna TX  (Green) -> ESP-32 GPIO 16 (RX2)
 *    - TF-Luna RX  (White) -> ESP-32 GPIO 17 (TX2)
 *
 *  FOR ARDUINO UNO:
 *    - TF-Luna VCC (Red)   -> Arduino 5V
 *    - TF-Luna GND (Black) -> Arduino GND
 *    - TF-Luna TX  (Green) -> Arduino Digital Pin 2 (RX)
 *    - TF-Luna RX  (White) -> Arduino Digital Pin 3 (TX)
 * ======================================================================================
 */

#if defined(ESP32)
  // ESP-32 uses HardwareSerial (Serial2)
  #define tfSerial Serial2
  #define RX_PIN 16
  #define TX_PIN 17
#else
  // Arduino UNO uses SoftwareSerial
  #include <SoftwareSerial.h>
  SoftwareSerial tfSerial(2, 3); // Pin 2 = RX, Pin 3 = TX
#endif

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
      } else {
        state = (b == 0x59) ? 1 : 0;
      }
    } else if (state == 2) {
      buf[idx++] = b;
      if (idx == 9) {
        state = 0; // Reset for next frame
        
        // Checksum calculation: sum of lower 8 bits of bytes 0..7
        uint8_t checksum = 0;
        for (int i = 0; i < 8; i++) {
          checksum += buf[i];
        }

        if (checksum == buf[8]) {
          dist = buf[2] | (buf[3] << 8); // Distance in cm
          str  = buf[4] | (buf[5] << 8); // Signal strength (flux)
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
#if defined(ESP32)
  Serial2.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN);
#else
  tfSerial.begin(115200);
#endif

  // Clear incoming buffer
  while (tfSerial.available() > 0) {
    tfSerial.read();
  }

  // Header for serial reader / CSV parsing
  Serial.println(F("yaw_deg,pitch_deg,distance_cm,strength"));
}

// 8-sample oversampling ring buffer for sub-centimeter decimal precision
#define OVERSAMPLE_SIZE 8
int dist_history[OVERSAMPLE_SIZE];
int history_idx = 0;
bool history_full = false;

float getDecimalDistance(int raw_cm) {
  dist_history[history_idx] = raw_cm;
  history_idx = (history_idx + 1) % OVERSAMPLE_SIZE;
  if (history_idx == 0) history_full = true;
  int count = history_full ? OVERSAMPLE_SIZE : history_idx;
  long sum = 0;
  for (int i = 0; i < count; i++) {
    sum += dist_history[i];
  }
  return (float)sum / (float)count;
}

void loop() {
  if (getTFLunaData(distance, strength)) {
    float dist_decimal = getDecimalDistance(distance);
    // Stream live CSV telemetry with 2 decimal places (e.g., 35.38 cm)
    Serial.print(F("0,0,"));
    Serial.print(dist_decimal, 2);
    Serial.print(F(","));
    Serial.println(strength);
    
    // 15ms pacing (~65 Hz) prevents USB buffer backlog lag
    delay(15);
  }
}

