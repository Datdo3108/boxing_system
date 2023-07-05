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
#include <HX711_ADC.h> // https://github.com/olkal/HX711_ADC
#include <Wire.h>
#include <stdio.h>
#include <stdlib.h>

// constant variables
// Set your Board ID (ESP32 Sender #1 = BOARD_ID 1, ESP32 Sender #2 = BOARD_ID 2, etc)
#define BOARD_ID 2
unsigned long lastTime = 0;
unsigned long timerDelay = 1;
// REPLACE WITH RECEIVER MAC Address
uint8_t broadcastAddress[] = {0x10, 0x52, 0x1C, 0xE2, 0xE1, 0x50};


HX711_ADC LoadCell(4, 5); // parameters: dt pin, sck pin<span data-mce-type="bookmark" style="display: inline-block; width: 0px; overflow: hidden; line-height: 0;" class="mce_SELRES_start"></span>

// data structure to send data must match with receiver
struct struct_loadcell {
    int id;
    float x;
} loadcell_data;

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
  
  // INIT LOAD CELL
  LoadCell.begin(); // start connection to HX711
  LoadCell.start(2000); // load cells gets 2000ms of time to stabilize
  /* setCalFactor() set the calibration factor for the load cell to 10000
   (Need to adjust this value later). */
  LoadCell.setCalFactor(10000);

  // INIT ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  } 
  // Set ESP-NOW role
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);

  // Once ESPNow is successfully init, we will register for Send CB to
  // get the status of Trasnmitted packet
  /*
    OnDataSent callback function is registered using esp_now_register_send_cb().
    This ensures that the OnDataSent function is called when a data packet is transmitted.
  */
  esp_now_register_send_cb(OnDataSent);
  
  // add a new peer device to the ESP-NOW network
  /* esp_now_add_peer() has two mandatory parameters
    + mac_addr: MAC address of recipient
    + role: role of the peer being added
  
  */
  esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);

}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    LoadCell.update(); // retrieves data from the load cell
    // Set values to send
    loadcell_data.id = BOARD_ID;
    loadcell_data.x = LoadCell.getData();

    // Send message via ESP-NOW
    /* esp_now_send() takes 3 parameters: 
      + the recipient's MAC address (in this case, 0 indicates broadcasting to all devices)
      + a pointer to the data to be sent (&data),
      + size of the data in bytes (sizeof(data)). */
    esp_now_send(0, (uint8_t *) &loadcell_data, sizeof(loadcell_data));
    lastTime = millis();
  }
}