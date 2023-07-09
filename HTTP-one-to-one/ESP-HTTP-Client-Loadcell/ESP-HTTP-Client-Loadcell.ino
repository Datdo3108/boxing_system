// Setup the client to send sensor data to the server
#include <ESP8266WiFi.h>
#include <Wire.h>
#include <HX711_ADC.h> // https://github.com/olkal/HX711_ADC
#include <stdio.h>
#include <stdlib.h>

// Initialize sensor parameters
HX711_ADC LoadCell(4, 5); // parameters: dt pin, sck pin<span data-mce-type="bookmark" style="display: inline-block; width: 0px; overflow: hidden; line-height: 0;" class="mce_SELRES_start"></span>
unsigned long timer = 0;
float x, y, z;

// Initialize network parameters
const char* ssid = "ESP8266";
const char* password = "31082002";
const char* host = "192.168.11.4"; // as specified in server.ino

// Set up the client object
WiFiClient client;

// Configure deep sleep in between measurements
const int sleepTimeSeconds = 2;

void setup() {
  Wire.begin();
  LoadCell.begin(); // start connection to HX711
  LoadCell.start(2000); // load cells gets 2000ms of time to stabilize
  LoadCell.setCalFactor(10000);
  
  // Connect to the server
  WiFi.begin(ssid, password);
  Serial.begin(115200);
  while(WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("IP Address (AP): "); Serial.println(WiFi.localIP());
  // Read all the lines of the response and print them to Serial
  Serial.println("Response: ");
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if((millis()-timer) > 10){
    // Read sensor value each 10 ms
    LoadCell.update(); // retrieves data from the load cell
    float i = LoadCell.getData(); // get output value
    Serial.print(" Load cell value: ");
    Serial.print(i);

    // Connect to the server and send the data as a URL parameter
    if(client.connect(host,80)) {
      String url = "/update?value=";
      url += String(x);
      client.print(String("GET ") + url + " HTTP/1.1\r\n" + "Host: " + host +  "\r\n" + 
                  "Connection: keep-alive\r\n\r\n"); // minimum set of required URL headers
      
      // GET /update?value=__x__ HTTP/1.1\r
      // Host: 192.168.11.4\r
      // Connection: keep-alive\r
      // \r

      delay(10);
    }
    timer = millis();
  }
}