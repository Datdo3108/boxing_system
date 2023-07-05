/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-many-to-one-esp8266-nodemcu/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

#include <ESP8266WiFi.h>
#include <espnow.h>

// sensor libraries
#include <Wire.h>
#include <MPU6050_light.h>


// constant variables
// Set your Board ID (ESP32 Sender #1 = BOARD_ID 1, ESP32 Sender #2 = BOARD_ID 2, etc)
#define BOARD_ID 1 // 1 for MPU6050
unsigned long lastTime = 0;
unsigned long timerDelay = 1;
// REPLACE WITH RECEIVER MAC Address
uint8_t broadcastAddress[] = {0x10, 0x52, 0x1C, 0xE2, 0xE1, 0x50};


MPU6050 mpu(Wire);

// Structure example to send data
// Must match the receiver structure
struct struct_mpu {
    int id;
    float x;
    float y;
    float z;
} mpu_data;


// Callback when data is sent
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  Serial.print("\r\nLast Packet Send Status: ");
  if (sendStatus == 0){
    Serial.println("Delivery success");
  }
  else{
    Serial.println("Delivery fail");
  }
}

void setup() {
  // INIT SERIAL: baud rate 115200
  Serial.begin(115200);

  // INIT WIFI
  // Set the Wi-Fi mode to WIFI_STA (Wi-Fi Station mode)
  WiFi.mode(WIFI_STA);
  // Disconnect from any previously connected Wi-Fi networks
  WiFi.disconnect();

  // INIT MPU6050
  Wire.begin();
  mpu.begin();

  // INIT ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  } 
  // Set ESP-NOW role
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);

  // Once ESPNow is successfully init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  /*
    OnDataSent callback function is registered using esp_now_register_send_cb().
    This ensures that the OnDataSent function is called when a data packet is transmitted.
  */
  esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);

}

void loop() {
  mpu.update();
  if ((millis() - lastTime) > timerDelay) {
    // Set values to send
    mpu_data.id = BOARD_ID;
    mpu_data.x = mpu.getAngleX();
    mpu_data.y = mpu.getAngleY();
    mpu_data.z = mpu.getAngleZ();

    // Send message via ESP-NOW
    /* esp_now_send() takes 3 parameters: 
      + the recipient's MAC address (in this case, 0 indicates broadcasting to all devices)
      + a pointer to the data to be sent (&data),
      + size of the data in bytes (sizeof(data)). */
    esp_now_send(0, (uint8_t *) &mpu_data, sizeof(mpu_data));
    lastTime = millis();
  }
}