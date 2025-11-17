/*
 * Dual VL53L0X with XSHUT Toggle - MAFIA-PROOF VERSION
 * 
 * Fixed: Properly reinitializes sensors on every switch
 */

#include <Wire.h>
#include "VL53L0X.h"

// XSHUT pins
#define SHT_LOX1 4
#define SHT_LOX2 5

// I2C addresses
#define LOX1_ADDRESS 0x30
#define LOX2_ADDRESS 0x31

int distance;
bool sensor1_active = true;

// Declare sensor objects globally but initialize in functions
VL53L0X* activeSensor = nullptr;

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(1); }

  Serial.println("Waiting for power to stabilize...");
  delay(500);

  pinMode(SHT_LOX1, OUTPUT);
  pinMode(SHT_LOX2, OUTPUT);

  // Power down both sensors initially
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  delay(100);

  Wire.begin();

  // Start with sensor 1
  activateSensor1();
  
  Serial.println("Sensor 1 active. Starting measurements...\n");
}

void activateSensor1() {
  // CRITICAL: Power down both sensors first
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  delay(100);  // Wait for complete shutdown
  
  // Create fresh sensor object
  if (activeSensor != nullptr) {
    delete activeSensor;
  }
  activeSensor = new VL53L0X();
  
  // Power up only sensor 1
  digitalWrite(SHT_LOX1, HIGH);
  delay(100);  // Critical: give sensor time to boot
  
  // Initialize with fresh object
  activeSensor->setTimeout(500);
  if(!activeSensor->init()) {
    Serial.println(F("FATAL: Failed to initialize sensor 1"));
    while(1);
  }
  
  // Set custom address
  activeSensor->setAddress(LOX1_ADDRESS);
  delay(10);
  
  Serial.println("Sensor 1 reinitialized successfully");
}

void activateSensor2() {
  // CRITICAL: Power down both sensors first
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  delay(100);  // Wait for complete shutdown
  
  // Create fresh sensor object
  if (activeSensor != nullptr) {
    delete activeSensor;
  }
  activeSensor = new VL53L0X();
  
  // Power up only sensor 2
  digitalWrite(SHT_LOX2, HIGH);
  delay(100);  // Critical: give sensor time to boot
  
  // Initialize with fresh object
  activeSensor->setTimeout(500);
  if(!activeSensor->init()) {
    Serial.println(F("FATAL: Failed to initialize sensor 2"));
    while(1);
  }
  
  // Set custom address
  activeSensor->setAddress(LOX2_ADDRESS);
  delay(10);
  
  Serial.println("Sensor 2 reinitialized successfully");
}

void toggleSensor() {
  sensor1_active = !sensor1_active;
  
  if (sensor1_active) {
    Serial.println("\n>>> Switching to Sensor 1 <<<");
    activateSensor1();
  } else {
    Serial.println("\n>>> Switching to Sensor 2 <<<");
    activateSensor2();
  }
}

void loop() {
  // Read from active sensor
  if (activeSensor != nullptr) {
    distance = activeSensor->readRangeSingleMillimeters();
    
    if (sensor1_active) {
      Serial.print("Sensor1:");
    } else {
      Serial.print("Sensor2:");
    }
    Serial.println(distance);
  }
  
  delay(100);
  
  // Toggle every 2 seconds
  static int count = 0;
  count++;
  if (count >= 20) {
    toggleSensor();
    count = 0;
  }
}