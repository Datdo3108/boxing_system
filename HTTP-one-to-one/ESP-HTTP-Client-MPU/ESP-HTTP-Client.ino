// Setup the client to send sensor data to the server
#include <ESP8266WiFi.h>
#include <Wire.h>
#include <MPU6050_light.h>

// Initialize sensor parameters
MPU6050 mpu(Wire);
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
  mpu.begin();
  
  // Connect to the server
  WiFi.begin(ssid,password);
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
  mpu.update();
  if((millis()-timer)>10){
    x = mpu.getAngleX();
    y = mpu.getAngleY();
    z = mpu.getAngleZ();
    Serial.print("x angle: ");
    Serial.print(x);
    Serial.print("___y angle: ");
    Serial.print(y);
    Serial.print("___z angle: ");
    Serial.println(z);
    // Connect to the server and send the data as a URL parameter
    if(client.connect(host,80)) {
      String url = "/update?value=";
      url += String(x) + "," + String(y) + "," + String(z);
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