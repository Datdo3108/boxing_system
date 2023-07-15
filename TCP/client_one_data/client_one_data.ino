#include <ESP8266WiFi.h>
#include <Wire.h>
#include <MPU6050_light.h>

const int rate = 100; // rate in milliseconds

const char* ssid = "LAPTOP-IO4BI4LC 0162";
const char* password = "lam123456";

const char* serverIP = "192.168.137.1";
const int serverPort = 1234;

MPU6050 mpu(Wire);

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    }
    Serial.println("Connected");

    Wire.begin();
    mpu.begin();
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;

        if (!client.connect(serverIP, serverPort)) {
            Serial.println("Connection failed.");
            delay(2000);
            return;
        }

        while (1) {
            mpu.update();

            float x, y, z;

            // Set values to send
            x = mpu.getAngleX();

            Serial.printf("%f\n", x);

            String message = String(x);
            client.print(message);
            Serial.println("Message sent to server");
            delay(rate);
        }
        

    }
}
