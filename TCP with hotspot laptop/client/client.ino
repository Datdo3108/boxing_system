#include <ESP8266WiFi.h>
#include <Wire.h>
#include <MPU6050_light.h>

const char* ssid = "LAPTOP-IO4BI4LC 0162";
const char* password = "lam123456";

MPU6050 mpu(Wire);

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println(".");
    }
    Serial.println("Connected");

    Wire.begin();
    mpu.begin();
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    const char* serverIP = "192.168.137.1";
    const int serverPort = 1234;

    if (!client.connect(serverIP, serverPort)) {
        Serial.println("Connection failed.");
        delay(5000);
        return;
    }

    String message = "Hello, server!";
    client.print(message);
    Serial.println("Message sent to server");

    delay(1000);
    }
}
