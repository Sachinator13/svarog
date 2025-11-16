/*
 * Dual VL53L0X Time-of-Flight Sensor using Pololu Library
 * 
 * Hardware Connections:
 * - Both sensors SCL -> A5
 * - Both sensors SDA -> A4
 * - Sensor 1 XSHUT -> D4
 * - Sensor 2 XSHUT -> D5
 * - VCC -> 5V (or 3.3V if your board requires it)
 * - GND -> GND
 */

#include <Wire.h>
#include "VL53L0X.h"

// Create two sensor objects
VL53L0X lox1;
VL53L0X lox2;

// XSHUT pins - adapted to your configuration
#define SHT_LOX1 4
#define SHT_LOX2 5

// New I2C addresses we'll assign
#define LOX1_ADDRESS 0x30
#define LOX2_ADDRESS 0x31

int sensor1, sensor2;

/*
 * setID() - Change I2C addresses of sensors
 * 
 * Process:
 * 1. Reset all sensors by setting XSHUT pins LOW
 * 2. Bring all sensors out of reset by setting XSHUT HIGH
 * 3. Keep sensor 1 awake, put sensor 2 to sleep
 * 4. Initialize sensor 1 and change its address
 * 5. Wake up sensor 2
 * 6. Initialize sensor 2 and change its address
 */
void setID() {
  // All reset
  digitalWrite(SHT_LOX1, LOW);    
  digitalWrite(SHT_LOX2, LOW);
  delay(10);
  
  // All unreset
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  // Activating LOX1 and resetting LOX2
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, LOW);
  Serial.println("Sensor 1 enabled, sensor 2 disabled");
  delay(50);  // Give sensor 1 time to wake up

  // Initializing LOX1
  Serial.println("Initializing sensor 1...");
  lox1.setTimeout(500);
  if(!lox1.init()) {
    Serial.println(F("Failed to boot first VL53L0X"));
    Serial.println(F("Check: Power, SDA/SCL wiring, sensor 1 XSHUT connection"));
    while(1);
  }
  
  // Change address of sensor 1
  lox1.setAddress(LOX1_ADDRESS);
  Serial.print("Sensor 1 initialized at address 0x");
  Serial.println(LOX1_ADDRESS, HEX);
  delay(10);

  // Activating LOX2
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  // Initializing LOX2
  Serial.println("Initializing sensor 2...");
  lox2.setTimeout(500);
  if(!lox2.init()) {
    Serial.println(F("Failed to boot second VL53L0X"));
    Serial.println(F("Check: Power, sensor 2 XSHUT connection to D5"));
    while(1);
  }
  
  // Change address of sensor 2
  lox2.setAddress(LOX2_ADDRESS);
  Serial.print("Sensor 2 initialized at address 0x");
  Serial.println(LOX2_ADDRESS, HEX);
}

void read_dual_sensors() {
  
  // Read from sensor 1
  sensor1 = lox1.readRangeSingleMillimeters();
  // Serial.print("1: ");
  // if (lox1.timeoutOccurred()) {
  //   Serial.print("TIMEOUT");
  // } else {
  //   Serial.print(sensor1);
  //   Serial.print("mm");
  // }
  
  // Serial.print("  ");

  // Read from sensor 2
  sensor2 = lox2.readRangeSingleMillimeters();
  // Serial.print("2: ");
  // if (lox2.timeoutOccurred()) {
  //   Serial.print("TIMEOUT");
  // } else {
  //   Serial.print(sensor2);
  //   Serial.print("mm");
  // }
  
  // Serial.println();
}

void setup() {
  Serial.begin(115200);

  // Wait until serial port opens for native USB devices
  while (!Serial) { delay(1); }

  // CRITICAL: Wait for power to stabilize before initializing sensors
  // VL53L0X needs stable voltage before I2C communication
  Serial.println("Waiting for power to stabilize...");
  delay(500);  // 500ms delay for power stabilization

  pinMode(SHT_LOX1, OUTPUT);
  pinMode(SHT_LOX2, OUTPUT);

  Serial.println("Shutdown pins initialized...");

  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);

  Serial.println("Both in reset mode...(pins are low)");
  
  Serial.println("Starting...");
  Wire.begin();
  
  setID();
  
  Serial.println("Both sensors ready!");
  Serial.println();
}

void loop() {
  read_dual_sensors();
  delay(100);

  // === Serial Plotter Output for Distances ===
  Serial.print("Sensor1:");
  Serial.print(sensor1);
  Serial.print(" Sensor2:");
  Serial.println(sensor2);
}
