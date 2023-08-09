#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <MPU6050_light.h>

const char* ssid = "LAPTOP-IO4BI4LC 0162";
const char* password = "lam123456";
const IPAddress laptopIP(192, 168, 137, 1);  // Replace with your laptop's IP address
const unsigned int laptopPort = 1234;        // Replace with the desired port number

const unsigned int localPort = 8888;  // Local port to listen on

WiFiUDP udp;
MPU6050 mpu(Wire);

void setup() {
    Serial.begin(115200);
    Wire.begin();
    mpu.begin();
    WiFi.begin(ssid, password);

    Serial.println("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }

    Serial.println("Connected to WiFi");

    udp.begin(localPort);
}

void loop() {
    mpu.update();

    // Read your sensor data or prepare the data you want to send
    // Set values to send
    float x = mpu.getAngleX();
    float y = mpu.getAngleY();
    float z = mpu.getAngleZ();
    String dataToSend =  String(x) +";"+ String(y) + ";" + String(z);

    // Send the data to the laptop
    udp.beginPacket(laptopIP, laptopPort);
    udp.write(dataToSend.c_str(), dataToSend.length());
    udp.endPacket();

    delay(10);  // Adjust the delay according to your requirements
}
